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

## 4.6 Working with databases: ADO.NET

**ADO.NET** is the part of the base class library (`System.Data`) that lets C# talk to relational databases. It is built in two layers. The **data providers** are driver classes written for one product: `Microsoft.Data.SqlClient` for SQL Server, `Npgsql` for PostgreSQL, `MySqlConnector` for MySQL, `Microsoft.Data.Sqlite` for SQLite, and the older `System.Data.OleDb`. Each provider supplies the same four kinds of class, with a prefix that names the product:

| Core object | Role | SQL Server | SQLite |
|---|---|---|---|
| **Connection** | opens a session to the database using a *connection string* | `SqlConnection` | `SqliteConnection` |
| **Command** | holds a SQL statement or stored-procedure name and its parameters | `SqlCommand` | `SqliteCommand` |
| **DataReader** | a forward-only, read-only, fast stream of rows from a query | `SqlDataReader` | `SqliteDataReader` |
| **DataAdapter** | fills a `DataSet` from the database and sends changes back | `SqlDataAdapter` | (not in `Microsoft.Data.Sqlite`) |

The provider-independent layer contains the **DataSet** and **DataTable**, an in-memory copy of tables, rows, columns, constraints and relations that is independent of any database.

```svgfig label="4.1" caption="ADO.NET architecture. The connected model (top path) streams rows with a DataReader while the connection stays open. The disconnected model (bottom path) uses a DataAdapter to fill a DataSet, closes the connection, works on the copy, and later pushes the changes back."
f = Fig(620, 230)
f.box(10, 80, 100, 56, "C# application", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(160, 14, 120, 40, "Command\n(SQL + parameters)", fill=SAND, stroke=AMBER, size=9.5)
f.box(160, 160, 120, 40, "DataAdapter\n(Fill / Update)", fill=SAND, stroke=AMBER, size=9.5)
f.box(325, 80, 110, 56, "Connection\n(connection string)", fill=MINT, stroke=TEAL, size=10)
f.box(490, 80, 120, 56, "Database\nSQL Server,\nSQLite, ...", fill=SOFT, stroke=SLATE, size=10)
f.box(325, 14, 110, 40, "DataReader\n(forward-only)", fill=SAND, stroke=AMBER, size=9.5)
f.box(325, 160, 110, 40, "DataSet / DataTable\n(in-memory copy)", fill=SAND, stroke=AMBER, size=9)
f.arrow([(110, 96), (135, 96), (135, 34), (160, 34)], color=NAVY)
f.arrow([(110, 120), (135, 120), (135, 180), (160, 180)], color=NAVY)
f.arrow([(280, 34), (300, 34), (300, 100), (325, 100)], color=NAVY)
f.arrow([(280, 180), (300, 180), (300, 120), (325, 120)], color=NAVY)
f.arrow([(435, 108), (490, 108)], color=NAVY, both=True)
f.arrow([(380, 80), (380, 54)], color=TEAL)
f.arrow([(380, 160), (380, 136)], color=TEAL, both=True)
f.text(40, 30, "connected model", size=10, color=TEAL, bold=True, anchor="start")
f.text(40, 216, "disconnected model", size=10, color=TEAL, bold=True, anchor="start")
```

### Connected model

Open the connection, run a command, read, close. The connection is a scarce resource, so open it late, close it early and always use `using`. Four command methods cover the cases:

| Method | Returns | Use |
|---|---|---|
| `ExecuteReader()` | a `DataReader` | `SELECT` with many rows |
| `ExecuteScalar()` | one `object` | `SELECT COUNT(*)`, `SUM`, one value |
| `ExecuteNonQuery()` | number of rows affected | `INSERT`, `UPDATE`, `DELETE`, DDL |

**Always use parameters.** Never build SQL by joining user text: `"... WHERE Name = '" + name + "'"` lets an attacker type `x' OR '1'='1` and read every row (**SQL injection**). A parameterised command sends the text and the values separately, so a value can never become SQL.

A **transaction** groups statements so that they all succeed or all fail (`BeginTransaction`, `Commit`, `Rollback`), which keeps a transfer between two accounts consistent.

The program below runs against an in-memory SQLite database (so nothing needs installing; with Mono the classes live in `Mono.Data.Sqlite`, while on .NET 8 you install the NuGet package `Microsoft.Data.Sqlite` and use `using Microsoft.Data.Sqlite;`, with the same class names and methods). To use SQL Server, replace the namespace and the three class prefixes by `SqlConnection`, `SqlCommand`, `SqlDataReader` and use a connection string such as `Server=.;Database=College;Trusted_Connection=True;TrustServerCertificate=True`.

