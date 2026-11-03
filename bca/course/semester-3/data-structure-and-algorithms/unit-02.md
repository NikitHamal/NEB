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

## 2.7 Seeing the ideas: the stack in pictures

A stack is the easiest structure to imagine because it exists on every kitchen shelf: a pile of plates. You put a clean plate on top and you take the top plate when you need one; nobody pulls a plate from the middle. This last-in, first-out behaviour is the whole idea, and the three figures that follow show how it organises storage, expression evaluation and bracket checking.

```photogrid label="2.1" cols="2" ratio="1.2" caption="The stack in the kitchen and in memory. (a) A pile of plates: only the top plate can be added or removed, which is LIFO order; a full pile that would topple is an overflow and an empty shelf is an underflow. (b) The same pile as a C array of size 5 with an integer top. After push(10), push(20), push(30) the array holds three items and top is 2; one pop leaves two items and top is 1. The value 30 is still in memory but is no longer part of the stack."
@ photo id="bca201/plates" cap="A pile of plates is a stack"
fit 1.2
focus 0.5 0.35
call 0.5 0.12 0.06 0.9 "top of the stack"
@ svg cap="Array stack after push 10, 20, 30 then pop"
f = Fig(300, 250)
for i in range(5):
    y = 195 - i * 38
    filled = i < 2
    f.box(90, y, 90, 34, ["10", "20", "30", "", ""][i] if i < 2 else ("30 (stale)" if i == 2 else ""), fill=BLUE if filled else SOFT, stroke=NAVY, size=10.5, bold=True, r=0)
    f.text(76, y + 17, "[%d]" % i, size=9.5, color=SLATE, anchor="end")
f.arrow([(230, 120), (186, 120)], color=RED, sw=1.8)
f.text(235, 105, "top = 1", size=10.5, color=RED, bold=True, anchor="start")
f.text(150, 14, "items[ ] of size 5", size=10.5, color=NAVY, bold=True)
f.text(150, 238, "overflow if top = 4; underflow if top = -1", size=9.5, color=SLATE)
```

```svgfig label="2.1" caption="Evaluating the postfix expression 8 2 + 3 * 6 2 / - with a stack. Each number is pushed; each operator pops two values, applies the operation (the first value popped is the right operand) and pushes the result. The stack after each token is shown from bottom to top. The final single value, 27, is the answer to the infix expression (8 + 2) * 3 - 6 / 2. No brackets and no precedence rules are needed once the expression is in postfix form."
f = Fig(580, 200)
toks = ["8", "2", "+", "3", "*", "6", "2", "/", "-"]
stk = [["8"], ["8", "2"], ["10"], ["10", "3"], ["30"], ["30", "6"], ["30", "6", "2"], ["30", "3"], ["27"]]
for i, t in enumerate(toks):
    x = 8 + i * 64
    op = t in "+-*/"
    f.box(x, 8, 56, 26, t, fill=SAND if op else BLUE, stroke=AMBER if op else NAVY, size=12, bold=True)
    s = stk[i]
    for j, v in enumerate(s):
        f.box(x + 4, 150 - j * 28, 48, 26, v, fill=MINT if i == 8 else SOFT, stroke=TEAL, size=10.5, bold=True, r=0)
f.text(290, 188, "stack depth at most 3; token types: operand pushes, operator pops two and pushes one", size=9.5, color=SLATE)
```

