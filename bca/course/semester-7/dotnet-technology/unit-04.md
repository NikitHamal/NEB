---
subject: DotNet Technology
grade: BCA Semester 7 (Elective II)
unit: 4
title: Advanced C#
hours: 14
area: BCA 406 · DotNet Technology · Unit 4
---

The last unit joins the language to real applications. A button must call *your* method when it is clicked, so you need a way to pass behaviour around: **delegates**, **events** and **lambda expressions**. Real programs meet bad input, missing files and broken networks, so you need **exception handling**. Data lives in collections and databases, so you need **LINQ** and **ADO.NET**. Finally the web: **ASP.NET** turns the same C# into pages and services. The unit follows the TU outline in that order, and closes with asynchronous programming and the laboratory list.

::: key What this unit gives you
- Delegates (single, multicast, generic `Action`, `Func`, `Predicate`), events and the publisher-subscriber pattern, lambda expressions and closures.
- `try`, `catch`, `finally`, exception hierarchy, custom exceptions, `throw` and `throw;`, exception filters.
- LINQ in query and method syntax: filtering, projection, ordering, grouping, joining, aggregation, deferred execution.
- ADO.NET (connected and disconnected models, parameters, transactions) with a program that really runs against SQLite, and an overview of Entity Framework Core.
- ASP.NET Core: request pipeline, middleware, MVC, Razor Pages, minimal APIs, dependency injection, and the older Web Forms controls.
- `async` and `await`, and a mapping of the laboratory work to sections of this book.
:::

## 4.1 Delegates

A **delegate** is a type-safe object that refers to a method. If a class is the blueprint for objects, a delegate type is the blueprint for *methods with a certain signature*: it fixes the parameter types and the return type, and any method with that signature can be stored in a delegate variable, passed to another method and called later. In C terms it is a function pointer with type checking and an object attached.

Using a delegate takes three steps: declare the delegate type, create an instance that points to a method, and invoke it.

```csharp
using System;

delegate int Operation(int a, int b);                 // 1. declare: any method taking two ints and returning int

class Program
{
    static int Add(int a, int b) { return a + b; }
    static int Multiply(int a, int b) { return a * b; }

    static void Apply(Operation op, int x, int y)       // a method that receives behaviour
    {
        Console.WriteLine("result = " + op(x, y));
    }

    static void Main()
    {
        Operation op = new Operation(Add);               // 2. create: point at Add
        Console.WriteLine("op(3, 4) = " + op(3, 4));     // 3. invoke
        op = Multiply;                                   // method group conversion
        Console.WriteLine("op(3, 4) = " + op.Invoke(3, 4));
        Apply(Add, 10, 5);
        Apply(Multiply, 10, 5);
        Apply(delegate (int a, int b) { return a - b; }, 10, 5);     // anonymous method
        Apply((a, b) => a % b, 10, 5);                               // lambda (Section 4.3)
    }
}
```
```output
op(3, 4) = 7
op(3, 4) = 12
result = 15
result = 50
result = 5
result = 0
```

### Multicast delegates

A delegate instance can refer to **several** methods at once. `+=` (or `Delegate.Combine`) appends a method and `-=` removes one; calling the delegate runs them in the order added. The result of a multicast delegate with a return value is the value of the **last** method, so multicast delegates are normally `void`.

### Built-in generic delegates

You rarely declare your own delegate type. .NET provides generic ones:

| Delegate | Signature | Use |
|---|---|---|
| `Action`, `Action<T>`, `Action<T1,T2>`, ... | `void (...)` | code that does something and returns nothing |
| `Func<TResult>`, `Func<T,TResult>`, ... | `TResult (...)` (last type parameter is the result) | code that computes a value |
| `Predicate<T>` | `bool (T)` | a test (used by `List<T>.FindAll`) |
| `Comparison<T>` | `int (T, T)` | ordering (used by `List<T>.Sort`) |
| `EventHandler`, `EventHandler<TEventArgs>` | `void (object sender, EventArgs e)` | events (Section 4.2) |