```csharp
using System;
using System.Data;
using Mono.Data.Sqlite;

class Program
{
    static void Exec(IDbConnection con, string sql)
    {
        using (IDbCommand cmd = con.CreateCommand()) { cmd.CommandText = sql; cmd.ExecuteNonQuery(); }
    }

    static void Main()
    {
        using (SqliteConnection con = new SqliteConnection("Data Source=:memory:"))
        {
            con.Open();
            Exec(con, "CREATE TABLE Student (Id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Program TEXT, Marks INTEGER)");

            // INSERT with parameters, inside a transaction
            using (SqliteTransaction tx = con.BeginTransaction())
            {
                string[] names = { "Anita", "Bikash", "Chandra", "Dipesh" };
                string[] progs = { "BCA", "BCA", "BIT", "BIT" };
                int[] marks = { 86, 52, 67, 38 };
                for (int i = 0; i < names.Length; i++)
                {
                    using (SqliteCommand cmd = new SqliteCommand("INSERT INTO Student (Name, Program, Marks) VALUES (@n, @p, @m)", con, tx))
                    {
                        cmd.Parameters.AddWithValue("@n", names[i]);
                        cmd.Parameters.AddWithValue("@p", progs[i]);
                        cmd.Parameters.AddWithValue("@m", marks[i]);
                        cmd.ExecuteNonQuery();
                    }
                }
                tx.Commit();
            }

            // ExecuteScalar
            using (SqliteCommand cmd = new SqliteCommand("SELECT AVG(Marks) FROM Student", con))
                Console.WriteLine("Average marks: " + Convert.ToDouble(cmd.ExecuteScalar()));

            // ExecuteReader with a parameter
            using (SqliteCommand cmd = new SqliteCommand("SELECT Id, Name, Marks FROM Student WHERE Program = @p ORDER BY Marks DESC", con))
            {
                cmd.Parameters.AddWithValue("@p", "BCA");
                using (SqliteDataReader rd = cmd.ExecuteReader())
                    while (rd.Read())
                        Console.WriteLine("  " + rd.GetInt32(0) + " " + rd["Name"] + " " + rd.GetInt32(2));
            }

            // UPDATE and DELETE: ExecuteNonQuery returns the number of affected rows
            using (SqliteCommand cmd = new SqliteCommand("UPDATE Student SET Marks = Marks + 5 WHERE Marks < 40", con))
                Console.WriteLine("Grace marks given to " + cmd.ExecuteNonQuery() + " student(s)");

            // The injection attempt is just text, so it matches nothing
            using (SqliteCommand cmd = new SqliteCommand("SELECT COUNT(*) FROM Student WHERE Name = @n", con))
            {
                cmd.Parameters.AddWithValue("@n", "x' OR '1'='1");
                Console.WriteLine("Rows matching the injection text: " + cmd.ExecuteScalar());
            }

            // A failed transaction is rolled back
            try
            {
                using (SqliteTransaction tx = con.BeginTransaction())
                {
                    using (SqliteCommand cmd = new SqliteCommand("DELETE FROM Student", con, tx)) Console.WriteLine("Deleting " + cmd.ExecuteNonQuery() + " rows inside the transaction...");
                    throw new InvalidOperationException("simulated failure");
                }
            }
            catch (InvalidOperationException) { Console.WriteLine("failure, transaction not committed (disposing it rolls back)"); }
            using (SqliteCommand cmd = new SqliteCommand("SELECT COUNT(*) FROM Student", con))
                Console.WriteLine("Rows after rollback: " + cmd.ExecuteScalar());
        }
    }
}
```
```output
Average marks: 60.75
  1 Anita 86
  2 Bikash 52
Grace marks given to 1 student(s)
Rows matching the injection text: 0
Deleting 4 rows inside the transaction...
failure, transaction not committed (disposing it rolls back)
Rows after rollback: 4
```

### Disconnected model: DataAdapter, DataSet and DataTable

In the **disconnected** model the adapter opens the connection by itself, copies the query result into a `DataTable` (`adapter.Fill(table)`) and closes the connection. You then browse, sort, filter, add, edit and delete rows in memory (each `DataRow` keeps a `RowState`: `Added`, `Modified`, `Deleted`, `Unchanged`), possibly for a long time and without holding a database session. `adapter.Update(table)` later opens the connection again and sends only the changed rows using the INSERT, UPDATE and DELETE commands, which a `CommandBuilder` can generate. A `DataSet` holds several tables plus `DataRelation` objects (foreign-key like links) and can be written to XML. This model suits desktop and web applications that show data in a grid (`DataGridView`, `GridView`) and scales better, because connections are held only briefly; its price is memory and the risk of conflicting changes by other users (*optimistic concurrency*).

