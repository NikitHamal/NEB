---
subject: DotNet Technology
grade: BCA Semester 7 (Elective II)
unit: 2
title: The C# Language Basics
hours: 12
area: BCA 406 · DotNet Technology · Unit 2
---

Every program, from a marks calculator to an online shop, is built from the same small kit: values with types, operators that combine them, strings, arrays, parameters that carry data into methods, and statements that decide and repeat. This unit teaches that kit in the order of the TU outline: console and GUI applications, identifiers and keywords, comments, data types, expressions and operators, strings and characters, arrays, variables and parameters, statements and namespaces. Each idea comes with a program that was compiled and run, and the printed output is the real output.

::: key What this unit gives you
- How a console or a GUI program is laid out and how it reads and writes data.
- The rules for identifiers, the keyword list, naming conventions and the three kinds of comment.
- Every built-in type with its size and range, literals, conversions, boxing, `checked`, nullable values, `const` and `readonly`.
- Operators and their precedence, strings and `StringBuilder`, characters, one-, two-dimensional and jagged arrays.
- Value, `ref`, `out`, `in` and `params` parameters, optional and named arguments, and every kind of statement.
- Namespaces and the `using` directive.
:::

## 2.1 Writing console and GUI applications

A **console application** talks to the user through text in a terminal. The `System.Console` class gives you the whole interface:

