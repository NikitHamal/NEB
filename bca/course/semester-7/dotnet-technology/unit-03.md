---
subject: DotNet Technology
grade: BCA Semester 7 (Elective II)
unit: 3
title: Creating Types in C#
hours: 12
area: BCA 406 · DotNet Technology · Unit 3
---

A college system needs students, teachers, courses and fees. Each is a *type*: it says what data an item has and what it can do. Unit 2 used the types that .NET provides; this unit shows how to make your own. C# gives you classes, structs, interfaces, enumerations and generics. The order follows the TU outline: classes, constructors and deconstructors, the `this` reference, properties, indexers, static members, finalizers, dynamic binding, operator overloading, inheritance, abstract classes, `base`, overloading, the `object` type, structs, access modifiers, interfaces, enums and generics.

::: key What this unit gives you
- Classes and objects, fields, methods, constructors (including chaining), deconstructors and `this`.
- Properties, indexers, static constructors, static classes and finalizers.
- Inheritance, `virtual`, `override`, `abstract`, `sealed`, `base`, and the difference between overloading, overriding and hiding.
- Operator overloading, the members of `System.Object`, structs, access modifiers.
- Interfaces, enumerations and generics with constraints; every program compiled and run.
:::

## 3.1 Classes and objects

A **class** is a reference type that bundles **data members** (fields, properties) and **function members** (methods, constructors, operators, indexers, events). `new` creates an **object** (an *instance*) of the class on the heap and returns a reference to it.

```csharp
using System;

class Student
{
    public string Name;                  // field
    public int Roll;
    private double marks;                // private field: hidden from other classes

    public void SetMarks(double m)       // method
    {
        if (m >= 0 && m <= 100) marks = m;
    }
    public double GetMarks() { return marks; }
    public string Grade()
    {
        if (marks >= 80) return "Distinction";
        if (marks >= 60) return "First";
        return marks >= 40 ? "Pass" : "Fail";
    }
}

class Program
{
    static void Main()
    {
        Student a = new Student();
        a.Name = "Anita"; a.Roll = 1; a.SetMarks(86);
        Student b = new Student { Name = "Bikash", Roll = 2 };    // object initializer
        b.SetMarks(250);                                           // rejected by the check
        Student c = a;                                             // same object, second reference
        c.Name = "Anita Rai";
        Console.WriteLine(a.Name + " " + a.Grade() + " (" + a.GetMarks() + ")");
        Console.WriteLine(b.Name + " " + b.Grade() + " (" + b.GetMarks() + ")");
        Console.WriteLine("a and c are the same object: " + ReferenceEquals(a, c));
    }
}
```
```output
Anita Rai Distinction (86)
Bikash Fail (0)
a and c are the same object: True
```

The program shows **encapsulation**: `marks` is `private`, so the only way to change it is `SetMarks`, which refuses an impossible value. It also shows that `Student c = a;` copies the reference, so changing `c.Name` changes what `a` sees.

A **partial class** (`partial class Student { }` in two files) lets several files contribute to one class; designers and code generators use it (the Windows Forms designer file). A **nested class** is declared inside another class and can be used to hide helper types.

## 3.2 Constructors and deconstructors

A **constructor** is a special method with the name of the class and no return type; it runs when `new` creates the object and puts it into a valid state. If you write none, the compiler gives a public parameterless one. As soon as you write any constructor, the free one disappears.

- **Overloaded constructors** have different parameter lists.
- **Constructor chaining** with `: this(...)` calls another constructor of the same class so that the initialisation code is written once; `: base(...)` calls the base-class constructor (Section 3.9).
- **Object initializers** (`new Student { Name = "A" }`) set accessible members after construction.
- A **copy constructor** takes another object of the same class and copies its data; C# does not provide it automatically.
- A **private constructor** prevents outside creation (used by singletons and static helpers).