| | Connected (`DataReader`) | Disconnected (`DataAdapter` + `DataSet`) |
|---|---|---|
| Connection | open during the whole read | opened and closed by `Fill` and `Update` |
| Access | forward-only, read-only | random access, editable |
| Memory | one row at a time | whole result in memory |
| Speed | fastest for a single pass | pays for the copy, fast afterwards |
| Updates | by commands you write | `Update` finds changed rows |
| Best for | reports, lookups, large reads | grids, forms, offline editing |

```csharp
using System;
using System.Data;
using Mono.Data.Sqlite;

class Program
{
    static void Main()
    {
        string cs = "Data Source=:memory:";
        using (SqliteConnection con = new SqliteConnection(cs))
        {
            con.Open();
            new SqliteCommand("CREATE TABLE Course (Code TEXT PRIMARY KEY, Title TEXT, Credits INTEGER)", con).ExecuteNonQuery();
            new SqliteCommand("INSERT INTO Course VALUES ('BCA101','Computer Fundamentals',3), ('BCA102','Programming in C',3), ('BCA106','Hardware Workshop',1)", con).ExecuteNonQuery();

            SqliteDataAdapter adapter = new SqliteDataAdapter("SELECT Code, Title, Credits FROM Course", con);
            SqliteCommandBuilder builder = new SqliteCommandBuilder(adapter);     // generates INSERT/UPDATE/DELETE
            DataTable table = new DataTable("Course");
            adapter.Fill(table);                                                  // copy into memory
            Console.WriteLine("Filled " + table.Rows.Count + " rows, columns: " + string.Join(", ", ColumnNames(table)));

            table.Rows[2]["Credits"] = 2;                                         // edit in memory
            table.Rows.Add("BCA151", "Discrete Structure", 3);                    // add in memory
            table.Rows[0].Delete();                                               // delete in memory
            foreach (DataRow r in table.Rows)
                Console.WriteLine("  " + (r.RowState == DataRowState.Deleted ? r["Code", DataRowVersion.Original] : r["Code"]) + " is " + r.RowState);

            Console.WriteLine("Rows in the database before Update: " + new SqliteCommand("SELECT COUNT(*) FROM Course", con).ExecuteScalar());
            int changes = adapter.Update(table);                                  // send only the changed rows
            Console.WriteLine("Update sent " + changes + " changes; rows in the database now: " + new SqliteCommand("SELECT COUNT(*) FROM Course", con).ExecuteScalar());

            DataRow[] threeCredit = table.Select("Credits = 3", "Code DESC");     // filter and sort in memory
            Console.WriteLine("3-credit courses (sorted in memory): " + string.Join(", ", Array.ConvertAll(threeCredit, r => (string)r["Code"])));
            Console.WriteLine("Total credits: " + table.Compute("SUM(Credits)", ""));
        }
    }

    static string[] ColumnNames(DataTable t)
    {
        string[] n = new string[t.Columns.Count];
        for (int i = 0; i < n.Length; i++) n[i] = t.Columns[i].ColumnName;
        return n;
    }
}
```
```output
Filled 3 rows, columns: Code, Title, Credits
  BCA101 is Deleted
  BCA102 is Unchanged
  BCA106 is Modified
  BCA151 is Added
Rows in the database before Update: 3
Update sent 3 changes; rows in the database now: 3
3-credit courses (sorted in memory): BCA151, BCA102
Total credits: 8
```

### Entity Framework Core (overview)

Writing SQL strings and mapping rows to objects by hand is repetitive. **Entity Framework Core (EF Core)** is the **object-relational mapper** of .NET: you write classes (*entities*) and a `DbContext`, and EF Core generates the SQL, tracks changes and maps rows to objects. The query language is LINQ, translated to SQL through expression trees (Section 4.3). Two ways to start: *code first* (write classes, create the database with **migrations**) and *database first* (scaffold classes from an existing database with `dotnet ef dbcontext scaffold`).