```csharp
using System;
using System.Collections.Generic;

class Program
{
    static void Log(string m) { Console.WriteLine("  LOG: " + m); }
    static void Audit(string m) { Console.WriteLine("  AUDIT: " + m.ToUpper()); }

    static void Main()
    {
        Action<string> notify = Log;
        notify += Audit;                                  // multicast: both run, in order
        Console.WriteLine("Two subscribers (" + notify.GetInvocationList().Length + "):");
        notify("fee paid");
        notify -= Log;
        Console.WriteLine("After removing Log:");
        notify("result published");

        Func<double, double, double> hyp = (a, b) => Math.Sqrt(a * a + b * b);
        Console.WriteLine("Func hypotenuse(3, 4) = " + hyp(3, 4));

        List<int> marks = new List<int> { 35, 62, 48, 91, 27, 74 };
        Predicate<int> passed = m => m >= 40;
        Console.WriteLine("Passed: " + string.Join(" ", marks.FindAll(passed)));
        marks.Sort((x, y) => y.CompareTo(x));             // Comparison<int>: descending
        Console.WriteLine("Descending: " + string.Join(" ", marks));

        Func<int, int>[] steps = { x => x + 1, x => x * 2, x => x - 3 };       // an array of behaviours
        int value = 5;
        foreach (Func<int, int> step in steps) value = step(value);
        Console.WriteLine("(5 + 1) * 2 - 3 = " + value);
    }
}
```
```output
Two subscribers (2):
  LOG: fee paid
  AUDIT: FEE PAID
After removing Log:
  AUDIT: RESULT PUBLISHED
Func hypotenuse(3, 4) = 5
Passed: 62 48 91 74
Descending: 91 74 62 48 35 27
(5 + 1) * 2 - 3 = 9
```

Delegates make **callbacks** and **strategy** patterns trivial: a sorting routine receives the comparison, a button receives the click handler, a retry helper receives the operation to retry. They are the foundation of events and LINQ.

## 4.2 Events

An **event** is a delegate-based notification. The class that raises the event is the **publisher**; classes that react are **subscribers**. The publisher exposes `public event EventHandler<T> Name;`, and subscribers attach handlers with `+=` and detach with `-=`. The keyword `event` restricts outsiders: they can only subscribe and unsubscribe, while only the publisher can *raise* (invoke) the event. A plain public delegate field would let anyone invoke or overwrite it.

The convention for the signature is `void Handler(object sender, EventArgs e)`: `sender` is the publisher; `e` carries data, in a class that derives from `EventArgs`. The publisher raises the event in a protected virtual `OnXxx` method and uses `?.Invoke` so that nothing happens when no one has subscribed.

```csharp
using System;

class FeePaidEventArgs : EventArgs
{
    public string Student { get; private set; }
    public decimal Amount { get; private set; }
    public FeePaidEventArgs(string student, decimal amount) { Student = student; Amount = amount; }
}

class Accounts                                            // publisher
{
    public event EventHandler<FeePaidEventArgs> FeePaid;

    public void Receive(string student, decimal amount)
    {
        Console.WriteLine("Accounts: received " + amount + " from " + student);
        OnFeePaid(new FeePaidEventArgs(student, amount));
    }
    protected virtual void OnFeePaid(FeePaidEventArgs e)
    {
        EventHandler<FeePaidEventArgs> handler = FeePaid;
        if (handler != null) handler(this, e);              // same as FeePaid?.Invoke(this, e)
    }
}

class SmsService                                          // subscriber 1
{
    public void OnFeePaid(object sender, FeePaidEventArgs e) { Console.WriteLine("  SMS to " + e.Student + ": Rs " + e.Amount + " received"); }
}
class Library                                             // subscriber 2
{
    public int Cleared;
    public void Clear(object sender, FeePaidEventArgs e) { Cleared++; Console.WriteLine("  Library: borrowing enabled for " + e.Student); }
}

class Program
{
    static void Main()
    {
        Accounts accounts = new Accounts();
        SmsService sms = new SmsService();
        Library lib = new Library();

        accounts.Receive("Anita", 5000);                      // nobody subscribed: no handler runs
        accounts.FeePaid += sms.OnFeePaid;
        accounts.FeePaid += lib.Clear;
        accounts.FeePaid += (s, e) => Console.WriteLine("  Lambda handler: " + (e.Amount >= 10000 ? "large payment" : "regular payment"));
        accounts.Receive("Bikash", 12500);
        accounts.FeePaid -= sms.OnFeePaid;
        accounts.Receive("Chandra", 4000);
        Console.WriteLine("Library cleared " + lib.Cleared + " students");
    }
}
```
```output
Accounts: received 5000 from Anita
Accounts: received 12500 from Bikash
  SMS to Bikash: Rs 12500 received
  Library: borrowing enabled for Bikash
  Lambda handler: large payment
Accounts: received 4000 from Chandra
  Library: borrowing enabled for Chandra
  Lambda handler: regular payment
Library cleared 2 students
```