```svgfig label="2.2" caption="Bracket matching with a stack. In the balanced string {[()]} every opening bracket is pushed and every closing bracket must match the item on top; the stack is empty at the end, so the string is balanced. In the faulty string {[(])} the closing square bracket arrives while the top is a round bracket, so the check stops at once with a mismatch. A string such as ((( ends with a non-empty stack, and a string such as ()) hits an empty stack: both are also unbalanced."
f = Fig(580, 190)
def row(y, s, stacks, ok):
    for i, ch in enumerate(s):
        x = 12 + i * 46
        f.box(x, y, 40, 24, ch, fill=BLUE, stroke=NAVY, size=12, bold=True)
        st = stacks[i]
        if st is None:
            continue
        f.text(x + 20, y + 38, "".join(st) if st else "empty", size=10.5, color=TEAL if ok else RED, bold=True)
row(12, "{[()]}", [["{"], ["{", "["], ["{", "[", "("], ["{", "["], ["{"], []], True)
f.text(330, 28, "balanced: stack is empty at the end", size=10.5, color=TEAL, bold=True, anchor="start")
row(100, "{[(])}", [["{"], ["{", "["], ["{", "[", "("], ["stop"], None, None], False)
f.text(330, 116, "unbalanced: ] meets ( on top", size=10.5, color=RED, bold=True, anchor="start")
```

### 2.7.1 Eight applications of stacks

1. **Undo and redo.** Every edit in a word processor or in a Nepali typing tool is pushed on an undo stack. Pressing Ctrl+Z pops the latest edit and reverses it, and the popped edit moves to a redo stack. The last change made is always the first one undone, exactly as a stack behaves.
2. **Back button and navigation history.** A web browser pushes each page you open. The back button pops the current page and shows the one below it. The Nagarik App and Fonepay screens work the same way when you press back after opening a payment form.
3. **Function calls and recursion.** When a C function calls another, its return address and local variables are pushed on the call stack as a stack frame. When the function returns, its frame is popped and execution continues in the caller. This is how recursive functions such as factorial and Towers of Hanoi (Unit 6) work, and why infinite recursion ends with a stack overflow.
4. **Expression evaluation.** Calculators and compilers convert infix expressions to postfix and evaluate them with a stack, as in Figure 2.1. Postfix needs no brackets and no precedence rules at run time. A spreadsheet formula such as the VAT calculation in a billing sheet is processed in this way.
5. **Checking brackets and tags.** A compiler or code editor pushes every opening bracket and matches it with each closing bracket (Figure 2.2). An HTML validator does the same for opening and closing tags. A non-empty stack at the end, or a mismatch on the way, is reported as a syntax error.
6. **Reversing data.** Pushing all characters of a string and then popping them returns the string reversed. The same idea reverses a list of numbers or the order of words in a sentence. It is a common exam program because it shows LIFO order clearly.
7. **Backtracking and depth-first search.** A maze solver or a puzzle solver pushes each choice and pops back to the last choice when it meets a dead end. Depth-first search in a graph (Unit 10) uses a stack in the same way. Without a stack the program would have to remember all earlier choices by hand.
8. **Converting number systems.** To convert a decimal number such as 45 to binary, repeated division by 2 produces the remainders in reverse order. Pushing each remainder and then popping them gives the correct bit order 101101. The same method converts to octal and hexadecimal.

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

## Model answers (5 and 10 marks)

**Q1. Explain the stack ADT with its operations and the conditions overflow and underflow. (5 marks)**

A **stack** is a linear data structure in which insertion and deletion take place only at one end, called the **top**. It follows the **LIFO** (last in, first out) rule: the item pushed last is the one popped first, like a pile of plates (Plate 2.1).

**Operations**
1. `push(x)`: place x on the top; `top` increases by one.
2. `pop()`: remove and return the top item; `top` decreases by one.
3. `peek()` (or `top()`): read the top item without removing it.
4. `isEmpty()`: true when `top == -1`.
5. `isFull()`: true when `top == MAX - 1` for an array of size MAX.

**Overflow** happens when `push` is called on a full stack, because there is no cell left. **Underflow** happens when `pop` or `peek` is called on an empty stack, because there is nothing to remove. A correct program tests `isFull()` before each push and `isEmpty()` before each pop and prints a message instead of corrupting memory.

All five operations take constant time, O(1), because only the top index changes. For example, after `push(10)`, `push(20)` and `push(30)` on a stack of size 5, `top` is 2; a `pop` returns 30 and leaves `top` equal to 1. A stack is used for undo, function calls, expression evaluation and bracket checking.