```csharp
// noexec
// dotnet add package Microsoft.EntityFrameworkCore.Sqlite
using Microsoft.EntityFrameworkCore;

public class Student { public int Id { get; set; } public string Name { get; set; } public int Marks { get; set; } }

public class CollegeContext : DbContext
{
    public DbSet<Student> Students { get; set; }
    protected override void OnConfiguring(DbContextOptionsBuilder o) => o.UseSqlite("Data Source=college.db");
}

// dotnet ef migrations add Initial ; dotnet ef database update
using var db = new CollegeContext();
db.Students.Add(new Student { Name = "Anita", Marks = 86 });
db.SaveChanges();                                                         // INSERT
var toppers = db.Students.Where(s => s.Marks >= 80).OrderBy(s => s.Name).ToList();   // SELECT ... WHERE ... ORDER BY
```

ADO.NET gives full control and the best raw speed; EF Core gives productivity and type safety. Many applications use EF Core for everyday work and ADO.NET (or the lightweight library Dapper) for heavy reports.

## 4.7 Writing web applications with ASP.NET

**ASP.NET** is the web framework of .NET. A web application receives an **HTTP request** (a method such as GET or POST, a URL, headers and perhaps a body) and returns an **HTTP response** (a status code such as 200 or 404, headers and a body of HTML or JSON). Everything in ASP.NET is a way of organising the code that turns one into the other. There are two generations:

| | ASP.NET (classic, Web Forms and MVC 5) | ASP.NET Core |
|---|---|---|
| Runs on | .NET Framework, Windows, IIS only | modern .NET on Windows, Linux, macOS, containers |
| Server | IIS (`System.Web`) | **Kestrel** (built in), optionally behind IIS, Nginx or Apache |
| Page models | Web Forms (server controls, view state, events), MVC | MVC, **Razor Pages**, **Blazor**, **minimal APIs**, Web API controllers |
| Configuration | `Web.config` | `appsettings.json`, environment variables |
| Status | maintained only; no new features | the framework for all new work |

### The ASP.NET Core application

A minimal application is one file. `WebApplication.CreateBuilder` creates the **host** (configuration, logging, dependency-injection container, Kestrel); `Build()` produces the app; the `Map...` calls define **endpoints**; `Run()` starts listening.

```csharp
// noexec
// dotnet new web -n Hello ; dotnet run
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSingleton<IGreeter, Greeter>();            // register a service (dependency injection)
var app = builder.Build();

app.UseHttpsRedirection();                                     // middleware
app.UseStaticFiles();

app.MapGet("/", () => "Hello, Nepal!");                        // minimal API endpoint
app.MapGet("/hello/{name}", (string name, IGreeter g) => g.Greet(name));   // route value and an injected service
app.MapPost("/students", (Student s) => Results.Created($"/students/{s.Id}", s));  // JSON in, JSON out

app.Run();

public interface IGreeter { string Greet(string name); }
public class Greeter : IGreeter { public string Greet(string name) => $"Namaste, {name}!"; }
public record Student(int Id, string Name, int Marks);
```

### Middleware and the request pipeline

ASP.NET Core processes a request through a chain of **middleware** components. Each one receives the `HttpContext`, may do some work before calling the **next** component, and may do more work after the next one returns. A component may also **short-circuit**: answer at once without calling `next` (authentication failure, a cached page). The order of the `app.Use...` calls is the order of the pipeline, so exception handling comes first and endpoints last. In essence the pipeline is a chain of delegates (Section 4.1): each middleware is a `Func<RequestDelegate, RequestDelegate>`. The program below builds the same idea in a few lines of plain C# so that you can see the order of execution.

```csharp
using System;
using System.Collections.Generic;

delegate string RequestDelegate(string path);

class Pipeline
{
    private List<Func<RequestDelegate, RequestDelegate>> parts = new List<Func<RequestDelegate, RequestDelegate>>();
    public Pipeline Use(Func<string, RequestDelegate, string> middleware)
    {
        parts.Add(next => path => middleware(path, next));
        return this;
    }
    public RequestDelegate Build(RequestDelegate endpoint)
    {
        RequestDelegate app = endpoint;
        for (int i = parts.Count - 1; i >= 0; i--) app = parts[i](app);      // wrap from the last to the first
        return app;
    }
}

class Program
{
    static void Main()
    {
        var pipeline = new Pipeline()
            .Use((path, next) => { Console.WriteLine("  [logging] before " + path); string r = next(path); Console.WriteLine("  [logging] after, response = " + r); return r; })
            .Use((path, next) => path.StartsWith("/admin") ? "401 Unauthorized (short-circuited)" : next(path))
            .Use((path, next) => next(path) + " [gzip]");
        RequestDelegate app = pipeline.Build(path => path == "/" ? "200 Home page" : "404 Not found");

        foreach (string url in new[] { "/", "/missing", "/admin/users" })
        {
            Console.WriteLine("GET " + url);
            Console.WriteLine("-> " + app(url));
        }
    }
}
```
```output
GET /
  [logging] before /
  [logging] after, response = 200 Home page [gzip]
-> 200 Home page [gzip]
GET /missing
  [logging] before /missing
  [logging] after, response = 404 Not found [gzip]
-> 404 Not found [gzip]
GET /admin/users
  [logging] before /admin/users
  [logging] after, response = 401 Unauthorized (short-circuited)
-> 401 Unauthorized (short-circuited)
```