| Member | Purpose |
|---|---|
| `Console.Write(x)` and `Console.WriteLine(x)` | Print without and with a new line |
| `Console.ReadLine()` | Read one line as a `string` (`null` at end of input) |
| `Console.Read()` and `Console.ReadKey()` | Read one character or one key press |
| `Console.WriteLine("{0} + {1}", a, b)` | Composite formatting with numbered placeholders |
| `Console.WriteLine($"{a} + {b}")` | String interpolation (C# 6 and later) |
| `Console.Error.WriteLine(x)` | Write to the error stream |
| `Console.Clear()`, `Console.ForegroundColor` | Screen control |
| `args` of `Main` | Command-line arguments |

The next program shows reading numbers, converting text safely and printing in three styles. `int.TryParse` returns `false` instead of throwing when the text is not a number, so it is the right choice for user input.

```csharp
// stdin: 12\nabc\n7
using System;

class Adder
{
    static int ReadInt(string prompt)
    {
        while (true)
        {
            Console.Write(prompt);
            string text = Console.ReadLine();
            int value;
            if (int.TryParse(text, out value)) return value;
            Console.WriteLine("  '" + text + "' is not a whole number, try again.");
        }
    }

    static void Main()
    {
        int a = ReadInt("First number: ");
        int b = ReadInt("Second number: ");
        Console.WriteLine("Concatenation: " + a + " + " + b + " = " + (a + b));
        Console.WriteLine("Composite:     {0} + {1} = {2}", a, b, a + b);
        Console.WriteLine($"Interpolated:  {a} + {b} = {a + b}");
    }
}
```
```output
First number: Second number:   'abc' is not a whole number, try again.
Second number: Concatenation: 12 + 7 = 19
Composite:     12 + 7 = 19
Interpolated:  12 + 7 = 19
```

The typed input was `12`, `abc` and `7`. A real terminal shows what you type; the captured output above does not, which is why the prompts run together on one line.

A **GUI application** (Windows Forms or WPF) is *event driven*. Instead of reading input at a place you choose, you create a window with controls and write **event handlers**, methods that the framework calls when the user clicks, types or resizes. `Application.Run(form)` starts the message loop that waits for events. The skeleton below adds two text boxes and a button; the handler converts the text, adds the numbers and shows the sum. It is compiled by the book's script but not executed because there is no screen.

```csharp
// compile-only
using System;
using System.Drawing;
using System.Windows.Forms;

public class AdderForm : Form
{
    TextBox txtA = new TextBox { Left = 20, Top = 20, Width = 80 };
    TextBox txtB = new TextBox { Left = 110, Top = 20, Width = 80 };
    Button btn = new Button { Text = "Add", Left = 200, Top = 18 };
    Label lbl = new Label { Left = 20, Top = 60, Width = 260, Text = "Sum appears here" };

    public AdderForm()
    {
        Text = "Adder";
        Size = new Size(320, 140);
        btn.Click += OnAddClick;                 // register the handler
        Controls.AddRange(new Control[] { txtA, txtB, btn, lbl });
    }

    void OnAddClick(object sender, EventArgs e)
    {
        int a, b;
        if (int.TryParse(txtA.Text, out a) && int.TryParse(txtB.Text, out b))
            lbl.Text = "Sum = " + (a + b);
        else
            lbl.Text = "Enter two whole numbers";
    }

    [STAThread]
    static void Main() { Application.Run(new AdderForm()); }
}
```

::: note Console versus GUI in one line
A console program decides when to ask; a GUI program waits and reacts. The language features of Units 2 and 3 are the same in both; only the input and output classes change. Laboratory work asks for both kinds.
:::

## 2.2 Identifiers and keywords

An **identifier** is the name you give to a class, method, variable, namespace and so on. The rules are:

1. It starts with a letter or an underscore `_`; the rest may also contain digits. Unicode letters are allowed (`नाम` is legal).
2. It is case sensitive: `Total`, `total` and `TOTAL` are three names.
3. It cannot be a keyword, unless you prefix it with `@` (`@class` is a legal name, rarely a good idea).
4. It cannot contain spaces or symbols such as `-`, `$` or `#`.

**Keywords** are words with a fixed meaning for the compiler. There are about 80 reserved keywords (`abstract`, `bool`, `class`, `if`, `int`, `namespace`, `new`, `return`, `static`, `void`, `while` and so on) and a group of **contextual keywords** (`var`, `get`, `set`, `value`, `async`, `await`, `yield`, `partial`, `where`) that are special only in a particular place, so `var` can still be used as a variable name although you should not.

Conventions are not enforced but every .NET team follows them:

| Item | Style | Example |
|---|---|---|
| Class, struct, enum, interface (with `I` prefix), method, property, namespace | PascalCase | `StudentRecord`, `IShape`, `GetTotal`, `MarksList` |
| Local variable, parameter | camelCase | `totalMarks`, `rollNo` |
| Private field | `_camelCase` | `_balance` |
| Constant | PascalCase | `MaxStudents` |

```csharp
// noexec
int roll1 = 10;      // legal
int _count = 0;      // legal
int 2nd = 5;         // error: starts with a digit
int total-marks = 3; // error: '-' is not allowed
int class = 4;       // error: keyword
int @class = 4;      // legal, but avoid
```

## 2.3 Comments

Comments are ignored by the compiler and explain the program to people.

```csharp
// noexec
// Single-line comment: runs to the end of the line.

/* Multi-line comment:
   everything between the markers is ignored. It cannot be nested. */

/// <summary>
/// XML documentation comment: three slashes before a type or member.
/// Editors show it as a tooltip and tools can turn it into HTML help.
/// </summary>
/// <param name="radius">Radius in metres.</param>
/// <returns>The area in square metres.</returns>
static double Area(double radius) => Math.PI * radius * radius;
```

Write comments that say *why*, not what: `i++; // add one to i` is noise, while `// the API counts from 1, so convert to a zero-based index` helps the next reader.

## 2.4 Data types

C# is statically typed: every variable has a type fixed at compile time. Types fall into two families (Section 1.4): **value types** and **reference types**. All the built-in names are aliases of types in the `System` namespace.

### Integral types

| C# name | .NET type | Size | Range |
|---|---|---|---|
| `sbyte` | `SByte` | 8 bits | -128 to 127 |
| `byte` | `Byte` | 8 bits | 0 to 255 |
| `short` | `Int16` | 16 bits | -32,768 to 32,767 |
| `ushort` | `UInt16` | 16 bits | 0 to 65,535 |
| `int` | `Int32` | 32 bits | -2,147,483,648 to 2,147,483,647 |
| `uint` | `UInt32` | 32 bits | 0 to 4,294,967,295 |
| `long` | `Int64` | 64 bits | about -9.22 × 10^18 to 9.22 × 10^18 |
| `ulong` | `UInt64` | 64 bits | 0 to about 1.84 × 10^19 |

### Real, boolean and character types

| C# name | Size | Meaning and precision |
|---|---|---|
| `float` | 32 bits | Binary floating point, about 7 significant digits; literal `3.5f` |
| `double` | 64 bits | Binary floating point, about 15 to 16 digits; the default for `3.5` |
| `decimal` | 128 bits | Decimal floating point, 28 to 29 digits; exact for money; literal `3.5m` |
| `bool` | 1 byte | `true` or `false` only (no 0 or 1) |
| `char` | 16 bits | One UTF-16 code unit; literal `'A'`, `'\n'`, `'\u0905'` |
| `string` | reference | Immutable sequence of `char` (Section 2.6) |
| `object` | reference | The root of all types |

```csharp
using System;

class TypesDemo
{
    static void Main()
    {
        Console.WriteLine("int range:   " + int.MinValue + " to " + int.MaxValue);
        Console.WriteLine("byte range:  " + byte.MinValue + " to " + byte.MaxValue);
        Console.WriteLine("sizeof int/long/double/decimal: " + sizeof(int) + " " + sizeof(long) + " " + sizeof(double) + " " + sizeof(decimal));

        double d = 0.1 + 0.2;
        decimal m = 0.1m + 0.2m;
        Console.WriteLine("double  0.1 + 0.2 == 0.3 ? " + (d == 0.3));
        Console.WriteLine("decimal 0.1 + 0.2 == 0.3 ? " + (m == 0.3m));

        Console.WriteLine("7 / 2 = " + 7 / 2 + ",  7 / 2.0 = " + 7 / 2.0 + ",  -7 % 3 = " + -7 % 3);
        char c = 'A';
        Console.WriteLine("'A' + 1 = " + (c + 1) + ", (char)(c + 1) = " + (char)(c + 1));
        Console.WriteLine("default(int) = " + default(int) + ", default(bool) = " + default(bool) + ", default(string) is null: " + (default(string) == null));
    }
}
```
```output
int range:   -2147483648 to 2147483647
byte range:  0 to 255
sizeof int/long/double/decimal: 4 8 8 16
double  0.1 + 0.2 == 0.3 ? False
decimal 0.1 + 0.2 == 0.3 ? True
7 / 2 = 3,  7 / 2.0 = 3.5,  -7 % 3 = -1
'A' + 1 = 66, (char)(c + 1) = B
default(int) = 0, default(bool) = False, default(string) is null: True
```

Two lessons from the output: binary `double` cannot store 0.1 exactly, so equality of computed doubles is unreliable (use `decimal` for money, or compare with a small tolerance); and integer division discards the fraction, so one operand must be real to get `3.5`.

```svgfig label="2.1" caption="The .NET type system. Every type derives from System.Object. Value types (through System.ValueType) hold their data in the variable; reference types hold a reference to a heap object."
f = Fig(600, 230)
f.box(240, 10, 120, 34, "System.Object", fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
f.box(90, 76, 150, 34, "ValueType", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(380, 76, 150, 34, "Reference types", fill=MINT, stroke=TEAL, size=11, bold=True)
f.arrow([(300, 44), (300, 60), (165, 60), (165, 76)], color=SLATE)
f.arrow([(300, 44), (300, 60), (455, 60), (455, 76)], color=SLATE)
f.box(10, 140, 100, 44, "Numeric\nint, double,\ndecimal", fill=SAND, stroke=AMBER, size=9.5)
f.box(118, 140, 80, 44, "bool\nchar", fill=SAND, stroke=AMBER, size=9.5)
f.box(206, 140, 90, 44, "struct\nDateTime", fill=SAND, stroke=AMBER, size=9.5)
f.box(304, 140, 70, 44, "enum", fill=SAND, stroke=AMBER, size=9.5)
f.box(390, 140, 70, 44, "class\nstring", fill=MINT, stroke=TEAL, size=9.5)
f.box(466, 140, 62, 44, "array", fill=MINT, stroke=TEAL, size=9.5)
f.box(534, 140, 60, 44, "interface\ndelegate", fill=MINT, stroke=TEAL, size=9)
for x in (60, 158, 251, 339):
    f.arrow([(165, 110), (165, 124), (x, 124), (x, 140)], color=SLATE)
for x in (425, 497, 564):
    f.arrow([(455, 110), (455, 124), (x, 124), (x, 140)], color=SLATE)
f.text(300, 212, "Value types: copied on assignment.   Reference types: the reference is copied.", size=10, color=SLATE)
```

### Literals and `var`

A **literal** is a value written directly in code. Suffixes choose the type: `10L` long, `10U` uint, `3.5f` float, `3.5m` decimal. Prefixes give other bases: `0xFF` hexadecimal (255) and `0b1010` binary (10). **Digit separators** make long numbers readable: `1_000_000`. `var` asks the compiler to *infer* the type from the right-hand side (`var n = 5;` is an `int`); the variable is still statically typed and cannot later hold a string.

### Nullable value types

A value type cannot be `null`, but a database column or a missing form field can be "no value". `int?` (shorthand for `Nullable<int>`) holds an int or null. Use `HasValue`, `Value` and the null-coalescing operator `??`:

```csharp
using System;

class NullableDemo
{
    static void Main()
    {
        int? age = null;
        Console.WriteLine("HasValue: " + age.HasValue);
        Console.WriteLine("age ?? -1 = " + (age ?? -1));
        age = 21;
        Console.WriteLine("HasValue: " + age.HasValue + ", Value: " + age.Value);
        int? next = age + 1;
        int? none = age + null;
        Console.WriteLine("age + 1 = " + next + ", age + null is null: " + (none == null));
    }
}
```
```output
HasValue: False
age ?? -1 = -1
HasValue: True, Value: 21
age + 1 = 22, age + null is null: True
```

### Type conversion

**Implicit conversion** happens automatically when no information can be lost (`int` to `long`, `int` to `double`). **Explicit conversion** (a *cast*) is required when information may be lost: `(int)3.9` gives 3 (truncation, not rounding). The `Convert` class rounds ("banker's rounding") and converts between many types; `Parse` and `TryParse` convert text.

| Expression | Result | Why |
|---|---|---|
| `long x = 5;` | 5 | implicit widening |
| `int y = (int)3.9;` | 3 | explicit; fraction truncated |
| `Convert.ToInt32(3.5)` | 4 | rounds to the nearest even number: 3.5 gives 4, 2.5 gives 2 |
| `(byte)300` | 44 | only the low 8 bits are kept (300 mod 256) when unchecked |
| `int.Parse("42")` | 42 | throws `FormatException` for "4x2" |
| `int.TryParse("4x2", out n)` | `false` | no exception |

**Boxing** converts a value type to `object` (or an interface) by allocating a heap object and copying the value into it; **unboxing** copies it back and needs an exact cast. Boxing costs memory and time, which is why generic collections (Unit 3) replaced the old `ArrayList`.

```csharp
using System;

class ConvertDemo
{
    static void Main()
    {
        Console.WriteLine("(int)3.9 = " + (int)3.9 + ",  (int)-3.9 = " + (int)-3.9);
        Console.WriteLine("Convert.ToInt32(3.5) = " + Convert.ToInt32(3.5) + ",  Convert.ToInt32(2.5) = " + Convert.ToInt32(2.5));
        Console.WriteLine("Math.Round(2.5, MidpointRounding.AwayFromZero) = " + Math.Round(2.5, MidpointRounding.AwayFromZero));
        int big = 300;
        Console.WriteLine("(byte)300 unchecked = " + unchecked((byte)big));
        try { Console.WriteLine(checked((byte)big)); }
        catch (OverflowException e) { Console.WriteLine("checked cast: " + e.GetType().Name); }

        int i = 123;
        object boxed = i;           // boxing: copy to the heap
        i = 456;                    // the box is not affected
        int back = (int)boxed;      // unboxing
        Console.WriteLine("boxed = " + boxed + ", i = " + i + ", unboxed = " + back);
        try { long wrong = (long)boxed; }
        catch (InvalidCastException) { Console.WriteLine("unboxing needs the exact type: (long) of a boxed int fails"); }
    }
}
```
```output
(int)3.9 = 3,  (int)-3.9 = -3
Convert.ToInt32(3.5) = 4,  Convert.ToInt32(2.5) = 2
Math.Round(2.5, MidpointRounding.AwayFromZero) = 3
(byte)300 unchecked = 44
checked cast: OverflowException
boxed = 123, i = 456, unboxed = 123
unboxing needs the exact type: (long) of a boxed int fails
```

### Constants, `readonly` and enumerations

`const` fixes a value at **compile time** (`const double Pi = 3.14159;`) and is implicitly static; only numbers, strings, `bool`, `char` and `null` are allowed. `readonly` fixes a **field** after the constructor has run, so its value may be computed at run time (`readonly DateTime created = DateTime.Now;`). Both stop accidental change. Enumerations (`enum`) give names to integer constants and are explained in Unit 3.
## 2.5 Expressions and operators

An **expression** is a combination of values, variables and operators that produces a value. An **operator** acts on one (unary), two (binary) or three (ternary) **operands**. Operators in the same row below have the same **precedence**; higher rows bind tighter, and operators of equal precedence group left to right except assignment, the conditional operator and `??`, which group right to left.

| Precedence (high to low) | Operators |
|---|---|
| Primary | `x.y`, `f(x)`, `a[i]`, `x++`, `x--`, `new`, `typeof`, `sizeof`, `checked`, `nameof`, `x?.y` |
| Unary | `+x`, `-x`, `!x`, `~x`, `++x`, `--x`, `(T)x` (cast) |
| Multiplicative | `*`, `/`, `%` |
| Additive | `+`, `-` |
| Shift | `<<`, `>>` |
| Relational and type testing | `<`, `>`, `<=`, `>=`, `is`, `as` |
| Equality | `==`, `!=` |
| Bitwise AND, XOR, OR | `&`, then `^`, then `\|` |
| Conditional AND, OR | `&&`, then `\|\|` |
| Null-coalescing | `??` |
| Conditional | `?:` |
| Assignment and lambda | `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `\|=`, `^=`, `<<=`, `>>=`, `=>` |

**Arithmetic.** `/` on two integers is integer division (the fraction is discarded); `%` is the remainder and takes the sign of the left operand (`-7 % 3` is `-1`). Dividing an integer by zero throws `DivideByZeroException`, while a floating-point division by zero gives `Infinity` or `NaN`. `++` and `--` add or subtract one; the prefix form (`++x`) changes first and yields the new value, the postfix form (`x++`) yields the old value and then changes.

**Relational and logical.** `==`, `!=`, `<`, `>`, `<=`, `>=` give `bool`. `&&` and `||` are **short-circuit**: `a && b` does not evaluate `b` when `a` is false, which is how `if (s != null && s.Length > 0)` avoids a null reference. `&` and `|` on bools always evaluate both sides; `!` negates.

**Bitwise and shift.** `&`, `|`, `^`, `~` work on the individual bits of integers; `x << n` multiplies by 2^n and `x >> n` divides by 2^n (for non-negative values).

**Null-related operators.** `a ?? b` is `a` unless `a` is null, then `b`. `s?.Length` gives `null` instead of throwing when `s` is null. `x ??= y` assigns only if `x` is null (C# 8).

**Type operators.** `x is T` tests the run-time type and, with a pattern, declares a variable (`if (o is int n)`); `x as T` converts or gives `null` instead of throwing; `typeof(T)` gives the `Type` object; `sizeof` gives the size of a value type; `nameof(x)` gives the name of a variable or member as a string.

::: example Precedence and increment by hand
Let `int a = 5, b = 3;`. Then `a + b * 2` is 11, not 16, because `*` binds tighter; `(a + b) * 2` is 16. `a++ + ++b` evaluates `a++` (value 5, then `a` becomes 6) and `++b` (b becomes 4, value 4), so the sum is 9; afterwards `a = 6` and `b = 4`. `a > b && b > 0 || false` is `(true && true) || false`, which is `true`.
:::

```csharp
using System;

class OperatorsDemo
{
    static void Main()
    {
        int a = 5, b = 3;
        Console.WriteLine("a + b * 2 = " + (a + b * 2) + ",  (a + b) * 2 = " + ((a + b) * 2));
        int r = a++ + ++b;
        Console.WriteLine("a++ + ++b = " + r + ", a = " + a + ", b = " + b);
        Console.WriteLine("5 & 3 = " + (5 & 3) + ", 5 | 3 = " + (5 | 3) + ", 5 ^ 3 = " + (5 ^ 3) + ", ~5 = " + (~5));
        Console.WriteLine("1 << 4 = " + (1 << 4) + ", 64 >> 3 = " + (64 >> 3));

        string s = null;
        Console.WriteLine("s?.Length is null: " + (s?.Length == null) + ", (s ?? \"default\") = " + (s ?? "default"));
        bool called = false;
        bool ok = (a < 0) && Check(ref called);       // second operand never runs
        Console.WriteLine("short circuit: Check was called = " + called);

        object o = 42;
        if (o is int n) Console.WriteLine("o is an int with value " + n);
        string text = o as string;
        Console.WriteLine("o as string = " + (text == null ? "null" : text));
        int mark = 55;
        Console.WriteLine(mark >= 40 ? "Pass" : "Fail");
        try { int zero = 0; Console.WriteLine(10 / zero); }
        catch (DivideByZeroException) { Console.WriteLine("integer 10 / 0 throws DivideByZeroException; 10.0 / 0 = " + 10.0 / 0); }
    }

    static bool Check(ref bool flag) { flag = true; return true; }
}
```
```output
a + b * 2 = 11,  (a + b) * 2 = 16
a++ + ++b = 9, a = 6, b = 4
5 & 3 = 1, 5 | 3 = 7, 5 ^ 3 = 6, ~5 = -6
1 << 4 = 16, 64 >> 3 = 8
s?.Length is null: True, (s ?? "default") = default
short circuit: Check was called = False
o is an int with value 42
o as string = null
Pass
integer 10 / 0 throws DivideByZeroException; 10.0 / 0 = Infinity
```

## 2.6 Strings and characters

### The `char` type

A `char` is a 16-bit UTF-16 code unit. The static methods of `Char` classify and convert it: `char.IsLetter`, `IsDigit`, `IsUpper`, `IsWhiteSpace`, `ToUpper`, `ToLower`. A `char` converts to its numeric code with a cast (`(int)'A'` is 65). Characters outside the basic multilingual plane (many emoji) need two `char`s, so `"😀".Length` is 2; Devanagari letters such as `अ` (U+0905) are one `char`.

### The `string` type

A `string` is a **reference type** that behaves like a value: it is **immutable**. Every "modification" (`Replace`, `ToUpper`, `+`) creates a new string and leaves the old one untouched. The C# compiler also **interns** identical literals so that they share one object.

| Task | Member |
|---|---|
| Length, character at an index | `s.Length`, `s[i]` |
| Case | `ToUpper()`, `ToLower()` |
| Trim spaces | `Trim()`, `TrimStart()`, `TrimEnd()` |
| Search | `Contains`, `StartsWith`, `EndsWith`, `IndexOf`, `LastIndexOf` |
| Part of a string | `Substring(start, length)`, `Remove`, `Insert` |
| Replace | `Replace("a", "b")` |
| Split and join | `Split(',')`, `string.Join(", ", parts)` |
| Compare | `==`, `Equals`, `string.Compare`, `CompareOrdinal`, `Equals(x, StringComparison.OrdinalIgnoreCase)` |
| Empty tests | `string.IsNullOrEmpty(s)`, `string.IsNullOrWhiteSpace(s)` |
| Build | `+`, `string.Concat`, `string.Format`, `$"..."`, `StringBuilder` |

**Literals.** A regular literal uses escape sequences (`\n` new line, `\t` tab, `\\` backslash, `\"` quote, `\u0905` Unicode). A **verbatim** literal `@"C:\notes\bca.txt"` treats the backslash literally and may span lines. An **interpolated** literal `$"Total: {total:N2}"` evaluates expressions in braces; the part after the colon is a **format specifier**.

| Specifier | Example | Result |
|---|---|---|
| `N2` | `$"{1234.5:N2}"` | `1,234.50` |
| `F1` | `$"{3.14159:F1}"` | `3.1` |
| `C` | `$"{99.5:C}"` | currency in the current culture |
| `D5` | `$"{42:D5}"` | `00042` |
| `X` | `$"{255:X}"` | `FF` |
| `P1` | `$"{0.256:P1}"` | `25.6 %` (spacing is culture dependent) |
| `,10` and `,-10` | `$"{7,5}"` and `$"{7,-5}"` | right and left aligned in a field of width 5 |
| `dd MMM yyyy` | `$"{date:dd MMM yyyy}"` | `05 Jan 2025` |

### `StringBuilder`

Because strings are immutable, building a long text with `+=` in a loop copies the growing text every time (quadratic work). `System.Text.StringBuilder` keeps a resizable buffer and appends in place; call `ToString()` at the end.

```csharp
using System;
using System.Globalization;
using System.Text;

class StringDemo
{
    static void Main()
    {
        CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;
        string s = "  Tribhuvan University, Kathmandu  ";
        string t = s.Trim();
        Console.WriteLine("[" + t + "] length " + t.Length + " (original " + s.Length + ")");
        Console.WriteLine(t.ToUpper() + " | " + t.Substring(0, 9) + " | IndexOf(\"Univ\") = " + t.IndexOf("Univ"));
        Console.WriteLine("Replace: " + t.Replace("Kathmandu", "Kirtipur"));
        string[] parts = "Ram,Sita,Hari".Split(',');
        Console.WriteLine("Split gives " + parts.Length + " parts; Join: " + string.Join(" / ", parts));
        string a = "bca", b = "BCA";
        Console.WriteLine("a == b: " + (a == b) + ", ignoring case: " + a.Equals(b, StringComparison.OrdinalIgnoreCase));
        Console.WriteLine("Compare(\"apple\", \"banana\") < 0: " + (string.Compare("apple", "banana") < 0));

        string path = @"C:\notes\bca.txt";
        Console.WriteLine("Verbatim: " + path);
        double total = 1234.5; int roll = 42;
        Console.WriteLine($"Total {total:N2} | roll {roll:D5} | hex {255:X} | share {0.256:P1} | [{7,5}] [{7,-5}]");

        string x = "abc"; string y = x.ToUpper();
        Console.WriteLine("x is still \"" + x + "\" after ToUpper (immutable); y = " + y);

        var sb = new StringBuilder();
        for (int i = 1; i <= 5; i++) sb.Append(i).Append(i < 5 ? "," : "");
        sb.Insert(0, "[").Append("]");
        Console.WriteLine("StringBuilder: " + sb + ", length " + sb.Length);

        string word = "Level";
        bool pal = true;
        for (int i = 0, j = word.Length - 1; i < j; i++, j--)
            if (char.ToLower(word[i]) != char.ToLower(word[j])) { pal = false; break; }
        Console.WriteLine(word + " is a palindrome: " + pal);
        int letters = 0, digits = 0;
        foreach (char ch in "BCA2025 Sem7") { if (char.IsLetter(ch)) letters++; else if (char.IsDigit(ch)) digits++; }
        Console.WriteLine("letters = " + letters + ", digits = " + digits);
    }
}
```
```output
[Tribhuvan University, Kathmandu] length 31 (original 35)
TRIBHUVAN UNIVERSITY, KATHMANDU | Tribhuvan | IndexOf("Univ") = 10
Replace: Tribhuvan University, Kirtipur
Split gives 3 parts; Join: Ram / Sita / Hari
a == b: False, ignoring case: True
Compare("apple", "banana") < 0: True
Verbatim: C:\notes\bca.txt
Total 1,234.50 | roll 00042 | hex FF | share 25.6 % | [    7] [7    ]
x is still "abc" after ToUpper (immutable); y = ABC
StringBuilder: [1,2,3,4,5], length 11
Level is a palindrome: True
letters = 6, digits = 5
```

::: caution Reference equality versus content equality
For `string`, `==` compares **contents**, because the type overloads it. For ordinary classes `==` compares references unless the class overloads it (Unit 3). Comparing user text with `==` is case sensitive and culture independent; use `StringComparison.OrdinalIgnoreCase` for case-insensitive tests, never `ToLower()` comparisons in security checks.
:::
## 2.7 Arrays

An **array** is a fixed-size, ordered collection of elements of one type, stored contiguously and indexed from zero. In C# an array is a **reference type**: it derives from `System.Array`, lives on the heap, and carries its own `Length`. Elements are initialised to the default of the type (0, `false`, `null`).

| Form | Declaration | Notes |
|---|---|---|
| One-dimensional | `int[] marks = new int[5];` or `int[] m = { 70, 82, 91 };` | `m.Length` is 3 |
| Rectangular (multi-dimensional) | `int[,] grid = new int[3, 4];` | one block, all rows the same length; `GetLength(0)` is rows |
| Jagged (array of arrays) | `int[][] rows = new int[3][];` then `rows[0] = new int[2];` | rows may differ in length |

Useful members: `Array.Sort(a)`, `Array.Reverse(a)`, `Array.IndexOf(a, x)`, `Array.BinarySearch(a, x)` (sorted array), `Array.Copy(src, dst, n)`, `a.Clone()` (shallow copy), `Array.Resize(ref a, n)`, `Array.Fill(a, v)`. The `foreach` loop reads every element without an index; it cannot change the elements of a value-type array. With LINQ (Unit 4), `a.Sum()`, `a.Max()`, `a.Average()` need `using System.Linq;`.

```csharp
using System;
using System.Linq;

class ArrayDemo
{
    static void Main()
    {
        int[] marks = { 72, 55, 91, 38, 64 };
        Console.WriteLine("Length " + marks.Length + ", first " + marks[0] + ", last " + marks[marks.Length - 1]);
        int sum = 0, max = marks[0];
        foreach (int m in marks) { sum += m; if (m > max) max = m; }
        Console.WriteLine("Sum " + sum + ", average " + (double)sum / marks.Length + ", max " + max);

        int[] sorted = (int[])marks.Clone();
        Array.Sort(sorted);
        Console.WriteLine("Sorted copy: " + string.Join(" ", sorted) + " | original unchanged: " + string.Join(" ", marks));
        Console.WriteLine("BinarySearch(64) index in sorted copy = " + Array.BinarySearch(sorted, 64));
        Console.WriteLine("LINQ: Min " + marks.Min() + ", Max " + marks.Max() + ", pass count " + marks.Count(x => x >= 40));

        int[,] a = { { 1, 2, 3 }, { 4, 5, 6 } };
        int[,] t = new int[3, 2];
        for (int i = 0; i < a.GetLength(0); i++)
            for (int j = 0; j < a.GetLength(1); j++)
                t[j, i] = a[i, j];
        Console.WriteLine("Rectangular " + a.GetLength(0) + "x" + a.GetLength(1) + "; transpose rows:");
        for (int i = 0; i < t.GetLength(0); i++) Console.WriteLine("  " + t[i, 0] + " " + t[i, 1]);

        int[][] tri = new int[4][];
        for (int i = 0; i < tri.Length; i++)
        {
            tri[i] = new int[i + 1];
            tri[i][0] = tri[i][i] = 1;
            for (int j = 1; j < i; j++) tri[i][j] = tri[i - 1][j - 1] + tri[i - 1][j];
        }
        Console.WriteLine("Jagged Pascal triangle:");
        foreach (int[] row in tri) Console.WriteLine("  " + string.Join(" ", row));

        int[] alias = marks;           // copies the reference, not the data
        alias[0] = 100;
        Console.WriteLine("marks[0] after alias[0] = 100: " + marks[0]);
    }
}
```
```output
Length 5, first 72, last 64
Sum 320, average 64, max 91
Sorted copy: 38 55 64 72 91 | original unchanged: 72 55 91 38 64
BinarySearch(64) index in sorted copy = 2
LINQ: Min 38, Max 91, pass count 4
Rectangular 2x3; transpose rows:
  1 4
  2 5
  3 6
Jagged Pascal triangle:
  1
  1 1
  1 2 1
  1 3 3 1
marks[0] after alias[0] = 100: 100
```

::: note Index and range operators (C# 8 and later)
`marks[^1]` is the last element and `marks[1..3]` is a slice of two elements (a new array). The book's checking tool compiles C# 7, so these two lines are shown but not run: `int last = marks[^1]; int[] middle = marks[1..4];`.
:::

## 2.8 Variables and parameters

### Variables and scope

A **variable** is a named storage location of a given type. A local variable exists from its declaration to the end of the block `{ }` that contains it; a name cannot be reused for another local variable in an enclosing scope (C# forbids shadowing of locals, unlike C). Local variables must be assigned before use (definite assignment); fields get default values automatically. Kinds of variable: local variables, parameters, instance fields, static fields and array elements.

### Passing arguments

By default C# passes arguments **by value**: the method receives a copy. For a reference type the copy is a copy of the *reference*, so the method can change the object's contents but cannot make the caller's variable refer to a different object.

| Modifier | At the call | Effect | Must be assigned |
|---|---|---|---|
| (none) | `F(x)` | a copy of the value (or reference) | before the call |
| `ref` | `F(ref x)` | an alias of the caller's variable: reads and writes it | before the call |
| `out` | `F(out x)` | an alias used to return a value; the method must assign it | by the method, before it returns |
| `in` | `F(in x)` | read-only alias; avoids copying a large struct | before the call |
| `params` | `F(1, 2, 3)` | a variable number of arguments collected in an array | last parameter only |

**Optional parameters** have a default (`void Greet(string name, string title = "Mr")`) and must come after the required ones. **Named arguments** let you pass by name in any order (`Greet(title: "Dr", name: "Rai")`). A **local function** is a method declared inside another method that can use its variables (`int Square(int v) => v * v;` written inside `Main`; the book's C# 7 checker has no local functions, so the program below uses a lambda instead). A **tuple** (`(int min, int max)`) returns several values without `out`.

```csharp
using System;

class ParameterDemo
{
    static void ByValue(int x) { x = 99; }
    static void ByRef(ref int x) { x = 99; }
    static void Split(double amount, out int rupees, out int paisa)
    {
        rupees = (int)amount;
        paisa = (int)Math.Round((amount - rupees) * 100);
    }
    static void Swap(ref int a, ref int b) { int t = a; a = b; b = t; }
    static int Total(params int[] values)
    {
        int sum = 0;
        foreach (int v in values) sum += v;
        return sum;
    }
    static string Greet(string name, string title = "Mr", int times = 1)
    {
        string s = "";
        for (int i = 0; i < times; i++) s += "Hello, " + title + " " + name + ". ";
        return s.Trim();
    }
    static (int min, int max) Range(int[] a)
    {
        int lo = a[0], hi = a[0];
        foreach (int v in a) { if (v < lo) lo = v; if (v > hi) hi = v; }
        return (lo, hi);
    }
    static void Rename(int[] a) { a[0] = -1; a = new int[] { 7, 7, 7 }; }   // second line affects only the copy of the reference

    static void Main()
    {
        int n = 5;
        ByValue(n); Console.WriteLine("after ByValue: " + n);
        ByRef(ref n); Console.WriteLine("after ByRef: " + n);
        int r, p;
        Split(125.75, out r, out p);
        Console.WriteLine("125.75 = Rs " + r + " and " + p + " paisa");
        int x = 1, y = 2; Swap(ref x, ref y); Console.WriteLine("swap: x = " + x + ", y = " + y);
        Console.WriteLine("Total() = " + Total() + ", Total(4, 5, 6) = " + Total(4, 5, 6));
        Console.WriteLine(Greet("Rai"));
        Console.WriteLine(Greet(title: "Dr", name: "Sharma", times: 2));
        var range = Range(new[] { 14, 3, 27, 9 });
        Console.WriteLine("Range: " + range.min + " to " + range.max);
        int[] data = { 10, 20, 30 };
        Rename(data);
        Console.WriteLine("data[0] = " + data[0] + " (contents changed), data.Length = " + data.Length + " (reference not replaced)");
        Func<int, int> square = v => v * v;       // a lambda (Unit 4); a local function is shown below
        Console.WriteLine("square(9) = " + square(9));
    }
}
```
```output
after ByValue: 5
after ByRef: 99
125.75 = Rs 125 and 75 paisa
swap: x = 2, y = 1
Total() = 0, Total(4, 5, 6) = 15
Hello, Mr Rai.
Hello, Dr Sharma. Hello, Dr Sharma.
Range: 3 to 27
data[0] = -1 (contents changed), data.Length = 3 (reference not replaced)
square(9) = 81
```

## 2.9 Statements

A **statement** is a unit of execution. C# groups them as declaration, expression, selection, iteration and jump statements. A **block** `{ ... }` groups several statements into one.

### Declaration and expression statements

`int total = 0;` declares (and here initialises) a variable; `const int Max = 10;` declares a constant. An *expression statement* is an assignment, increment, method call, `new` or `await`: `total += 5;`, `Console.WriteLine(x);`. An expression such as `x + 1;` alone is not a legal statement.

### Selection statements

```csharp
// noexec
if (mark >= 80) grade = "Distinction";
else if (mark >= 60) grade = "First";
else if (mark >= 40) grade = "Pass";
else grade = "Fail";
```

The condition must be a `bool`; `if (x = 5)` is a compile error, which removes a classic C bug. The `switch` statement chooses among constant cases. Each case section must end with `break`, `return`, `throw`, `continue` or `goto`; **fall-through is not allowed** except when several labels share one section. A `case` can use patterns and `when` guards, and the `default` section handles all the rest.

```csharp
// noexec
// C# 8 switch expression, not run by the book's C# 7 checker
string kind = day switch
{
    "Sat" => "Holiday",
    "Sun" or "Mon" => "Weekend or start of week",
    _ => "Working day"
};
```

### Iteration statements

| Statement | Use | Remarks |
|---|---|---|
| `for (init; test; step)` | known number of repetitions | all three parts optional; `for (;;)` loops forever |
| `while (test)` | repeat while true; test first | may run zero times |
| `do { } while (test);` | test last | runs at least once |
| `foreach (T x in collection)` | every element of an array or collection | loop variable is read-only; changing the collection inside the loop throws |

### Jump statements

`break` leaves the nearest loop or `switch`; `continue` skips to the next iteration; `return` leaves the method (with a value if it is not `void`); `goto label;` jumps to a label (rarely justified, but `goto case` in `switch` is legal); `throw` raises an exception (Unit 4).

```csharp
using System;

class StatementDemo
{
    static string Classify(int mark)
    {
        if (mark < 0 || mark > 100) return "Invalid";
        if (mark >= 80) return "Distinction";
        if (mark >= 60) return "First";
        if (mark >= 40) return "Pass";
        return "Fail";
    }

    static void Main()
    {
        foreach (int m in new[] { 91, 67, 45, 12, 120 }) Console.WriteLine(m + " -> " + Classify(m));

        for (int d = 1; d <= 7; d++)
        {
            switch (d)
            {
                case 6: Console.WriteLine("day 6: Saturday (holiday)"); break;
                case 1:
                case 7: Console.WriteLine("day " + d + ": start or end of the week"); break;
                default: continue;
            }
        }

        int n = 5, fact = 1;
        while (n > 1) fact *= n--;
        Console.WriteLine("5! = " + fact);

        int digits = 0, number = 70215;
        do { digits++; number /= 10; } while (number > 0);
        Console.WriteLine("70215 has " + digits + " digits");

        Console.Write("Primes below 30:");
        for (int i = 2; i < 30; i++)
        {
            bool prime = true;
            for (int j = 2; j * j <= i; j++)
                if (i % j == 0) { prime = false; break; }
            if (prime) Console.Write(" " + i);
        }
        Console.WriteLine();

        for (int i = 1; i <= 3; i++)
            Console.WriteLine(new string('*', i).PadLeft(3));

        int found = -1;
        int[,] table = { { 3, 8 }, { 5, 9 }, { 2, 7 } };
        for (int i = 0; i < 3 && found < 0; i++)
            for (int j = 0; j < 2; j++)
                if (table[i, j] == 9) { found = i * 10 + j; goto done; }
    done:
        Console.WriteLine("9 found at row " + found / 10 + ", column " + found % 10);
    }
}
```
```output
91 -> Distinction
67 -> First
45 -> Pass
12 -> Fail
120 -> Invalid
day 1: start or end of the week
day 6: Saturday (holiday)
day 7: start or end of the week
5! = 120
70215 has 5 digits
Primes below 30: 2 3 5 7 11 13 17 19 23 29
  *
 **
***
9 found at row 1, column 1
```

## 2.10 Namespaces

A **namespace** groups related types and prevents name clashes: your `Student` class in `NepalCollege.Records` is a different type from someone else's `Student` in `Library.Members`. The full name of a type is its **fully qualified name**, such as `System.Collections.Generic.List<T>`. Namespaces do not affect access rights; they are only a naming and organising tool, and they usually mirror the folder structure.

| Feature | Syntax |
|---|---|
| Declare | `namespace Shop.Billing { class Invoice { } }` (block form), or `namespace Shop.Billing;` at the top of the file (file-scoped, C# 10) |
| Nest | `namespace A { namespace B { } }` is the same as `namespace A.B { }` |
| Import | `using System.Text;` lets you write `StringBuilder` for `System.Text.StringBuilder` |
| Alias | `using Sb = System.Text.StringBuilder;` resolves a clash or shortens a long name |
| Static import | `using static System.Math;` lets you write `Sqrt(2)` instead of `Math.Sqrt(2)` |
| Global using | `global using System.Linq;` applies to the whole project (C# 10; templates add common ones as *implicit usings*) |
| Alias for the root | `global::System.String` skips any local namespace named `System` |

```csharp
using System;
using static System.Math;
using Money = System.Decimal;

namespace NepalCollege.Records
{
    class Student { public string Name = "Anita"; }
}

namespace Library.Members
{
    class Student { public string Name = "Binod"; public int Id = 7; }
}

namespace App
{
    using NepalCollege.Records;

    class Program
    {
        static void Main()
        {
            Student s1 = new Student();                       // NepalCollege.Records.Student
            Library.Members.Student s2 = new Library.Members.Student();
            Console.WriteLine(s1.Name + " (" + s1.GetType().FullName + ")");
            Console.WriteLine(s2.Name + " (" + s2.GetType().FullName + ")");
            Console.WriteLine("Sqrt(2) = " + Sqrt(2).ToString("F4") + ", PI = " + PI.ToString("F5"));
            Money fee = 12500.50m;
            Console.WriteLine("Fee alias type: " + fee.GetType().Name);
        }
    }
}
```
```output
Anita (NepalCollege.Records.Student)
Binod (Library.Members.Student)
Sqrt(2) = 1.4142, PI = 3.14159
Fee alias type: Decimal
```

## 2.11 Summary and exercises

A C# program is a set of statements inside methods inside classes inside namespaces. Console programs ask for input; GUI programs react to events. Identifiers are case sensitive and follow PascalCase and camelCase conventions. Types are value types (integral, floating, `decimal`, `bool`, `char`, `struct`, `enum`) or reference types (`string`, arrays, classes); conversions are implicit when safe and explicit otherwise; `checked` turns silent overflow into an exception. Operators follow a precedence table, and `&&`, `||`, `??` and `?.` short-circuit. Strings are immutable (use `StringBuilder` to build). Arrays can be one-dimensional, rectangular or jagged. Arguments are passed by value unless `ref`, `out`, `in` or `params` is used. Statements are declaration, expression, selection (`if`, `switch`), iteration (`for`, `while`, `do`, `foreach`) and jump (`break`, `continue`, `return`, `goto`, `throw`). Namespaces organise names and `using` imports them.

1. State the rules for identifiers and decide which are legal: `_total`, `2marks`, `Total-Marks`, `@if`, `नाम`.
2. Explain the difference between `const` and `readonly`.
3. List the integral types with sizes and ranges. Which type would you use for the price of an item in rupees, and why?
4. Why does `0.1 + 0.2 == 0.3` evaluate to `false` for `double`? How would you fix a bank program?
5. Explain implicit and explicit conversion, `Convert.ToInt32`, `Parse` and `TryParse` with examples.
6. What are boxing and unboxing? Why are they costly?
7. Evaluate: `int a = 7, b = 2; a / b; a % b; a / (double)b; a++ * --b;`.
8. Differentiate `&&` and `&`. Why is short-circuit evaluation useful?
9. Why are strings immutable? When should `StringBuilder` be preferred?
10. Write a program that counts vowels and consonants in a line entered by the user.
11. Declare a 2 x 3 rectangular array and a jagged array with rows of length 1, 2 and 3. Compare the two forms.
12. Explain `ref`, `out`, `in` and `params` with a short example of each.
13. Explain optional and named arguments. What rule must optional parameters obey?
14. Write a program that reads n and prints the Fibonacci series up to n terms.
15. What is the difference between `break` and `continue`? Does C# allow fall-through between `case` sections?
16. What is a namespace? Show how to resolve a name clash between two `Student` classes.
17. Write a GUI program with a text box and a button that shows the square of the number typed.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain value types and reference types with parameter passing.**

A value-type variable holds its data, so assignment copies the data; a reference-type variable holds a reference, so assignment copies the reference and both variables then refer to one object. When an argument is passed by value, the method receives a copy: for `int` the caller's number is untouched (`ByValue(n)` leaves `n` at 5 in the book's program); for an array the copy of the reference still points to the same array, so `a[0] = -1` is visible to the caller, but `a = new int[3]` inside the method is not. With `ref` the method works on the caller's variable itself, so the caller's `n` becomes 99; `out` is the same but the method must assign the parameter before returning, which suits `TryParse`-style methods.

**Q2 (5 marks). Write a program that reads a line and counts vowels, consonants, digits and spaces.**

```csharp
// stdin: Tribhuvan University 2025
using System;

class Count
{
    static void Main()
    {
        string line = Console.ReadLine();
        int vowels = 0, consonants = 0, digits = 0, spaces = 0;
        foreach (char c in line.ToLower())
        {
            if ("aeiou".IndexOf(c) >= 0) vowels++;
            else if (char.IsLetter(c)) consonants++;
            else if (char.IsDigit(c)) digits++;
            else if (char.IsWhiteSpace(c)) spaces++;
        }
        Console.WriteLine($"Vowels {vowels}, consonants {consonants}, digits {digits}, spaces {spaces}");
    }
}
```
```output
Vowels 7, consonants 12, digits 4, spaces 2
```

Explanation: the line is converted to lower case once, so only five vowels need testing; `IndexOf` returns -1 when the character is not found; the `else if` chain makes sure each character is counted once.

**Q3 (5 marks). Evaluate `int a = 7, b = 2;` for `a / b`, `a % b`, `a / (double)b` and `a++ * --b`.**

`a / b` is integer division, 3. `a % b` is 1. `a / (double)b` converts `b` first, so the division is real: 3.5. In `a++ * --b` the postfix `a++` yields the old value 7 (and `a` becomes 8); the prefix `--b` makes `b` equal to 1 and yields 1; the product is 7.

**Q4 (10 marks). Describe the statements of C# with a program for each category.**

*Declaration:* `int total = 0; const double Rate = 0.13;`. *Expression:* `total += 5;`, `Console.WriteLine(total);`, `list.Add(3);`. *Selection:* `if`/`else if`/`else` chooses by a `bool` condition (the condition must be `bool`, so `if (x = 5)` does not compile); `switch` chooses among constant or pattern cases and does not allow fall-through except for stacked labels. *Iteration:* `for` for counted loops, `while` when the test comes first, `do-while` when the body must run once, `foreach` for every element of a collection (read-only loop variable). *Jump:* `break` leaves the loop or `switch`, `continue` goes to the next iteration, `return` leaves the method, `goto` jumps to a label, `throw` raises an exception.

The program in Section 2.9 combines them: a classification method with `if` and `return`, a `switch` with stacked cases, `while` computing 5! = 120, `do-while` counting five digits in 70215, a nested `for` printing the primes below 30 (2 3 5 7 11 13 17 19 23 29) with `break` out of the inner loop, and a `goto` leaving two nested loops.

**Q5 (10 marks). Distinguish rectangular and jagged arrays and write code that stores and prints Pascal's triangle with four rows.**

A rectangular array `int[,]` is one block of memory with a fixed number of rows and columns; `GetLength(0)` and `GetLength(1)` give the sizes; it is compact and indexed `a[i, j]`. A jagged array `int[][]` is an array whose elements are themselves arrays, so each row is allocated separately and may have a different length; it is indexed `a[i][j]`, is usually faster to access in .NET and suits triangular data. In Section 2.7 the triangle is built with `tri[i] = new int[i + 1]`, setting both ends of each row to 1 and each inner element to the sum of the two elements above it, which prints `1`, `1 1`, `1 2 1`, `1 3 3 1`. A rectangular array would waste the unused upper half.