**GUI events.** In Windows Forms, `button.Click += OnAddClick;` is exactly this mechanism; the framework is the publisher that raises `Click` from its message loop (Section 2.1). WPF and ASP.NET Web Forms controls follow the same convention (`OnClick`, `TextChanged`). In the designer, double-clicking a button writes the `+=` line and an empty handler for you.

::: note Event versus delegate, in one table
| | public delegate field | `event` |
|---|---|---|
| Outsider can invoke | yes | **no** |
| Outsider can replace all handlers with `=` | yes | **no**, only `+=` and `-=` |
| Typical use | callbacks passed as parameters | notifications from an object |
:::

## 4.3 Lambda expressions

A **lambda expression** is a short, nameless function written with the lambda operator `=>` ("goes to"). It can be assigned to a delegate or passed wherever a delegate is expected.

| Form | Example |
|---|---|
| Expression lambda | `x => x * x` or `(a, b) => a + b` |
| Statement lambda | `x => { if (x < 0) return 0; return x; }` |
| No parameters | `() => Console.WriteLine("hi")` |
| Typed parameters | `(int a, int b) => a + b` |
| Discards and static lambdas (C# 9) | `(_, _) => 0`, `static x => x + 1` |

The compiler infers the parameter types from the delegate it is converted to. Behind the scenes it creates a method (and, when variables are captured, a hidden class). A lambda can also be converted to an **expression tree** (`Expression<Func<int,int>>`), a data structure describing the code instead of compiled code; Entity Framework and LINQ providers translate such trees to SQL.

### Closures

A lambda can use local variables of the enclosing method. It **captures the variable itself**, not a copy of its value at that moment, so the variable lives as long as the lambda does and later changes are seen. This is a **closure**.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static Func<int> MakeCounter()
    {
        int count = 0;                                    // captured; survives after MakeCounter returns
        return () => ++count;
    }

    static void Main()
    {
        Func<int, int> square = x => x * x;
        Func<int, int, int> add = (a, b) => a + b;
        Action hello = () => Console.WriteLine("Hello from a lambda");
        Func<int, int> clamp = x => { if (x < 0) return 0; if (x > 100) return 100; return x; };
        hello();
        Console.WriteLine("square(7) = " + square(7) + ", add(2, 3) = " + add(2, 3) + ", clamp(150) = " + clamp(150) + ", clamp(-9) = " + clamp(-9));

        Func<int> c1 = MakeCounter(), c2 = MakeCounter();
        Console.WriteLine("c1: " + c1() + " " + c1() + " " + c1() + "   c2: " + c2() + "  (each closure has its own count)");

        int threshold = 50;
        Func<int, bool> aboveLimit = m => m > threshold;
        Console.WriteLine("60 above limit: " + aboveLimit(60));
        threshold = 70;                                   // the lambda sees the changed variable
        Console.WriteLine("60 above limit after the limit becomes 70: " + aboveLimit(60));

        var names = new List<string> { "Ram", "Sita", "Bikash", "Gita", "Anil" };
        var result = names.Where(n => n.Length <= 4).OrderBy(n => n).Select(n => n.ToUpper());
        Console.WriteLine(string.Join(", ", result));
        var actions = new List<Action>();
        for (int i = 0; i < 3; i++) { int copy = i; actions.Add(() => Console.Write(copy + " ")); }
        foreach (Action a in actions) a();
        Console.WriteLine("(a fresh copy per iteration, so 0 1 2 and not 3 3 3)");
    }
}
```
```output
Hello from a lambda
square(7) = 49, add(2, 3) = 5, clamp(150) = 100, clamp(-9) = 0
c1: 1 2 3   c2: 1  (each closure has its own count)
60 above limit: True
60 above limit after the limit becomes 70: False
ANIL, GITA, RAM, SITA
0 1 2 (a fresh copy per iteration, so 0 1 2 and not 3 3 3)
```

## 4.4 Exception handling

An **exception** is an object that represents an error found at run time: a missing file, a bad number, a null reference, a network failure. When code detects the problem it **throws** the exception; the runtime unwinds the call stack looking for a **handler** (`catch` block) that accepts that type. If none is found the program ends with an unhandled-exception message. Exceptions separate the normal path of a method from its error handling, instead of the C style of checking a return code after every call.

### `try`, `catch`, `finally`

```csharp
// noexec
try
{
    // code that may throw
}
catch (SpecificException ex) when (ex.Code == 404)   // optional filter
{
    // handle this one
}
catch (Exception ex)                                  // more general types last
{
    // handle everything else
}
finally
{
    // always runs: release resources
}
```

Rules to remember: catch blocks are tested **in order**, so list the most specific type first (a general `catch (Exception)` before a specific one is a compile error); a `try` needs at least one `catch` or a `finally`; the `finally` block runs whether or not an exception occurred, and even when the `try` block does `return`; `using` is shorthand for `try`/`finally` with `Dispose()`.

### The exception hierarchy

All exceptions derive from `System.Exception`. Two branches matter: `SystemException` (thrown by the runtime) and `ApplicationException` (an old base for custom exceptions, no longer recommended; derive from `Exception` directly).

| Exception | Thrown when |
|---|---|
| `ArgumentException`, `ArgumentNullException`, `ArgumentOutOfRangeException` | a method receives a bad argument |
| `InvalidOperationException` | the object is in the wrong state (for example `Pop` on an empty stack) |
| `NullReferenceException` | a member is used through a `null` reference |
| `IndexOutOfRangeException` | an index is outside an array |
| `InvalidCastException` | an invalid cast or unboxing |
| `FormatException` | `int.Parse("abc")` |
| `OverflowException` | arithmetic overflow inside `checked`, or a conversion that does not fit |
| `DivideByZeroException` | integer division by zero |
| `KeyNotFoundException` | a dictionary key is missing |
| `FileNotFoundException`, `DirectoryNotFoundException`, `IOException` | file system problems |
| `NotImplementedException`, `NotSupportedException` | placeholders and unsupported operations |
| `OutOfMemoryException`, `StackOverflowException` | resources exhausted (the second cannot be caught) |

Useful members of every exception: `Message` (text), `StackTrace`, `InnerException` (the exception that caused this one), `Data` and `Source`.

### Throwing, rethrowing and custom exceptions

`throw new ArgumentNullException(nameof(name));` raises an exception. Inside a `catch`, **`throw;`** rethrows the *same* exception and keeps its original stack trace, whereas `throw ex;` resets the trace and hides where the error began; never write it. To translate a low-level error into a meaningful one, wrap it: `throw new FeeException("Payment failed", ex);` so the cause is kept in `InnerException`. A **custom exception** has a name ending in `Exception`, derives from `Exception` and offers the three standard constructors.

```csharp
using System;
using System.IO;