### MVC, Razor Pages and Web API

**MVC (Model-View-Controller)** splits a web application into three roles. The **Model** holds data and business rules (`Student`, validation attributes, EF Core entities). The **View** is a Razor template (`.cshtml`) that mixes HTML with C# using `@` to render the model. The **Controller** is a class whose **action methods** handle requests: it reads input, calls the model, chooses a view and passes it the model. **Routing** maps a URL such as `/Students/Details/5` to the controller `StudentsController`, action `Details`, with `id = 5`, following the default pattern `{controller=Home}/{action=Index}/{id?}`. The benefit is separation of concerns, easy testing of controllers and many views for one model.

```svgfig label="4.2" caption="The MVC request cycle. The router selects a controller action, the action works with the model and returns a view with its data, and the Razor view produces the HTML in the response."
f = Fig(620, 190)
f.box(10, 70, 90, 50, "Browser\nGET /Students/\nDetails/5", fill=BLUE, stroke=NAVY, size=9)
f.box(130, 70, 90, 50, "Routing\nmiddleware", fill=SOFT, stroke=SLATE, size=10)
f.box(250, 20, 130, 50, "StudentsController\nDetails(int id)", fill=SAND, stroke=AMBER, size=9.5)
f.box(250, 120, 130, 50, "Model\nStudent + EF Core", fill=MINT, stroke=TEAL, size=10)
f.box(430, 70, 100, 50, "View\nDetails.cshtml", fill=BLUE, stroke=NAVY, size=10)
f.box(555, 70, 55, 50, "HTML\nresponse", fill=SOFT, stroke=SLATE, size=9)
f.arrow([(100, 95), (130, 95)], color=NAVY)
f.arrow([(220, 95), (235, 95), (235, 45), (250, 45)], color=NAVY)
f.arrow([(315, 70), (315, 120)], color=TEAL, both=True)
f.arrow([(380, 45), (405, 45), (405, 95), (430, 95)], color=NAVY)
f.arrow([(530, 95), (555, 95)], color=NAVY)
f.text(327, 98, "data", size=9.5, color=TEAL, bold=True, anchor="start")
f.text(405, 38, "model", size=9.5, color=NAVY, anchor="start")
```

```csharp
// noexec
// Controllers/StudentsController.cs
public class StudentsController : Controller
{
    private readonly CollegeContext _db;
    public StudentsController(CollegeContext db) => _db = db;          // dependency injection

    public IActionResult Index() => View(_db.Students.OrderBy(s => s.Name).ToList());

    public IActionResult Details(int id)
    {
        var student = _db.Students.Find(id);
        if (student == null) return NotFound();
        return View(student);                                          // passes the model to Details.cshtml
    }

    [HttpPost, ValidateAntiForgeryToken]
    public IActionResult Create(Student s)
    {
        if (!ModelState.IsValid) return View(s);                       // validation attributes were checked
        _db.Add(s); _db.SaveChanges();
        return RedirectToAction(nameof(Index));
    }
}
```

```text
@* Views/Students/Details.cshtml *@
@model Student
<h2>@Model.Name</h2>
<p>Marks: @Model.Marks  (@(Model.Marks >= 40 ? "Pass" : "Fail"))</p>
<a asp-action="Index">Back to the list</a>
```

**Razor Pages** is the page-focused alternative: each page is a `.cshtml` file with a `PageModel` class (`OnGet`, `OnPost`) beside it, which keeps the view and its logic together and suits form-based sites. **Web API controllers** and minimal APIs return JSON instead of HTML for mobile apps and JavaScript front ends. **Blazor** builds interactive web UI in C# instead of JavaScript.

### Dependency injection, configuration and state

**Dependency injection (DI)** is built into the host. A class asks for what it needs in its constructor (`IGreeter`, `CollegeContext`), and the container supplies it. Services are registered with a lifetime: *singleton* (one for the application), *scoped* (one per request, the usual choice for a `DbContext`) or *transient* (new each time). DI keeps classes loosely coupled and testable. **Configuration** comes from `appsettings.json`, environment variables and secrets, merged and read through `IConfiguration`. HTTP is **stateless**, so state across requests is kept in cookies, the **session**, a database or a cache; Web Forms hid this with *view state*, a hidden field that grew large.