**Q2. Convert the infix expression A + B * (C - D) / E into postfix and evaluate it for A = 6, B = 4, C = 9, D = 5, E = 2. (5 marks)**

**Rules.** Scan the infix expression from left to right. Operands go straight to the output. An operator is pushed on the stack after popping every operator on the stack that has higher or equal precedence (`*` and `/` are higher than `+` and `-`). An opening bracket is pushed; a closing bracket pops operators to the output until the opening bracket is found. At the end, pop everything.

**Conversion.**
1. `A` goes to output: `A`.
2. `+` is pushed. Stack: `+`.
3. `B` goes to output: `A B`.
4. `*` has higher precedence than `+`, so it is pushed. Stack: `+ *`.
5. `(` is pushed; `C` goes to output: `A B C`.
6. `-` is pushed above `(`; `D` goes to output: `A B C D`.
7. `)` pops `-`: output `A B C D -`; the bracket is discarded.
8. `/` has the same precedence as `*`, so `*` is popped first: output `A B C D - *`; then `/` is pushed.
9. `E` goes to output; at the end `/` and `+` are popped: **`A B C D - * E / +`**.

**Evaluation.** Substituting values gives `6 4 9 5 - * 2 / +`. Then 9 - 5 = 4; 4 * 4 = 16; 16 / 2 = 8; 6 + 8 = **14**. The stack never holds more than four values, and the result agrees with direct calculation 6 + 4 * (9 - 5) / 2 = 6 + 8 = 14.

**Q3. Explain how a stack is implemented with an array, write the push and pop algorithms, and describe four applications. Evaluate the infix expression (8 + 2) * 3 - 6 / 2 using postfix. (10 marks)**

**Introduction.** A stack is a LIFO list whose only access point is the top. It is implemented either with an array and an integer `top` initialised to -1, or with a linked list (Unit 5). The array version is fast and simple but has a fixed capacity.

**Array implementation (Plate 2.1).** Declare `int items[MAX]; int top = -1;`.

*Push algorithm:* (1) if `top == MAX - 1`, report overflow and stop; (2) `top = top + 1`; (3) `items[top] = x`.

*Pop algorithm:* (1) if `top == -1`, report underflow and stop; (2) `x = items[top]`; (3) `top = top - 1`; (4) return x.

Both take O(1) time, and the space is O(MAX).

**Applications.**
1. *Function calls:* the call stack stores return addresses and local variables, which makes recursion possible.
2. *Expression evaluation:* postfix expressions are evaluated with one stack (Figure 2.1).
3. *Bracket matching:* compilers verify that every bracket and tag is closed in the right order (Figure 2.2).
4. *Undo and back navigation:* editors and browsers keep the history in a stack.

**Conversion of (8 + 2) * 3 - 6 / 2.** Reading the tokens: `(` is pushed; 8 is output; `+` is pushed; 2 is output; `)` pops `+`, giving `8 2 +`; `*` is pushed; 3 is output; `-` has lower precedence than `*`, so `*` is popped (output `8 2 + 3 *`) and `-` is pushed; 6 is output; `/` has higher precedence than `-`, so it is pushed; 2 is output; at the end `/` and `-` are popped. The postfix form is **`8 2 + 3 * 6 2 / -`**.

**Evaluation (Figure 2.1).**

| Token | Action | Stack (bottom to top) |
|---|---|---|
| 8, 2 | push | 8, 2 |
| `+` | pop 2 and 8, push 10 | 10 |
| 3 | push | 10, 3 |
| `*` | pop 3 and 10, push 30 | 30 |
| 6, 2 | push | 30, 6, 2 |
| `/` | pop 2 and 6, push 3 | 30, 3 |
| `-` | pop 3 and 30, push 27 | 27 |

The answer is **27**, and one value remains on the stack, which confirms the expression was well formed.

**Conclusion.** The stack is simple, but it supports some of the deepest ideas in programming: recursion, parsing and backtracking. Its constant-time operations and strict LIFO discipline make it the natural tool whenever the most recent item must be handled first.