class InsufficientFundsException : Exception
{
    public decimal Shortfall { get; private set; }
    public InsufficientFundsException(string message, decimal shortfall) : base(message) { Shortfall = shortfall; }
}

class Wallet
{
    public decimal Balance { get; private set; }
    public Wallet(decimal balance) { Balance = balance; }
    public void Pay(decimal amount)
    {
        if (amount <= 0) throw new ArgumentOutOfRangeException("amount", "must be positive");
        if (amount > Balance) throw new InsufficientFundsException("Balance is too low", amount - Balance);
        Balance -= amount;
    }
}

class Program
{
    static void Parse(string text)
    {
        try
        {
            int n = int.Parse(text);
            Console.WriteLine("  parsed " + n + ", 100 / n = " + 100 / n);
        }
        catch (FormatException) { Console.WriteLine("  '" + text + "' is not a number"); }
        catch (DivideByZeroException) { Console.WriteLine("  cannot divide by zero"); }
        catch (OverflowException) { Console.WriteLine("  '" + text + "' is too large for int"); }
        finally { Console.WriteLine("  (finally: done with '" + text + "')"); }
    }

    static string Load(string path)
    {
        try { return File.ReadAllText(path); }
        catch (FileNotFoundException ex)
        {
            throw new InvalidOperationException("Configuration could not be loaded", ex);   // wrap and keep the cause
        }
    }