### Security basics for every web application

| Threat | Defence in ASP.NET Core |
|---|---|
| SQL injection | parameters or EF Core (Section 4.6) |
| Cross-site scripting (XSS) | Razor HTML-encodes `@` output by default; avoid `@Html.Raw` on user text |
| Cross-site request forgery (CSRF) | anti-forgery tokens (`[ValidateAntiForgeryToken]`) |
| Weak passwords | ASP.NET Core Identity: salted, slow password hashes, lockout, 2FA |
| Plain-text traffic | HTTPS redirection and HSTS |
| Over-posting | bind to a view model, not the entity |

### ASP.NET Web Forms (classic) in brief

Older systems and many textbooks use **Web Forms**: a page is an `.aspx` file of markup with **server controls** (`<asp:TextBox>`, `<asp:Button>`, `<asp:GridView>`) and a *code-behind* class (`.aspx.cs`). The model imitates desktop programming: you double-click a button and write `Button1_Click`. Under the surface the framework keeps control state in a hidden **view state** field and runs a **page life cycle** on every request: `PreInit`, `Init`, `Load`, control events (`Click`), `PreRender`, `Render`, `Unload`. It is covered here because it shows the event idea in a web setting and appears in examination papers. It is Windows-only and has no future development.

```text
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="Demo.Default" %>
<form id="form1" runat="server">
    <asp:TextBox ID="txtMarks" runat="server" />
    <asp:Button ID="btnCheck" runat="server" Text="Check" OnClick="btnCheck_Click" />
    <asp:Label ID="lblResult" runat="server" />
</form>
```

```csharp
// noexec
// Default.aspx.cs (code-behind)
public partial class Default : System.Web.UI.Page
{
    protected void btnCheck_Click(object sender, EventArgs e)
    {
        int marks;
        lblResult.Text = int.TryParse(txtMarks.Text, out marks) ? (marks >= 40 ? "Pass" : "Fail") : "Enter a number";
    }
}
```

## 4.8 Asynchronous programming and files