A **deconstructor** is the opposite: a method named `Deconstruct` with `out` parameters that lets an object be split into variables: `var (name, roll) = student;`. (This is C# 7 syntax that Mono 6.8's compiler does not support, so the next program calls `Deconstruct` directly and the tuple form is shown as a comment.) Do not confuse it with a *destructor*, the old name for the finalizer (Section 3.7).

```csharp
using System;

class Course
{
    public string Code;
    public string Title;
    public int Credits;

    public Course() : this("TBA", "Untitled", 3) { }                  // chains to the full constructor
    public Course(string code) : this(code, "Untitled", 3) { }
    public Course(string code, string title, int credits)
    {
        Code = code; Title = title; Credits = credits;
        Console.WriteLine("  constructor ran for " + code);
    }
    public Course(Course other) : this(other.Code, other.Title, other.Credits) { }   // copy constructor

    public void Deconstruct(out string code, out string title)
    {
        code = Code; title = Title;
    }
}

class Program
{
    static void Main()
    {
        Console.WriteLine("Creating c1:"); Course c1 = new Course();
        Console.WriteLine("Creating c2:"); Course c2 = new Course("BCA 406");
        Console.WriteLine("Creating c3:"); Course c3 = new Course("BCA 406", "DotNet Technology", 3);
        Console.WriteLine("Copying c3:"); Course c4 = new Course(c3);
        c4.Title = "Copy";
        Console.WriteLine(c3.Title + " / " + c4.Title);
        string code, title;
        c3.Deconstruct(out code, out title);                  // with C# 7: var (code, title) = c3;
        Console.WriteLine("Deconstructed: " + code + " - " + title);
    }
}
```
```output
Creating c1:
  constructor ran for TBA
Creating c2:
  constructor ran for BCA 406
Creating c3:
  constructor ran for BCA 406
Copying c3:
  constructor ran for BCA 406
DotNet Technology / Copy
Deconstructed: BCA 406 - DotNet Technology
```

## 3.3 The `this` reference

Inside an instance method or constructor, **`this`** is a reference to the object on which the method was called. It is used to (1) separate a field from a parameter with the same name (`this.name = name;`), (2) pass the current object to another method (`list.Add(this)`), (3) call another constructor (`: this(...)`), (4) return the current object so that calls can be chained (`return this;`, the *fluent* style), and (5) declare indexers (`public int this[int i]`) and extension methods (`this string s` as the first parameter of a static method). A static method has no `this`, because no object is involved.

```csharp
using System;
using System.Text;

class Report
{
    private StringBuilder body = new StringBuilder();
    private string title;

    public Report(string title) { this.title = title; }          // this disambiguates

    public Report Add(string line)
    {
        body.AppendLine("  - " + line);
        return this;                                              // enables chaining
    }
    public override string ToString() { return title + ":\n" + body.ToString().TrimEnd(); }
}

class Program
{
    static void Main()
    {
        Report r = new Report("Weekly tasks").Add("Write unit 3").Add("Run the programs").Add("Revise LINQ");
        Console.WriteLine(r);
    }
}
```
```output
Weekly tasks:
  - Write unit 3
  - Run the programs
  - Revise LINQ
```

## 3.4 Properties

A **property** looks like a field to the caller but runs code in an accessor: `get` returns the value and `set` receives it as the implicit parameter `value`. Properties are the standard way to expose data, because the class can later add validation, logging or change notification without changing its callers.

| Form | Example | Meaning |
|---|---|---|
| Full property | `public int Age { get { return age; } set { if (value >= 0) age = value; } }` | validation in the setter |
| Auto-implemented | `public string Name { get; set; }` | the compiler creates a hidden field |
| Read-only | `public int Id { get; }` | set only in the constructor |
| Private setter | `public double Balance { get; private set; }` | readable outside, writable inside |
| Computed | `public double Area => Width * Height;` | no storage, calculated every time |
| Initialiser | `public string Status { get; set; } = "New";` | default value |
| `init` accessor (C# 9) | `public string Code { get; init; }` | set only while the object is created |

```csharp
using System;

class BankAccount
{
    private double balance;
    public string Owner { get; set; }
    public int Number { get; }                                    // read-only
    public string Status { get; set; } = "Active";                // initialiser
    public double Balance                                         // read-only to the outside
    {
        get { return balance; }
        private set { balance = value; }
    }
    public double WithTax => balance * 1.13;                      // computed (13 percent VAT, illustrative)

    public BankAccount(int number, string owner) { Number = number; Owner = owner; }

    public void Deposit(double amount)
    {
        if (amount <= 0) throw new ArgumentException("Deposit must be positive");
        Balance += amount;
    }
    public bool Withdraw(double amount)
    {
        if (amount <= 0 || amount > Balance) return false;
        Balance -= amount;
        return true;
    }
}

class Program
{
    static void Main()
    {
        BankAccount acc = new BankAccount(1001, "Sita");
        acc.Deposit(5000);
        Console.WriteLine(acc.Owner + " #" + acc.Number + " " + acc.Status + " balance " + acc.Balance);
        Console.WriteLine("Withdraw 7000: " + acc.Withdraw(7000) + ", Withdraw 1500: " + acc.Withdraw(1500));
        Console.WriteLine("Balance " + acc.Balance + ", with tax " + acc.WithTax);
        // acc.Balance = 1;   // compile error: the setter is private
        try { acc.Deposit(-5); }
        catch (ArgumentException e) { Console.WriteLine("Rejected: " + e.Message); }
    }
}
```
```output
Sita #1001 Active balance 5000
Withdraw 7000: False, Withdraw 1500: True
Balance 3500, with tax 3955
Rejected: Deposit must be positive
```

::: note Field versus property
A public **field** is part of the class's data layout; changing it later (to add a check) breaks every caller that was compiled against it. A **property** hides the storage, so the class stays free to change. This is why .NET guidelines say: never make instance fields public; expose properties.
:::

## 3.5 Indexers

An **indexer** lets an object be used like an array: `marks[2]`. It is declared like a property with the name `this` and a parameter list in square brackets. The parameter need not be an integer: a `string` index gives dictionary-like access. An indexer can be overloaded, can be read-only, and can validate its index.

```csharp
using System;

class MarkSheet
{
    private string[] subjects = { "Maths", "Java", "DBMS", "Networks" };
    private int[] marks = new int[4];

    public int this[int i]                               // integer indexer
    {
        get
        {
            if (i < 0 || i >= marks.Length) throw new IndexOutOfRangeException("Subject number " + i + " does not exist");
            return marks[i];
        }
        set { marks[i] = value; }
    }

    public int this[string subject]                      // overloaded: string indexer
    {
        get { return marks[Array.IndexOf(subjects, subject)]; }
        set { marks[Array.IndexOf(subjects, subject)] = value; }
    }

    public int Total
    {
        get { int t = 0; foreach (int m in marks) t += m; return t; }
    }
}

class Program
{
    static void Main()
    {
        MarkSheet sheet = new MarkSheet();
        sheet[0] = 78;
        sheet["Java"] = 85;
        sheet["DBMS"] = 69;
        sheet[3] = 74;
        Console.WriteLine("Java = " + sheet["Java"] + ", third subject = " + sheet[2] + ", total = " + sheet.Total);
        try { Console.WriteLine(sheet[9]); }
        catch (IndexOutOfRangeException e) { Console.WriteLine("Error: " + e.Message); }
    }
}
```
```output
Java = 85, third subject = 69, total = 306
Error: Subject number 9 does not exist
```

## 3.6 Static constructors and static classes

A **static member** belongs to the class itself, not to any object: one copy is shared by all instances and it is reached through the class name (`Math.PI`, `Console.WriteLine`). A static method cannot use `this` or instance members directly.

A **static constructor** (`static ClassName() { }`) initialises static data. It has no access modifier and no parameters, is called automatically by the runtime at most once, before the first instance is created or any static member is used, and you cannot call it yourself. A **static class** (`static class Helper`) can contain only static members, cannot be instantiated and cannot be inherited; utility libraries such as `Math` and `Console` are static classes. **Extension methods** are static methods in a static class whose first parameter is marked `this`; they let you call `"abc".IsPalindrome()` as if the method belonged to `string`.

```csharp
using System;

class Counter
{
    public static int Created;                    // shared by every object
    public static readonly DateTime Started;
    public readonly int Id;

    static Counter()                              // runs once, before first use
    {
        Started = new DateTime(2025, 1, 1);
        Console.WriteLine("static constructor ran");
    }
    public Counter() { Created++; Id = Created; }
}

static class TextTools
{
    public static bool IsPalindrome(this string s)
    {
        string t = s.Replace(" ", "").ToLower();
        for (int i = 0, j = t.Length - 1; i < j; i++, j--)
            if (t[i] != t[j]) return false;
        return true;
    }
    public static string Initials(this string name)
    {
        string r = "";
        foreach (string w in name.Split(' ')) r += char.ToUpper(w[0]);
        return r;
    }
}

class Program
{
    static void Main()
    {
        Console.WriteLine("Main starts");
        Counter a = new Counter();
        Counter b = new Counter();
        Console.WriteLine("Created = " + Counter.Created + ", a.Id = " + a.Id + ", b.Id = " + b.Id + ", started " + Counter.Started.Year);
        Console.WriteLine("\"Never odd or even\".IsPalindrome() = " + "Never odd or even".IsPalindrome());
        Console.WriteLine("\"tribhuvan university\".Initials() = " + "tribhuvan university".Initials());
    }
}
```
```output
Main starts
static constructor ran
Created = 2, a.Id = 1, b.Id = 2, started 2025
"Never odd or even".IsPalindrome() = True
"tribhuvan university".Initials() = TU
```

## 3.7 Finalizers

A **finalizer** (written `~ClassName() { }`, with no parameters and no modifiers) is a method the garbage collector calls on an object *after* finding it unreachable and *before* reclaiming its memory. It exists to release unmanaged resources if the programmer forgot to. Its limits are important: you cannot call it, you do not know *when* it runs (possibly never before the program ends), and objects with finalizers live longer because they survive one extra collection. For these reasons .NET uses the **dispose pattern**: implement `IDisposable` with a `Dispose()` method that releases the resource at once, call `GC.SuppressFinalize(this)` to cancel the finalizer, and let callers use `using`.

```csharp
using System;

class FileLock : IDisposable
{
    private bool disposed;
    public string Name { get; private set; }

    public FileLock(string name) { Name = name; Console.WriteLine("  acquired " + name); }

    public void Dispose()
    {
        if (!disposed)
        {
            disposed = true;
            Console.WriteLine("  released " + Name);        // free the unmanaged resource here
            GC.SuppressFinalize(this);                      // the finalizer is no longer needed
        }
    }
    ~FileLock()                                              // safety net only
    {
        if (!disposed) Console.WriteLine("  finalizer: " + Name + " was never disposed");
    }
}

class Program
{
    static void Main()
    {
        Console.WriteLine("Using block:");
        using (FileLock f = new FileLock("report.txt"))
        {
            Console.WriteLine("  working with " + f.Name);
        }                                                   // Dispose runs here, even after an exception
        Console.WriteLine("Explicit Dispose:");
        FileLock g = new FileLock("data.db");
        g.Dispose();
        g.Dispose();                                        // calling twice is harmless
    }
}
```
```output
Using block:
  acquired report.txt
  working with report.txt
  released report.txt
Explicit Dispose:
  acquired data.db
  released data.db
```

## 3.8 Inheritance, dynamic binding and abstract classes

**Inheritance** lets a new class (the *derived* or child class) reuse and extend an existing one (the *base* or parent class): `class Student : Person`. The derived class gets the accessible members of the base, can add its own, and can replace some. C# allows **single inheritance** of classes: one base class, but any number of interfaces. Every class ultimately derives from `System.Object`. Constructors are not inherited, but a derived constructor must call a base constructor: implicitly the parameterless one, or explicitly with `: base(args)`. Base constructors run first.

### `base`, `virtual`, `override`, `new` and `sealed`

| Keyword | Meaning |
|---|---|
| `base.Member` | Refers to the base-class version of a member from inside the derived class |
| `virtual` | Marks a base member that derived classes **may** replace |
| `override` | Replaces a virtual (or abstract) base member |
| `new` (on a member) | **Hides** a base member with a new one; no polymorphism (a compiler warning without `new`) |
| `sealed` | On a class: cannot be inherited. On an override: cannot be overridden further |
| `abstract` | A member without a body, or a class that cannot be instantiated; derived classes must supply the body |

### Dynamic binding (run-time polymorphism)

Which version of a virtual method runs is decided at **run time**, by the real type of the object, not by the declared type of the variable. This is **dynamic binding**, also called late binding or run-time polymorphism. The compiler keeps a *virtual method table* for each class; a call to a virtual method looks up the slot in the table of the actual object. A non-virtual method is bound at compile time using the variable's declared type. Hiding with `new` is therefore not polymorphic: the version chosen depends on the variable type.

An **abstract class** models an idea that is incomplete by itself ("Shape"). It may contain fields, constructors, normal methods and abstract methods. You cannot write `new Shape()`, but you can declare `Shape s = new Circle(2);`.

```svgfig label="3.1" caption="A class hierarchy with an abstract base class. Circle and Rectangle override the abstract Area method. A Shape variable can refer to either, and the call s.Area() is bound at run time to the actual object's version."
f = Fig(560, 230)
f.box(190, 10, 180, 56, "abstract class Shape\nName\nabstract double Area()", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(40, 130, 190, 50, "class Circle\nRadius\noverride Area()", fill=BLUE, stroke=NAVY, size=10)
f.box(330, 130, 190, 50, "class Rectangle\nWidth, Height\noverride Area()", fill=BLUE, stroke=NAVY, size=10)
f.arrow([(135, 130), (135, 98), (280, 98), (280, 66)], color=SLATE)
f.arrow([(425, 130), (425, 98), (280, 98), (280, 66)], color=SLATE)
f.text(280, 90, "inherits from", size=9.5, color=SLATE)
f.text(280, 212, "Shape s = new Circle(2);   s.Area() runs Circle.Area", size=10.5, color=TEAL, bold=True)
```

```csharp
using System;

abstract class Shape
{
    public string Name { get; private set; }
    protected Shape(string name) { Name = name; }
    public abstract double Area();                         // no body: derived classes must override
    public virtual string Describe()                       // may be overridden
    {
        return Name + " with area " + Area().ToString("F2");
    }
}

class Circle : Shape
{
    private double r;
    public Circle(double r) : base("Circle") { this.r = r; }
    public override double Area() { return Math.PI * r * r; }
}

class Rectangle : Shape
{
    private double w, h;
    public Rectangle(double w, double h) : base("Rectangle") { this.w = w; this.h = h; }
    public override double Area() { return w * h; }
}

class Square : Rectangle
{
    public Square(double side) : base(side, side) { }
    public override string Describe() { return "Square! " + base.Describe(); }     // extends the base version
}

class Animal
{
    public string Speak() { return "..."; }                   // not virtual
    public virtual string Move() { return "moves"; }
}
class Dog : Animal
{
    public new string Speak() { return "Woof"; }              // hides, not overrides
    public override string Move() { return "runs"; }          // overrides
}

class Program
{
    static void Main()
    {
        Shape[] shapes = { new Circle(2), new Rectangle(3, 4), new Square(5) };
        foreach (Shape s in shapes) Console.WriteLine(s.Describe());

        Animal a = new Dog();                                  // declared Animal, real type Dog
        Dog d = new Dog();
        Console.WriteLine("Hidden method through Animal variable: " + a.Speak() + ", through Dog variable: " + d.Speak());
        Console.WriteLine("Overridden method through Animal variable: " + a.Move() + ", through Dog variable: " + d.Move());
        Console.WriteLine("a is Dog: " + (a is Dog) + ", a is object: " + (a is object) + ", type name: " + a.GetType().Name);
    }
}
```
```output
Circle with area 12.57
Rectangle with area 12.00
Square! Rectangle with area 25.00
Hidden method through Animal variable: ..., through Dog variable: Woof
Overridden method through Animal variable: runs, through Dog variable: runs
a is Dog: True, a is object: True, type name: Dog
```

The output shows both rules: `Move()` is virtual and overridden, so the real type (`Dog`) decides even through an `Animal` variable; `Speak()` is hidden with `new`, so the declared type decides. In examinations, always say that **overriding gives run-time polymorphism and hiding does not**.

### Method overloading versus overriding

| | Overloading | Overriding |
|---|---|---|
| Where | same class (or base and derived) | derived class only |
| Signature | same name, **different** parameter list | same name and **same** signature |
| Binding | compile time (static) | run time (dynamic) |
| Keywords | none | `virtual` / `abstract` and `override` |
| Return type | cannot be the only difference | must match |

```csharp
using System;

class Calculator
{
    public int Add(int a, int b) { return a + b; }
    public double Add(double a, double b) { return a + b; }
    public int Add(int a, int b, int c) { return a + b + c; }
    public string Add(string a, string b) { return a + b; }
}

class Program
{
    static void Main()
    {
        Calculator c = new Calculator();
        Console.WriteLine(c.Add(2, 3) + " | " + c.Add(2.5, 3) + " | " + c.Add(1, 2, 3) + " | " + c.Add("Net", "Core"));
    }
}
```
```output
5 | 5.5 | 6 | NetCore
```

The compiler picks the best match from the argument types: `Add(2.5, 3)` uses the `double` version because 2.5 is a `double` and the `int` 3 converts implicitly.

## 3.9 Operator overloading

C# lets a class or struct define the meaning of operators for its own type, so that `a + b` works for fractions, vectors or money. An overloaded operator is a `public static` method named `operator` followed by the symbol. Rules: you can overload unary `+ - ! ~ ++ --`, binary `+ - * / % & | ^ << >>` and the comparison operators; you **cannot** create new operators, change precedence, or overload `=`, `&&`, `||`, `?:`, `.`, `new` or `is` (the short-circuit operators are derived from `true`/`false` and `&`/`|`). Comparison operators must be overloaded in pairs (`==` with `!=`, `<` with `>`, `<=` with `>=`). If you overload `==`, also override `Equals` and `GetHashCode`; otherwise the compiler warns, because collections use those two. Implicit and explicit **conversion operators** (`public static implicit operator double(Fraction f)`) define conversions.

```csharp
using System;

class Fraction
{
    public int Num { get; private set; }
    public int Den { get; private set; }

    public Fraction(int num, int den)
    {
        if (den == 0) throw new ArgumentException("Denominator cannot be zero");
        int g = Gcd(Math.Abs(num), Math.Abs(den));
        if (den < 0) { num = -num; den = -den; }
        Num = num / g; Den = den / g;
    }
    static int Gcd(int a, int b) { return b == 0 ? (a == 0 ? 1 : a) : Gcd(b, a % b); }

    public static Fraction operator +(Fraction a, Fraction b) { return new Fraction(a.Num * b.Den + b.Num * a.Den, a.Den * b.Den); }
    public static Fraction operator -(Fraction a, Fraction b) { return new Fraction(a.Num * b.Den - b.Num * a.Den, a.Den * b.Den); }
    public static Fraction operator *(Fraction a, Fraction b) { return new Fraction(a.Num * b.Num, a.Den * b.Den); }
    public static Fraction operator -(Fraction a) { return new Fraction(-a.Num, a.Den); }       // unary minus
    public static bool operator ==(Fraction a, Fraction b) { return a.Num == b.Num && a.Den == b.Den; }
    public static bool operator !=(Fraction a, Fraction b) { return !(a == b); }
    public static bool operator <(Fraction a, Fraction b) { return a.Num * b.Den < b.Num * a.Den; }
    public static bool operator >(Fraction a, Fraction b) { return b < a; }
    public static implicit operator double(Fraction f) { return (double)f.Num / f.Den; }

    public override bool Equals(object obj) { Fraction f = obj as Fraction; return !ReferenceEquals(f, null) && this == f; }
    public override int GetHashCode() { return Num * 31 + Den; }
    public override string ToString() { return Den == 1 ? Num.ToString() : Num + "/" + Den; }
}

class Program
{
    static void Main()
    {
        Fraction a = new Fraction(1, 2), b = new Fraction(1, 3);
        Console.WriteLine(a + " + " + b + " = " + (a + b));
        Console.WriteLine(a + " - " + b + " = " + (a - b));
        Console.WriteLine(a + " * " + b + " = " + (a * b));
        Console.WriteLine("-(" + a + ") = " + (-a));
        Console.WriteLine("2/4 == 1/2 : " + (new Fraction(2, 4) == a) + ",  a > b : " + (a > b));
        double d = a;                                           // implicit conversion
        Console.WriteLine("as double: " + d);
    }
}
```
```output
1/2 + 1/3 = 5/6
1/2 - 1/3 = 1/6
1/2 * 1/3 = 1/6
-(1/2) = -1/2
2/4 == 1/2 : True,  a > b : True
as double: 0.5
```

## 3.10 The `object` type and its members

`System.Object` (alias `object`) is the root of every type, so a variable of type `object` can hold anything (value types are boxed). Every type therefore inherits these members:

| Member | Default behaviour | Usually overridden to |
|---|---|---|
| `ToString()` | returns the type name (`Program+Student`) | return a readable description |
| `Equals(object)` | reference equality for classes | compare contents (value equality) |
| `GetHashCode()` | based on the reference | give equal objects equal codes (needed by `Dictionary` and `HashSet`) |
| `GetType()` | returns the `Type` object (not virtual) | not overridable; used for reflection |
| `ReferenceEquals(a, b)` | static; tests the identity of two references | not overridable |
| `Finalize()` | does nothing | written as a `~Class()` finalizer |
| `MemberwiseClone()` | protected; shallow copy of the fields | used to implement `Clone` |

The rule connecting the two: **if `a.Equals(b)` is true then `a.GetHashCode()` must equal `b.GetHashCode()`**. A mutable object used as a dictionary key must not change the fields that feed its hash code.

```csharp
using System;
using System.Collections.Generic;

class Point
{
    public int X, Y;
    public Point(int x, int y) { X = x; Y = y; }
}

class GoodPoint
{
    public readonly int X, Y;
    public GoodPoint(int x, int y) { X = x; Y = y; }
    public override string ToString() { return "(" + X + ", " + Y + ")"; }
    public override bool Equals(object obj)
    {
        GoodPoint p = obj as GoodPoint;
        return p != null && p.X == X && p.Y == Y;
    }
    public override int GetHashCode() { return X * 397 ^ Y; }
}

class Program
{
    static void Main()
    {
        Point p1 = new Point(1, 2), p2 = new Point(1, 2);
        Console.WriteLine("Point.ToString(): " + p1);
        Console.WriteLine("p1.Equals(p2): " + p1.Equals(p2) + " (reference comparison)");

        GoodPoint g1 = new GoodPoint(1, 2), g2 = new GoodPoint(1, 2);
        Console.WriteLine("GoodPoint.ToString(): " + g1 + ", Equals: " + g1.Equals(g2) + ", same hash: " + (g1.GetHashCode() == g2.GetHashCode()));
        var set = new HashSet<GoodPoint> { g1 };
        Console.WriteLine("HashSet contains an equal point: " + set.Contains(g2));
        Console.WriteLine("Type: " + g1.GetType().Name + ", base type: " + g1.GetType().BaseType.Name);
        object o = 42;
        Console.WriteLine("42 as object: " + o.GetType().Name + ", ToString() = \"" + o.ToString() + "\"");
    }
}
```
```output
Point.ToString(): Point
p1.Equals(p2): False (reference comparison)
GoodPoint.ToString(): (1, 2), Equals: True, same hash: True
HashSet contains an equal point: True
Type: GoodPoint, base type: Object
42 as object: Int32, ToString() = "42"
```

## 3.11 Structs

A **struct** is a **value type** declared with `struct`. It can have fields, properties, methods, constructors (with parameters), operators and interfaces, but **cannot inherit** from another struct or class (it derives implicitly from `System.ValueType`) and cannot have a finalizer. Copying a struct copies all its data, so structs suit small, immutable pieces of data: `Point`, `DateTime`, `Color`, a coordinate, a money amount.

| | `class` | `struct` |
|---|---|---|
| Kind | reference type | value type |
| Storage | heap (variable holds a reference) | inline: stack or inside the containing object |
| Assignment | copies the reference | copies the data |
| Inheritance | single base class | none (interfaces allowed) |
| Default value | `null` | all fields zero (parameterless constructor always exists) |
| Best for | objects with identity and behaviour | small values, 16 bytes or less, preferably immutable (`readonly struct` enforces this from C# 7.2) |

```csharp
using System;

struct PointS { public int X, Y; public PointS(int x, int y) { X = x; Y = y; } }
class PointC { public int X, Y; public PointC(int x, int y) { X = x; Y = y; } }

struct Money
{
    public decimal Amount { get; }
    public string Currency { get; }
    public Money(decimal amount, string currency) { Amount = amount; Currency = currency; }
    public Money Add(Money other) { return new Money(Amount + other.Amount, Currency); }
    public override string ToString() { return Currency + " " + Amount.ToString("N2"); }
}

class Program
{
    static void Main()
    {
        PointS s1 = new PointS(1, 2); PointS s2 = s1; s2.X = 99;
        PointC c1 = new PointC(1, 2); PointC c2 = c1; c2.X = 99;
        Console.WriteLine("struct: s1.X = " + s1.X + ", s2.X = " + s2.X + "   (independent copies)");
        Console.WriteLine("class:  c1.X = " + c1.X + ", c2.X = " + c2.X + "   (one object, two references)");

        Money fee = new Money(12500m, "NPR");
        Money total = fee.Add(new Money(2500.50m, "NPR"));
        Console.WriteLine(fee + " + 2,500.50 = " + total);
        PointS def = default(PointS);
        Console.WriteLine("default struct: (" + def.X + ", " + def.Y + ")");
    }
}
```
```output
struct: s1.X = 1, s2.X = 99   (independent copies)
class:  c1.X = 99, c2.X = 99   (one object, two references)
NPR 12,500.00 + 2,500.50 = NPR 15,000.50
default struct: (0, 0)
```

## 3.12 Access modifiers

An **access modifier** controls which code may see a type or member. Always give each member the narrowest access that works.

| Modifier | Visible to | Typical use |
|---|---|---|
| `public` | all code in any assembly | the API of the class |
| `private` | only the containing type (the default for members) | fields, helpers |
| `protected` | the containing type and its derived classes | members for subclasses |
| `internal` | all code in the same assembly (the default for top-level types) | helpers of a library |
| `protected internal` | same assembly **or** derived classes in any assembly | |
| `private protected` | derived classes **in the same assembly** | (C# 7.2) |
| `file` | only the same source file (C# 11) | generated helper types |

A top-level type can be only `public` or `internal`; nested types and members can use all. A derived class cannot be more accessible than its base class, and a method cannot expose a less accessible type in its signature.

```svgfig label="3.2" caption="Where each access modifier lets a member be seen. Rows are the places the calling code can be in; a tick means the call compiles."
f = Fig(580, 205)
cols = ["public", "protected\ninternal", "internal", "protected", "private"]
rows = ["Same class", "Derived class, same assembly", "Non-derived class, same assembly", "Derived class, other assembly", "Any class, other assembly"]
tick = [
  [1, 1, 1, 1, 1],
  [1, 1, 1, 1, 0],
  [1, 1, 1, 0, 0],
  [1, 1, 0, 1, 0],
  [1, 0, 0, 0, 0],
]
x0, y0, cw, rh = 205, 38, 74, 28
for j, c in enumerate(cols):
    f.text(x0 + j * cw + cw / 2, 18, c.split("\n")[0], size=9.5, color=NAVY, bold=True)
    if "\n" in c: f.text(x0 + j * cw + cw / 2, 30, c.split("\n")[1], size=9.5, color=NAVY, bold=True)
for i, r in enumerate(rows):
    y = y0 + i * rh
    f.text(8, y + rh / 2, r, size=10, color=SLATE, anchor="start", vmid=True)
    for j in range(5):
        ok = tick[i][j]
        f.box(x0 + j * cw + 4, y + 3, cw - 8, rh - 6, "yes" if ok else "no", fill=MINT if ok else ROSE, stroke=TEAL if ok else RED, size=10, bold=True)
```

::: example Protected in practice
`class Person { protected string nid; }` and `class Teacher : Person { void Show() { Console.WriteLine(nid); } }` compiles because `Teacher` is a derived class. A `Main` method that creates a `Person` and writes `p.nid` does not compile, because `Main` is not in a derived class. Through a `Teacher` object created inside `Teacher`, access is allowed.
:::

## 3.13 Interfaces

An **interface** is a contract: a list of members (methods, properties, events, indexers) that a class promises to provide, with no fields and, traditionally, no code. By convention the name starts with `I`. A class (or struct) *implements* the interface and must supply every member. Because a class can implement **many** interfaces, interfaces give C# the benefits of multiple inheritance without its ambiguity. A variable of the interface type can refer to any implementing object, which gives polymorphism that does not depend on a common base class.

| | Abstract class | Interface |
|---|---|---|
| Instances | cannot be created | cannot be created |
| Members | fields, constructors, concrete and abstract methods | signatures only (C# 8 adds default implementations) |
| Inheritance | a class derives from **one** | a class may implement **many** |
| Use | closely related types sharing code | unrelated types sharing a capability (`IComparable`, `IDisposable`, `IEnumerable<T>`) |
| Access modifiers on members | any | members are public |

**Explicit implementation** (`void IPrinter.Print()`) hides a member from the class's own interface and is used when two interfaces have the same member name. Important framework interfaces: `IComparable<T>` (ordering, used by `Sort`), `IEquatable<T>`, `IEnumerable<T>` (works with `foreach` and LINQ), `IDisposable` (cleanup) and `ICloneable`.

```csharp
using System;
using System.Collections.Generic;

interface IPayable
{
    decimal MonthlyPay();
    string Name { get; }
}
interface IReportable { string Report(); }

class Employee : IPayable, IReportable, IComparable<Employee>
{
    public string Name { get; private set; }
    private decimal salary;
    public Employee(string name, decimal salary) { Name = name; this.salary = salary; }
    public decimal MonthlyPay() { return salary; }
    public string Report() { return Name + " earns " + salary.ToString("N0"); }
    public int CompareTo(Employee other) { return salary.CompareTo(other.salary); }   // used by Sort
}

class Contractor : IPayable
{
    public string Name { get; private set; }
    private decimal hourly; private int hours;
    public Contractor(string name, decimal hourly, int hours) { Name = name; this.hourly = hourly; this.hours = hours; }
    public decimal MonthlyPay() { return hourly * hours; }
}

class Printer1 { public void Print() { Console.WriteLine("Laser"); } }
class Both : IPayable, IReportable
{
    public string Name { get { return "Both"; } }
    public decimal MonthlyPay() { return 1; }
    string IReportable.Report() { return "explicit implementation: reachable only through IReportable"; }
}

class Program
{
    static void Main()
    {
        List<IPayable> staff = new List<IPayable>
        {
            new Employee("Anita", 65000m), new Contractor("Bikash", 800m, 90), new Employee("Chandra", 48000m)
        };
        decimal total = 0;
        foreach (IPayable p in staff) { total += p.MonthlyPay(); Console.WriteLine(p.Name + ": " + p.MonthlyPay().ToString("N0")); }
        Console.WriteLine("Total payroll: " + total.ToString("N0"));

        Employee[] team = { new Employee("Anita", 65000m), new Employee("Chandra", 48000m), new Employee("Dipesh", 57000m) };
        Array.Sort(team);                                                  // uses IComparable<Employee>
        foreach (Employee e in team) Console.WriteLine(e.Report());

        IReportable r = new Both();
        Console.WriteLine(r.Report());
        Console.WriteLine("Contractor implements IReportable: " + (staff[1] is IReportable));
    }
}
```
```output
Anita: 65,000
Bikash: 72,000
Chandra: 48,000
Total payroll: 185,000
Chandra earns 48,000
Dipesh earns 57,000
Anita earns 65,000
explicit implementation: reachable only through IReportable
Contractor implements IReportable: False
```

::: note Default interface methods (C# 8 and later)
An interface may now include a method body: `interface ILogger { void Log(string m) { Console.WriteLine(m); } }`. This lets library authors add members without breaking existing implementers. The book's C# 7 checker does not compile it, so it is mentioned only; exam answers should still describe an interface as a contract without implementation.
:::

## 3.14 Enumerations

An **enumeration** (`enum`) is a value type made of named integer constants. It makes code readable (`Day.Friday` instead of `5`) and prevents invalid constants from spreading. The underlying type is `int` unless you choose another (`enum Level : byte`); the first name is 0 and each next name is one more unless you assign a value. `[Flags]` marks an enum whose values are powers of two, so values can be combined with `|` and tested with `&` (or `HasFlag`).

```csharp
using System;

enum Day { Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday }
enum Grade : byte { F = 0, D = 40, C = 50, B = 60, A = 80 }

[Flags]
enum Permission { None = 0, Read = 1, Write = 2, Execute = 4, All = Read | Write | Execute }

class Program
{
    static void Main()
    {
        Day d = Day.Friday;
        Console.WriteLine(d + " has the value " + (int)d);
        Console.WriteLine("Next day: " + (Day)(((int)d + 1) % 7));
        Console.WriteLine("Parse: " + Enum.Parse(typeof(Day), "Monday") + ", IsDefined(9): " + Enum.IsDefined(typeof(Day), 9));
        foreach (Grade g in Enum.GetValues(typeof(Grade))) Console.Write(g + "=" + (int)g + " ");
        Console.WriteLine();

        Permission p = Permission.Read | Permission.Write;
        Console.WriteLine("p = " + p + ", can write: " + ((p & Permission.Write) != 0) + ", can execute: " + p.HasFlag(Permission.Execute));
        p |= Permission.Execute;
        Console.WriteLine("after adding Execute: " + p + " (equals All: " + (p == Permission.All) + ")");
        p &= ~Permission.Write;                                      // remove a flag
        Console.WriteLine("after removing Write: " + p);

        switch (d)
        {
            case Day.Saturday: case Day.Sunday: Console.WriteLine("weekend"); break;
            default: Console.WriteLine("working day"); break;
        }
    }
}
```
```output
Friday has the value 5
Next day: Saturday
Parse: Monday, IsDefined(9): False
F=0 D=40 C=50 B=60 A=80 
p = Read, Write, can write: True, can execute: False
after adding Execute: All (equals All: True)
after removing Write: Read, Execute
working day
```

## 3.15 Generics

Before generics, a reusable collection stored `object`: `ArrayList` accepted anything, forced casts and boxing, and found type errors only at run time. **Generics** (C# 2.0) let you write a class, struct, interface, method or delegate with a **type parameter** such as `T`, and fill in the real type when you use it. The compiler checks every use (type safe), no casts are needed, and value types are stored without boxing (fast). `List<int>` and `List<string>` are different *constructed* types made from one *generic* definition `List<T>`.

```svgfig label="3.3" caption="A generic definition and the types constructed from it. One piece of source, Stack<T>, gives the compiler a separate, fully type-checked class for each type argument; no boxing or casting is needed."
f = Fig(560, 170)
f.box(205, 10, 150, 46, "class Stack<T>\nPush(T)  T Pop()", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(10, 110, 150, 46, "Stack<int>\nPush(int)  int Pop()", fill=BLUE, stroke=NAVY, size=10)
f.box(205, 110, 150, 46, "Stack<string>\nPush(string)  string Pop()", fill=BLUE, stroke=NAVY, size=10)
f.box(400, 110, 150, 46, "Stack<Student>\nPush(Student)  Student Pop()", fill=BLUE, stroke=NAVY, size=9.5)
f.arrow([(280, 56), (280, 110)], color=SLATE)
f.arrow([(250, 56), (250, 82), (85, 82), (85, 110)], color=SLATE)
f.arrow([(310, 56), (310, 82), (475, 82), (475, 110)], color=SLATE)
f.text(280, 98, "T = string", size=9.5, color=TEAL, bold=True, anchor="start")
```

### Generic methods and constraints

A **generic method** has its own type parameter: `static void Swap<T>(ref T a, ref T b)`. The compiler usually infers `T` from the arguments (`Swap(ref x, ref y)`). Inside generic code `T` could be anything, so you cannot call `a.CompareTo(b)` unless you promise that `T` supports it with a **constraint**:

| Constraint | Meaning |
|---|---|
| `where T : struct` | `T` must be a non-nullable value type |
| `where T : class` | `T` must be a reference type |
| `where T : new()` | `T` has a public parameterless constructor (so `new T()` is legal) |
| `where T : BaseClass` | `T` derives from `BaseClass` |
| `where T : IComparable<T>` | `T` implements the interface (so `CompareTo` can be called) |
| `where T : U` | `T` derives from another type parameter `U` |

### Standard generic collections

| Collection | Use | Notes |
|---|---|---|
| `List<T>` | resizable array | index, `Add`, `Remove`, `Sort`, `Contains` |
| `Dictionary<TKey, TValue>` | key to value lookup | average O(1); keys unique |
| `HashSet<T>` | set of unique items | union, intersection |
| `Queue<T>`, `Stack<T>` | FIFO and LIFO | `Enqueue/Dequeue`, `Push/Pop` |
| `LinkedList<T>` | doubly linked list | cheap insert in the middle |
| `SortedDictionary<TKey, TValue>` | ordered by key | O(log n) |

```csharp
using System;
using System.Collections.Generic;

class Stack<T>                                     // our own generic class
{
    private List<T> items = new List<T>();
    public int Count { get { return items.Count; } }
    public void Push(T item) { items.Add(item); }
    public T Pop()
    {
        if (items.Count == 0) throw new InvalidOperationException("stack is empty");
        T top = items[items.Count - 1];
        items.RemoveAt(items.Count - 1);
        return top;
    }
}

class Pair<TKey, TValue>
{
    public TKey Key { get; private set; }
    public TValue Value { get; private set; }
    public Pair(TKey k, TValue v) { Key = k; Value = v; }
    public override string ToString() { return "(" + Key + ", " + Value + ")"; }
}

class Program
{
    static void Swap<T>(ref T a, ref T b) { T t = a; a = b; b = t; }

    static T Max<T>(T[] items) where T : IComparable<T>      // constraint lets us call CompareTo
    {
        T best = items[0];
        foreach (T x in items) if (x.CompareTo(best) > 0) best = x;
        return best;
    }

    static T Create<T>() where T : new() { return new T(); }

    static void Main()
    {
        Stack<int> s = new Stack<int>();
        s.Push(10); s.Push(20); s.Push(30);
        Console.WriteLine("Pop " + s.Pop() + ", then " + s.Pop() + ", count left " + s.Count);
        Stack<string> words = new Stack<string>();
        words.Push("net"); words.Push("dot");
        Console.WriteLine(words.Pop() + words.Pop());

        int x = 1, y = 2; Swap(ref x, ref y);
        string a = "A", b = "B"; Swap(ref a, ref b);
        Console.WriteLine("Swap ints: " + x + "," + y + "; strings: " + a + "," + b);
        Console.WriteLine("Max of ints: " + Max(new[] { 4, 17, 9 }) + ", of strings: " + Max(new[] { "pear", "apple", "zebra" }));
        Console.WriteLine("Create<List<int>>() count = " + Create<List<int>>().Count);
        Console.WriteLine(new Pair<string, int>("Maths", 78));

        var marks = new Dictionary<string, int> { { "Anita", 86 }, { "Bikash", 52 } };
        marks["Chandra"] = 67;
        foreach (KeyValuePair<string, int> kv in marks) Console.WriteLine(kv.Key + " -> " + kv.Value);
        int val;
        Console.WriteLine("TryGetValue(\"Dipesh\"): " + marks.TryGetValue("Dipesh", out val));
        try { s.Pop(); s.Pop(); }
        catch (InvalidOperationException e) { Console.WriteLine("Error: " + e.Message); }
    }
}
```
```output
Pop 30, then 20, count left 1
dotnet
Swap ints: 2,1; strings: B,A
Max of ints: 17, of strings: zebra
Create<List<int>>() count = 0
(Maths, 78)
Anita -> 86
Bikash -> 52
Chandra -> 67
TryGetValue("Dipesh"): False
Error: stack is empty
```

**Variance** (a preview): a read-only generic interface may be *covariant* (`IEnumerable<out T>`: an `IEnumerable<string>` can be used as `IEnumerable<object>`), and an input-only one *contravariant* (`Action<in T>`). A `List<string>` is not a `List<object>`, because a list can also be written to.

## 3.16 Summary and exercises

A class is a reference type with fields, properties, methods, constructors and more; constructors set up objects (chained with `this(...)`, base-class ones with `base(...)`), properties and indexers give controlled access, static members and static constructors belong to the type, and finalizers are a safety net behind `IDisposable`. Inheritance with `virtual` and `override` gives dynamic binding, abstract classes force derived classes to complete a design, and interfaces give contracts that classes may combine. Overloaded operators make user types natural to use, structs are small value types, enums name constants, access modifiers limit visibility, and generics give reusable, type-safe, boxing-free code.

1. Define class and object. Write a `Book` class with private fields, a constructor, properties and a method that returns a description.
2. What is constructor chaining? Why is it useful? Show it with `this(...)`.
3. Explain `this` with five uses.
4. Compare fields and properties. Write an auto-implemented property and one with validation.
5. What is an indexer? Write a class `Week` with a string indexer for the days.
6. When is a static constructor called? List the rules for static classes.
7. What is a finalizer? Why is the dispose pattern preferred? Write the pattern.
8. Differentiate method overloading, overriding and hiding.
9. Explain dynamic binding with a program using a base class `Shape` and two derived classes.
10. Distinguish abstract classes and interfaces. When would you choose each?
11. Overload `+` and `==` for a `Complex` or `Money` class. What other members must be overridden together with `==`?
12. List the members of `System.Object` and explain `ToString`, `Equals` and `GetHashCode`.
13. Compare struct and class. When would you use a struct?
14. Explain the six access modifiers with an example of `protected`.
15. Declare an enum for months and a `[Flags]` enum for file permissions; show how to add and remove a flag.
16. What are generics and why were they introduced? Write a generic `Swap<T>` and a generic method with a `where T : IComparable<T>` constraint.
17. State and explain the six kinds of generic constraint.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Distinguish overloading, overriding and hiding.**

*Overloading* gives several methods in one class the same name but different parameter lists, e.g. `Add(int, int)` and `Add(double, double)`; the compiler chooses at compile time, so it is static polymorphism. *Overriding* replaces a `virtual` or `abstract` base method in a derived class with the same signature using `override`; the version is chosen at run time from the real type of the object (dynamic binding). *Hiding* declares a new member with the same name in the derived class using `new`; the base member still exists and the choice depends on the declared type of the variable. In Section 3.8 `Animal a = new Dog(); a.Move()` runs `Dog.Move` (overriding) while `a.Speak()` runs `Animal.Speak` (hiding).

**Q2 (5 marks). What is a property? Write a class with a validated property.**

A property is a member that exposes a value through `get` and `set` accessors, so callers use field syntax while the class keeps control. 

```csharp
using System;

class Person
{
    private int age;
    public string Name { get; set; }
    public int Age
    {
        get { return age; }
        set
        {
            if (value < 0 || value > 130) throw new ArgumentOutOfRangeException("value", "Age must be 0 to 130");
            age = value;
        }
    }
}

class Program
{
    static void Main()
    {
        Person p = new Person { Name = "Rita", Age = 21 };
        Console.WriteLine(p.Name + " is " + p.Age);
        try { p.Age = -4; }
        catch (ArgumentOutOfRangeException) { Console.WriteLine("Age -4 rejected by the setter"); }
    }
}
```
```output
Rita is 21
Age -4 rejected by the setter
```

Advantages: validation, read-only or write-private access, computed values, and freedom to change the storage later without breaking callers.

**Q3 (10 marks). Explain inheritance and polymorphism in C# with a program.**

Inheritance forms an *is-a* relationship: `Circle` is a `Shape`. The derived class reuses the base class's accessible members, adds its own and may override virtual ones; constructors are not inherited, so the derived constructor calls the base one with `: base(...)`, and the base part is constructed first. C# supports single inheritance of classes and multiple interfaces; `sealed` stops further inheritance. Polymorphism means that one call, `s.Area()`, behaves according to the real object: the compiler stores a virtual method table in each class and the call looks up the entry of the actual object at run time. The program in Section 3.8 stores a `Circle`, a `Rectangle` and a `Square` in a `Shape[]` and prints `12.57`, `12.00` and `25.00`; adding a new shape needs no change in the loop, which is the open-closed principle. Square overrides `Describe` and calls `base.Describe()` to extend rather than replace the behaviour.

**Q4 (10 marks). What are generics? Explain their advantages and constraints with an example.**

Generics let a type or method declare type parameters, so the same code works for many types while the compiler still checks them. Advantages: (1) *type safety*, because errors are found at compile time instead of `InvalidCastException` at run time; (2) *no casting* when reading from a collection; (3) *performance*, since value types are stored directly with no boxing; (4) *reuse*, as one `Stack<T>` serves `int`, `string` and `Student`; (5) *readability*. A constraint tells the compiler what `T` can do. Without `where T : IComparable<T>` the call `x.CompareTo(best)` in `Max<T>` would not compile, because `T` might be a type with no ordering. Section 3.15 builds `Stack<T>`, `Pair<TKey, TValue>`, `Swap<T>`, `Max<T>` with a constraint and `Create<T>() where T : new()`, and uses `Dictionary<string, int>`. The old `ArrayList` is non-generic: it stores `object`, boxes every `int` and needs a cast on each read, which is why it should not be used in new code.

**Q5 (10 marks). Compare an abstract class and an interface, and write a program in which a class implements two interfaces.**

An abstract class is a partly complete class: it can have fields, constructors, concrete methods and abstract methods, and a class can derive from only one. An interface lists members only and a class may implement several; members are public and, before C# 8, bodiless. Use an abstract class when subclasses share state and code (all shapes have a name); use an interface to say that unrelated types support a capability (an `Employee` and a `Contractor` are both `IPayable`; `string` and `int` are both `IComparable`). In Section 3.13, `Employee` implements `IPayable`, `IReportable` and `IComparable<Employee>`: `Array.Sort(team)` orders employees by salary through `CompareTo`, the payroll loop treats `Employee` and `Contractor` identically through `IPayable`, and an explicit implementation hides `Report` from the class's own public surface. The program was compiled and run; the payroll total is 65,000 + 72,000 + 48,000 = 185,000.