    static int FinallyWins()
    {
        try { return 1; }
        finally { Console.WriteLine("  finally runs before the method returns"); }
    }

    static void Main()
    {
        foreach (string s in new[] { "25", "abc", "0", "99999999999" }) Parse(s);

        Wallet w = new Wallet(500);
        try { w.Pay(800); }
        catch (InsufficientFundsException e) { Console.WriteLine("Payment failed: " + e.Message + " by Rs " + e.Shortfall); }

        try { Load("no-such-file.cfg"); }
        catch (InvalidOperationException e) { Console.WriteLine(e.Message + "; cause: " + e.InnerException.GetType().Name); }

        Console.WriteLine("FinallyWins returned " + FinallyWins());

        try
        {
            try { throw new ArgumentException("inner problem"); }
            catch (ArgumentException) { Console.WriteLine("  inner handler logs and rethrows"); throw; }
        }
        catch (Exception e) { Console.WriteLine("  outer handler got " + e.GetType().Name + ": " + e.Message); }
    }
}
```
```output
  parsed 25, 100 / n = 4
  (finally: done with '25')
  'abc' is not a number
  (finally: done with 'abc')
  cannot divide by zero
  (finally: done with '0')
  '99999999999' is too large for int
  (finally: done with '99999999999')
Payment failed: Balance is too low by Rs 300
Configuration could not be loaded; cause: FileNotFoundException
  finally runs before the method returns
FinallyWins returned 1
  inner handler logs and rethrows
  outer handler got ArgumentException: inner problem