Waiting for a disk, a database or a web server wastes a thread if the program just blocks. **`async` and `await`** (C# 5) let a method start such an operation, give the thread back to do other work, and **resume after the `await`** when the operation finishes. An `async` method returns `Task` (nothing), `Task<T>` (a result) or `ValueTask<T>`; the compiler turns the method into a state machine. Rules: use `await` instead of `.Result` or `.Wait()` (which can deadlock a UI), name async methods with the suffix `Async`, and pass a `CancellationToken` for long work. A UI thread stays responsive, and a web server serves more requests with the same threads, because no thread sits idle during I/O. (Threads are for CPU-bound parallel work; `Task.Run` moves it off the current thread.)

```csharp
using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

class Program
{
    static async Task<int> FetchMarksAsync(string student, int delayMs, int marks)
    {
        await Task.Delay(delayMs);                         // stands for a database or HTTP call
        Console.WriteLine("  got " + student);
        return marks;
    }

    static async Task RunAsync()
    {
        Stopwatch sw = Stopwatch.StartNew();
        int a = await FetchMarksAsync("Anita", 300, 86);              // one after another: about 300 + 300 ms
        int b = await FetchMarksAsync("Bikash", 300, 52);
        Console.WriteLine("Sequential total " + (a + b) + " took more than 500 ms: " + (sw.ElapsedMilliseconds >= 500));

        sw.Restart();
        Task<int> ta = FetchMarksAsync("Chandra", 300, 67);          // start both, then wait for both
        Task<int> tb = FetchMarksAsync("Dipesh", 300, 38);
        int[] results = await Task.WhenAll(ta, tb);
        Console.WriteLine("Concurrent total " + results.Sum() + " took less than 500 ms: " + (sw.ElapsedMilliseconds < 500));

        string path = Path.Combine(Path.GetTempPath(), "bca-demo.txt");
        File.WriteAllLines(path, new[] { "Anita,86", "Bikash,52", "Chandra,67" });
        string[] lines = File.ReadAllLines(path);
        double avg = lines.Select(l => int.Parse(l.Split(',')[1])).Average();
        Console.WriteLine("Read " + lines.Length + " lines from a file, average mark " + avg.ToString("F2"));
        File.Delete(path);
    }

    static void Main()
    {
        RunAsync().Wait();                                 // a console Main of this era cannot be async; .NET 7+ allows async Task Main
    }
}
```
```output
  got Anita
  got Bikash
Sequential total 138 took more than 500 ms: True
  got Chandra
  got Dipesh
Concurrent total 105 took less than 500 ms: True
Read 3 lines from a file, average mark 68.33
```

For files, use `File.ReadAllText/WriteAllText/ReadAllLines/AppendAllText` for small files, and `StreamReader`/`StreamWriter` inside `using` for large ones; `Path.Combine` builds paths portably; `FileNotFoundException` and `UnauthorizedAccessException` are the usual errors.

## 4.9 Laboratory work

The TU laboratory list is written for C# console or GUI programs. Use this map to find the section, the program and the idea for each experiment:

| Laboratory task | Where in this book |
|---|---|
| Basic language features: variables, operators, control statements, arrays, strings | Unit 2, Sections 2.4 to 2.9 |
| Classes, objects, constructors, properties, indexers | Unit 3, Sections 3.1 to 3.5 |
| Inheritance, abstract classes, interfaces, polymorphism | Unit 3, Sections 3.8 and 3.13 |
| Operator overloading, structs, enums, generics | Unit 3, Sections 3.9, 3.11, 3.14, 3.15 |
| Delegates, events and lambda expressions | Unit 4, Sections 4.1 to 4.3 |
| Exception handling with custom exceptions | Unit 4, Section 4.4 |
| LINQ queries | Unit 4, Section 4.5 |
| Database application (connected and disconnected) and simple ASP.NET page | Unit 4, Sections 4.6 and 4.7 |

::: tip A mini-project that uses everything
Build a *Student Result Manager*. Entities: `Student`, `Subject`, `Result` (classes with properties, one abstract `Person`, an `IReportable` interface). Store the data in SQLite through ADO.NET or EF Core, query toppers and averages with LINQ, raise a `ResultPublished` event that a notifier handles, validate marks with a custom exception, and expose the list in an ASP.NET Core page. Document each design choice in a short report; this is the shape of a good viva.
:::

## 4.10 Summary and exercises

A delegate is a type-safe method reference; multicast delegates call several methods; `Action`, `Func` and `Predicate` cover most needs. Events are protected delegates for the publisher-subscriber pattern. Lambdas are short anonymous functions that capture variables (closures). Exceptions are thrown, propagate up the stack and are handled by `catch`; `finally` and `using` release resources; custom exceptions model domain errors. LINQ queries any `IEnumerable<T>` with deferred execution. ADO.NET offers a connected model (command and reader) and a disconnected model (adapter and `DataSet`); parameters prevent SQL injection and transactions keep data consistent; EF Core maps classes to tables. ASP.NET Core routes HTTP requests through a middleware pipeline to MVC controllers, Razor Pages or minimal APIs, with dependency injection and configuration built in; `async` and `await` keep threads free during I/O.

1. What is a delegate? Declare, instantiate and invoke one. How does a multicast delegate work?
2. Compare `Action`, `Func` and `Predicate` with an example of each.
3. What is an event? How does it differ from a public delegate field? Write a publisher and two subscribers.
4. Explain lambda expressions and closures. What does a lambda capture?
5. What is the output of the loop that stores `() => Console.Write(i)` in a list for `i` from 0 to 2 (a) directly and (b) with `int copy = i`? Explain.
6. Explain `try`, `catch`, `finally` and the order of catch blocks. Does `finally` run if the `try` block returns?
7. Difference between `throw;` and `throw ex;`. Write a custom exception class.
8. List six common exceptions with the situation that causes each.
9. What is LINQ? Write the same query in query syntax and method syntax and explain deferred execution.
10. Write LINQ for: the average mark per program; the top three students; the students whose names start with "A".
11. Explain the ADO.NET architecture with a diagram. Name the core objects of a data provider.
12. Compare the connected and disconnected models. Write code with `SqlConnection`, `SqlCommand` and `SqlDataReader`.
13. What is SQL injection? Show an attack and the defence with parameters.
14. What does a `DataAdapter` do? What are `Fill` and `Update`?
15. What is Entity Framework Core? What is code-first and what is a migration?
16. Explain the ASP.NET Core request pipeline and middleware. Why does the order matter?
17. Explain MVC with a diagram. What are routing, controller, action, model and view?
18. Compare ASP.NET Web Forms and ASP.NET Core.
19. What do `async` and `await` do? Why not call `.Result`?

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain delegates and multicast delegates with an example.**

A delegate is a type that holds a reference to a method with a particular signature, making callbacks type safe. Declaration: `delegate int Operation(int a, int b);` Instantiation: `Operation op = Add;` where `static int Add(int a, int b)`. Invocation: `op(3, 4)` returns 7; the same variable can later refer to `Multiply` and return 12 (Section 4.1). A multicast delegate holds an invocation list built with `+=`; calling it runs every method in the order added, and `-=` removes one. In the logging program, `Action<string> notify = Log; notify += Audit;` printed a line from each method, and after `notify -= Log` only the audit line appeared. Multicast delegates should return `void`, since only the last method's return value survives. Delegates underlie events, lambdas and LINQ.

**Q2 (5 marks). Differentiate an event from a delegate.**

A delegate is a type for methods; an event is a member of a class declared with a delegate type and the `event` keyword. Code outside the publisher can only subscribe (`+=`) and unsubscribe (`-=`); it cannot invoke the event or replace the list with `=`. With a plain public delegate field any code can call it or erase every subscriber. Events therefore protect the publisher and implement the publisher-subscriber pattern: in Section 4.2 `Accounts.FeePaid` notified `SmsService`, `Library` and a lambda, and handlers added later started receiving notifications while removed ones stopped. The convention is `EventHandler<TEventArgs>`, a sender and an `EventArgs` subclass with the data.

**Q3 (5 marks). What is exception handling? Explain `try`, `catch` and `finally`, and write a custom exception.**

Exception handling is the mechanism for detecting and reacting to run-time errors without cluttering the normal logic. Code that may fail is placed in `try`; when an exception is thrown the runtime searches the `catch` blocks in order for the first whose type matches, so specific exceptions come before `Exception`; `finally` always runs, whether or not an exception was thrown, and is used to release resources (file, connection). A custom exception derives from `Exception`: `class InsufficientFundsException : Exception { public decimal Shortfall { get; private set; } public InsufficientFundsException(string m, decimal s) : base(m) { Shortfall = s; } }`. In Section 4.4 paying Rs 800 from a balance of Rs 500 throws it with Shortfall 300, which the caller catches and reports.

**Q4 (10 marks). Explain the ADO.NET architecture, comparing the connected and disconnected models, with code.**

ADO.NET has a data provider layer (Connection, Command, DataReader, DataAdapter) specific to a database, and a provider-independent layer (`DataSet`, `DataTable`, `DataRow`, `DataRelation`). In the connected model a `Connection` is opened, a `Command` runs SQL (`ExecuteReader`, `ExecuteScalar`, `ExecuteNonQuery`) and a forward-only `DataReader` streams rows while the connection stays open; it is fast and uses little memory but is read-only and holds the connection. In the disconnected model a `DataAdapter` opens the connection, executes the `SELECT`, `Fill`s a `DataTable` or `DataSet` and closes the connection; the user edits the in-memory rows (tracked by `RowState`), and `Update` sends only the changed rows back using generated INSERT, UPDATE and DELETE commands. Connected suits reports and lookups; disconnected suits grids, forms and offline work, at the cost of memory and the need to handle concurrency conflicts. Both models must use **parameters** (`@p`), never string concatenation, to prevent SQL injection, and should wrap related changes in a transaction. The programs of Section 4.6 insert four students in a transaction, read the BCA students with a parameter (Anita 86, Bikash 52), show that the text `x' OR '1'='1` matches 0 rows, roll back a failed delete (4 rows remain), and fill, change and update a `Course` table (3 changes sent).

**Q5 (10 marks). Explain the MVC pattern in ASP.NET Core and the request pipeline.**

MVC divides an application into Model (data and business rules), View (Razor templates producing HTML) and Controller (action methods handling requests). A request such as `GET /Students/Details/5` first passes through the middleware pipeline (HTTPS redirection, static files, routing, authentication, authorisation); the order of `app.Use...` calls is the order of execution, and any component may short-circuit, as the `/admin` check did in the Section 4.7 program, which answered `401` without calling the endpoint. Routing matches the URL to `StudentsController.Details(id = 5)`; the framework creates the controller with its dependencies supplied by the dependency-injection container (`CollegeContext`); the action loads the model from the database, returns `View(student)`, and the Razor view renders the HTML, which travels back through the same middleware in reverse order (as `[logging] after` showed). Advantages: separation of concerns, testable controllers, several views for one model, clean URLs. Razor Pages organises the same ideas page by page; Web API controllers and minimal APIs return JSON; model binding and validation attributes check input; `[ValidateAntiForgeryToken]` and Razor's default HTML encoding defend against CSRF and XSS.