```

::: caution Good practice
Catch only what you can handle; never write an empty `catch { }`. Do not use exceptions for ordinary control flow (use `TryParse`, `TryGetValue`, `if`). Release resources with `using` or `finally`. Throw the most specific built-in type that fits, and put the details in the message. Log with the stack trace at the boundary of the application, not at every level.
:::

## 4.5 Introduction to LINQ

**LINQ** (Language Integrated Query) puts a uniform query language inside C#. The same operators work on arrays and lists (*LINQ to Objects*), databases (Entity Framework), XML (`System.Xml.Linq`) and JSON; only the data source changes. It needs `using System.Linq;` and is built on three ideas you already know: generics, lambda expressions and the interface `IEnumerable<T>`, together with **extension methods** (Section 3.6), since `Where`, `Select` and the rest are extension methods of `IEnumerable<T>`.

There are two equivalent syntaxes. **Query syntax** looks like SQL and the compiler translates it into **method syntax**:

```csharp
// noexec
var q1 = from s in students where s.Marks >= 40 orderby s.Marks descending select s.Name;   // query syntax
var q2 = students.Where(s => s.Marks >= 40).OrderByDescending(s => s.Marks).Select(s => s.Name); // method syntax
```

### The main operators

| Operation | Operators | Notes |
|---|---|---|
| Filter | `Where` | keeps elements for which the predicate is true |
| Project | `Select`, `SelectMany` | transforms each element; `SelectMany` flattens |
| Order | `OrderBy`, `OrderByDescending`, `ThenBy`, `Reverse` | stable sort |
| Group | `GroupBy` | each group has a `Key` and the elements |
| Join | `Join`, `GroupJoin` | like SQL inner join and left join |
| Aggregate | `Count`, `Sum`, `Min`, `Max`, `Average`, `Aggregate` | one value |
| Quantifiers | `Any`, `All`, `Contains` | `bool` |
| Element | `First`, `FirstOrDefault`, `Single`, `Last`, `ElementAt` | `First` throws if nothing matches; `FirstOrDefault` returns the default value |
| Partition | `Take`, `Skip`, `TakeWhile`, `SkipWhile` | paging |
| Set | `Distinct`, `Union`, `Intersect`, `Except` | |
| Conversion | `ToList`, `ToArray`, `ToDictionary` | run the query now and store the result |

### Deferred execution

A query that returns `IEnumerable<T>` does **not run when you write it**; it runs when you enumerate it (`foreach`, `ToList()`, `Count()`). The query holds the recipe, so if the source changes before enumeration, the result reflects the change, and enumerating twice runs the recipe twice. Operators that return one value (`Count`, `Sum`, `First`) and conversions (`ToList`) execute immediately.

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Student
{
    public string Name; public string Program; public int Marks;
    public Student(string n, string p, int m) { Name = n; Program = p; Marks = m; }
}

class Program
{
    static void Main()
    {
        var students = new List<Student>
        {
            new Student("Anita", "BCA", 86), new Student("Bikash", "BCA", 52), new Student("Chandra", "BIT", 67),
            new Student("Dipesh", "BIT", 38), new Student("Esha", "BCA", 91), new Student("Firoz", "BBA", 74)
        };

        var toppers = from s in students where s.Marks >= 60 orderby s.Marks descending select s.Name + " (" + s.Marks + ")";
        Console.WriteLine("Query syntax:  " + string.Join(", ", toppers));
        Console.WriteLine("Method syntax: " + string.Join(", ", students.Where(s => s.Marks >= 60).OrderByDescending(s => s.Marks).Select(s => s.Name)));

        Console.WriteLine("Count " + students.Count + ", Average " + students.Average(s => s.Marks).ToString("F2") + ", Max " + students.Max(s => s.Marks) + ", Passed " + students.Count(s => s.Marks >= 40));
        Console.WriteLine("Any failing: " + students.Any(s => s.Marks < 40) + ", All above 30: " + students.All(s => s.Marks > 30));
        Console.WriteLine("First BIT: " + students.First(s => s.Program == "BIT").Name + ", Single Esha: " + students.Single(s => s.Name == "Esha").Marks);
        Console.WriteLine("Nobody named Zed: " + (students.FirstOrDefault(s => s.Name == "Zed") == null));

        Console.WriteLine("Group by program:");
        foreach (var g in students.GroupBy(s => s.Program).OrderBy(g => g.Key))
            Console.WriteLine("  " + g.Key + ": " + g.Count() + " students, average " + g.Average(s => s.Marks).ToString("F1") + " -> " + string.Join(", ", g.Select(s => s.Name)));

        var fees = new[] { new { Program = "BCA", Fee = 90000 }, new { Program = "BIT", Fee = 95000 } };
        var joined = from s in students join f in fees on s.Program equals f.Program select s.Name + ":" + f.Fee;
        Console.WriteLine("Join (BBA has no fee row, so Firoz drops out): " + string.Join(" ", joined));

        Console.WriteLine("Page 2 (size 2): " + string.Join(", ", students.OrderBy(s => s.Name).Skip(2).Take(2).Select(s => s.Name)));
        Console.WriteLine("Distinct programs: " + string.Join(", ", students.Select(s => s.Program).Distinct()));

        var live = students.Where(s => s.Marks >= 90);          // nothing runs yet
        students.Add(new Student("Gita", "BCA", 95));            // source changes before enumeration
        Console.WriteLine("Deferred: " + string.Join(", ", live.Select(s => s.Name)) + "  (Gita was added after the query was written)");
        var snapshot = students.Where(s => s.Marks >= 90).ToList();   // executes now
        students.Add(new Student("Hari", "BCA", 99));
        Console.WriteLine("ToList snapshot has " + snapshot.Count + " items, a live query would now have " + students.Count(s => s.Marks >= 90));
    }
}
```
```output
Query syntax:  Esha (91), Anita (86), Firoz (74), Chandra (67)
Method syntax: Esha, Anita, Firoz, Chandra
Count 6, Average 68.00, Max 91, Passed 5
Any failing: True, All above 30: True
First BIT: Chandra, Single Esha: 91
Nobody named Zed: True
Group by program:
  BBA: 1 students, average 74.0 -> Firoz
  BCA: 3 students, average 76.3 -> Anita, Bikash, Esha
  BIT: 2 students, average 52.5 -> Chandra, Dipesh
Join (BBA has no fee row, so Firoz drops out): Anita:90000 Bikash:90000 Chandra:95000 Dipesh:95000 Esha:90000
Page 2 (size 2): Chandra, Dipesh
Distinct programs: BCA, BIT, BBA
Deferred: Esha, Gita  (Gita was added after the query was written)
ToList snapshot has 2 items, a live query would now have 3
```

