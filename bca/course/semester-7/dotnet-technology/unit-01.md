---
subject: DotNet Technology
grade: BCA Semester 7 (Elective II)
unit: 1
title: Introducing C# and the .NET Framework
hours: 7
area: BCA 406 · DotNet Technology · Unit 1
---

A student in Butwal writes a small billing program in C#. On her laptop it runs on Windows; the same compiled file later runs unchanged on the college's Linux server and, with a rebuild, inside a phone app. She never decides how much memory each object needs, never frees it, and when she accidentally treats a text value as a number the program stops at once with a clear message instead of printing nonsense. All of this comes from the platform underneath the language. **C#** is the language you type; **.NET** is the platform that compiles, checks, runs and cleans up after it. This unit explains the idea of each part before Units 2 to 4 teach you to use them.

::: key What this unit gives you
- What C# and .NET are, how they developed, and why C# is called object oriented, type safe and memory managed.
- How source code becomes CIL, an assembly and finally machine code, and what the CLR does while the program runs.
- The framework class library, the other members of the .NET family (.NET Framework, .NET Core and .NET 5+, Mono, Xamarin, Unity) and .NET Standard 2.0.
- The technologies you will meet on top of the platform: console, Windows Forms, WPF, ASP.NET, ADO.NET and Entity Framework.
- Your first programs, run and explained line by line.
:::

## 1.1 What C# and .NET are

**C#** (pronounced "C sharp") is a general-purpose, statically typed, object-oriented language designed by Anders Hejlsberg's team at Microsoft. It first shipped in 2002 with .NET Framework 1.0 and Visual Studio .NET. It was standardised as ECMA-334 (and ISO/IEC 23270), so the language is not owned only by one product. New versions appear every November together with a new .NET release: C# 8 (2019) added nullable reference types, C# 9 (2020) records, C# 10 to 12 (2021 to 2023) global usings, file-scoped namespaces and primary constructors, and C# 13 and 14 (2024 and 2025) continued with refinements to `params`, `field` in properties and extension members. You do not need to memorise this history; remember that the language grows by adding features and almost never breaks old code.

**.NET** is the free, open-source (MIT licence) developer platform that runs C#. It consists of three things that you should keep apart in your mind:

| Part | What it is | Examples |
|---|---|---|
| Languages | The notations you write | C#, F#, Visual Basic |
| Runtime | The engine that loads, checks and runs programs and manages memory | CLR (Common Language Runtime) with the JIT compiler and garbage collector |
| Libraries | Ready-made classes you call | Base Class Library (BCL): `System`, `System.IO`, `System.Linq`, `System.Net.Http`, and more |

Add the **SDK** (software development kit: compiler, `dotnet` command-line tool, templates, build system) and an editor such as Visual Studio or Visual Studio Code, and you have everything required to build software. Anything written in a .NET language can use libraries written in another, because all of them compile to the same intermediate form, described in Section 1.5.

::: note A short timeline you can use in the exam
2002 .NET Framework 1.0 and C# 1.0. 2005 generics (C# 2.0). 2007 LINQ and lambdas (C# 3.0). 2012 `async` and `await` (C# 5.0). 2014 Roslyn, the open-source C# compiler. 2016 .NET Core 1.0, cross-platform. 2019 .NET Framework 4.8, the last version of the Windows-only line. 2020 .NET 5 joins .NET Framework and .NET Core into one product called ".NET". Since then one release per year; even-numbered releases (8, 10) are Long Term Support (LTS).
:::

## 1.2 Object orientation

An **object-oriented** language organises a program as a set of objects that hold data and the operations on that data, instead of as a long list of procedures. C# supports the four classic ideas:

| Idea | Meaning | C# feature (taught in Unit 3) |
|---|---|---|
| Encapsulation | Hide the data inside the object; expose a small, safe interface | `private` fields, properties, access modifiers |
| Inheritance | Build a new class from an existing one | `class Car : Vehicle`, `base` |
| Polymorphism | One call, different behaviour depending on the real object | `virtual` and `override`, interfaces |
| Abstraction | Describe what a thing does without saying how | `abstract` classes, `interface` |

Two properties of C# make its object orientation especially clean. First, **everything is an object in the type system**: every type, even `int`, derives from `System.Object`, so `5.ToString()` is legal. Second, C# has **single inheritance of classes but multiple interfaces**: a class has exactly one base class but may implement many interfaces, which avoids the ambiguity of multiple inheritance in C++.

C# is also a **multi-paradigm** language. Alongside objects it supports functional ideas (lambda expressions, LINQ, immutable records, pattern matching) and, through the `async` model, asynchronous programming. A top-level program can even contain statements without any class, which is how Section 1.9 starts.

::: example A class is a blueprint, an object is a thing built from it
`class Student { public string Name; public int Roll; }` describes what every student has. `new Student()` builds one student in memory. Ten `new Student()` calls make ten independent objects that share one description. Remember this sentence for any "define class and object" question.
:::

## 1.3 Type safety

A language is **type safe** when it stops you from using a value in a way its type does not allow. C# achieves this in three layers.

1. **Static checking at compile time.** Every variable, parameter and return value has a declared type, and the compiler rejects mismatches. `int n = "ten";` does not compile, and neither does calling a method that does not exist.
2. **Definite assignment.** The compiler proves that a local variable is given a value before it is read. Reading an unassigned variable is an error, not a random leftover number as in C.
3. **Checks at run time.** What cannot be proved at compile time is checked while the program runs: an invalid cast throws `InvalidCastException`, an array index outside the array throws `IndexOutOfRangeException`, and a call through a null reference throws `NullReferenceException`. The program never silently reads memory it does not own.

Arithmetic is also under control: integer overflow wraps around silently by default, but you can ask for checking with the `checked` keyword, which throws `OverflowException` (Unit 2). Unsafe pointer code exists, but it must be marked with the `unsafe` keyword and enabled in the project, so ordinary programs cannot have the buffer overflows that cause many security holes in C and C++.

The program below shows the run-time layer. The line `object o = "hello";` is legal because every string is an object, but the unboxing cast `(int)o` is wrong and is caught.

```csharp
using System;

public class TypeSafetyDemo
{
    public static void Main()
    {
        object o = "hello";
        try
        {
            int n = (int)o;                 // wrong: o holds a string
            Console.WriteLine(n);
        }
        catch (InvalidCastException)
        {
            Console.WriteLine("Caught InvalidCastException: a string is not an int.");
        }

        int[] marks = new int[3];
        try
        {
            marks[3] = 90;                  // valid indexes are 0, 1, 2
        }
        catch (IndexOutOfRangeException)
        {
            Console.WriteLine("Caught IndexOutOfRangeException: no memory outside the array is touched.");
        }

        int big = int.MaxValue;
        Console.WriteLine("unchecked: " + (big + 1));
        try { Console.WriteLine(checked(big + 1)); }
        catch (OverflowException) { Console.WriteLine("checked: OverflowException"); }
    }
}
```
```output
Caught InvalidCastException: a string is not an int.
Caught IndexOutOfRangeException: no memory outside the array is touched.
unchecked: -2147483648
checked: OverflowException
```

## 1.4 Memory management

In C a programmer must `malloc` and `free` memory by hand and one mistake gives a leak or a crash. In C# the runtime manages memory automatically. You need to know three things: where values live, how the garbage collector decides what to free, and what it cannot free.

**Stack and heap.** Each running method has a **stack frame** holding its local variables. Stack memory is released the moment the method returns. **Value types** (`int`, `double`, `bool`, `char`, `struct`, `enum`) store their data directly in the variable, so a local `int` lives on the stack (a value type that is a field of an object lives inside that object). **Reference types** (`class`, `string`, arrays, delegates, interfaces) store only a reference (an address) in the variable; the object itself is created on the **managed heap** by `new`.

**Garbage collection.** The **garbage collector (GC)** finds objects that no part of the running program can reach any more and reclaims their memory. A collection works in three steps: *mark* every object reachable from the **roots** (local variables, static fields, CPU registers), *sweep* away the unmarked ones, and *compact* the survivors so that free memory is one block. Because most objects die young, the heap is split into **generations**:

| Generation | Holds | Collected |
|---|---|---|
| 0 | newly created, short-lived objects | very often, very quickly |
| 1 | survivors of one collection; a buffer between short- and long-lived | less often |
| 2 | long-lived objects (caches, static data) | rarely; a full collection |
| Large Object Heap | objects of 85,000 bytes or more (big arrays, big strings) | together with generation 2 |

An object that survives a collection is promoted to the next generation. Collection starts when generation 0 fills up; you rarely call `GC.Collect()` yourself, and doing so usually hurts performance.

```svgfig label="1.1" caption="The managed heap. Local variables on the stack hold references to objects on the heap. A collection keeps the objects reachable from the roots (solid arrows), frees the unreachable one, and promotes survivors from generation 0 to 1."
f = Fig(600, 250)
f.text(90, 18, "Stack (method frames)", size=11, color=NAVY, bold=True)
f.box(20, 30, 140, 36, "int count = 3", fill=BLUE, stroke=NAVY, size=10)
f.box(20, 76, 140, 36, "Student s1", fill=BLUE, stroke=NAVY, size=10)
f.box(20, 122, 140, 36, "Student s2", fill=BLUE, stroke=NAVY, size=10)
f.text(380, 18, "Managed heap", size=11, color=TEAL, bold=True)
f.box(230, 30, 340, 90, "", fill=MINT, stroke=TEAL)
f.text(300, 44, "Generation 0", size=10, color=TEAL, bold=True)
f.box(246, 56, 90, 50, "Student\nRoll 1", fill="#ffffff", stroke=TEAL, size=10)
f.box(350, 56, 90, 50, "Student\nRoll 2", fill="#ffffff", stroke=TEAL, size=10)
f.box(454, 56, 100, 50, "Orphan\nno reference", fill=ROSE, stroke=RED, size=10, dash=True)
f.box(230, 134, 340, 44, "Generation 1  and  Generation 2 (survivors)", fill=SAND, stroke=AMBER, size=10)
f.box(230, 190, 340, 40, "Large Object Heap (85,000 bytes or more)", fill=SOFT, stroke=SLATE, size=10)
f.arrow([(160, 94), (246, 82)], color=NAVY)
f.arrow([(160, 140), (200, 140), (200, 110), (350, 100)], color=NAVY)
f.text(504, 124, "freed", size=9.5, color=RED, bold=True)
```

**What the GC does not manage.** The GC knows only about memory. A file handle, a database connection or a network socket is an *unmanaged resource* owned by the operating system, and the GC will not close it at a predictable time. Classes that hold such resources implement `IDisposable`; you release them deterministically with `using`:

```csharp
// noexec
using (var writer = new System.IO.StreamWriter("log.txt"))
{
    writer.WriteLine("saved");
}   // writer.Dispose() runs here, even if an exception was thrown
```
A **finalizer** (Unit 3) is a last-resort cleanup that the GC calls some time after an object becomes unreachable. Never rely on it to close files promptly.

The program below makes the generations visible. It allocates an object, shows its generation, forces a collection while the object is still referenced and shows that it was promoted, and then counts collections.

```csharp
// noexec
using System;

public class GcDemo
{
    class Student { public int Roll = 1; }

    public static void Main()
    {
        Student s = new Student();
        Console.WriteLine("Generation after creation: " + GC.GetGeneration(s));
        GC.Collect();
        Console.WriteLine("Generation after one collection: " + GC.GetGeneration(s));
        GC.Collect();
        Console.WriteLine("Generation after two collections: " + GC.GetGeneration(s));
        Console.WriteLine("Max generation: " + GC.MaxGeneration);
        GC.KeepAlive(s);   // s is still reachable up to this line
    }
}
```
```output
Generation after creation: 0
Generation after one collection: 1
Generation after two collections: 2
Max generation: 2
```

This is the typical output on .NET 8. Mono's collector numbers its generations differently, so this one program was not executed by the book's checking script; every other program in the book was.
::: caution Common misconceptions
"C# has no pointers": it has them, but only in `unsafe` code. "The GC closes my files": it frees memory, not operating-system resources, so use `using`. "Setting a variable to `null` frees the object immediately": it only removes one reference; the memory is reclaimed at the next collection that finds the object unreachable.
:::

## 1.5 C# and the CLR: from source code to a running program

A C# compiler does not produce machine code for a particular processor. It produces **CIL** (Common Intermediate Language, also called MSIL or IL): a compact, processor-independent instruction set. The CIL, together with **metadata** that describes every type, method and field, is stored in an **assembly**, a `.dll` or `.exe` file. Because the metadata is inside the file, the runtime and tools such as reflection can read the types without header files.

When you run the assembly, the **CLR (Common Language Runtime)** takes over:

1. The **class loader** finds and loads the assembly and the types the program uses.
2. The **verifier** checks that the CIL is type safe.
3. The **JIT (just-in-time) compiler** translates each method from CIL to native machine code the first time the method is called and keeps the result in memory for later calls. Modern runtimes also use *tiered compilation*: a quick first translation, then a better optimised one for methods that run often. **ReadyToRun** (partial ahead-of-time) and **Native AOT** can compile to native code before deployment for faster start-up.
4. The **execution engine** runs the native code and provides the services of Section 1.6.

```svgfig label="1.2" caption="From C# source to a running process. The compiler (Roslyn) produces CIL and metadata inside an assembly; at run time the CLR loads, verifies and JIT-compiles it, and the garbage collector and base class library support the running code."
f = Fig(620, 190)
f.box(10, 70, 90, 50, "C# source\nProgram.cs", fill=BLUE, stroke=NAVY, size=10)
f.box(135, 70, 100, 50, "C# compiler\n(Roslyn)", fill=SAND, stroke=AMBER, size=10)
f.box(270, 62, 110, 66, "Assembly\nCIL + metadata\n.dll / .exe", fill=MINT, stroke=TEAL, size=10)
f.box(415, 20, 195, 150, "", fill=SOFT, stroke=SLATE)
f.text(512, 36, "CLR (runtime)", size=11, color=NAVY, bold=True)
f.box(430, 48, 80, 34, "Loader and\nverifier", fill=BLUE, stroke=NAVY, size=9)
f.box(520, 48, 80, 34, "JIT\ncompiler", fill=BLUE, stroke=NAVY, size=9)
f.box(430, 92, 80, 34, "Garbage\ncollector", fill=BLUE, stroke=NAVY, size=9)
f.box(520, 92, 80, 34, "Exceptions,\nthreads", fill=BLUE, stroke=NAVY, size=9)
f.text(512, 150, "Native code runs on the CPU", size=10, color=TEAL, bold=True)
f.arrow([(100, 95), (135, 95)], color=NAVY)
f.arrow([(235, 95), (270, 95)], color=NAVY)
f.arrow([(380, 95), (415, 95)], color=NAVY)
```

The same assembly therefore runs on any operating system for which a runtime exists. This is the meaning of the old slogan "write once, run anywhere", with the difference from Java that the .NET JIT compiles methods straight to native code and that value types and generics are first-class in the instruction set.

**Managed and unmanaged code.** Code that runs under the CLR's control is *managed code*; the CLR guarantees type safety, memory management and exception handling for it. Code outside the CLR (a C library, the Windows API) is *unmanaged*. A C# program can call it through **P/Invoke** (`[DllImport]`), but then the safety guarantees stop at the border.

### Common Type System and Common Language Specification

The **CTS (Common Type System)** defines the types the runtime understands (classes, structs, interfaces, enums, delegates) and the rules for them, for example that every type derives from `System.Object`. C#'s `int` is the CTS type `System.Int32`; Visual Basic's `Integer` is the same type. The **CLS (Common Language Specification)** is a subset of the CTS rules that a public library should follow if it wants to be usable from every .NET language (for instance, not distinguishing two members only by upper and lower case, since Visual Basic is not case sensitive). Together they make **language interoperability** possible: a class written in F# can be inherited by a C# class.

The CLI (Common Language Infrastructure, ECMA-335) is the open standard that describes the CTS, CLS, CIL, metadata and the virtual execution system. The CLR is Microsoft's implementation of the CLI; Mono and the open-source CoreCLR are others.

### Assemblies and the .NET build outputs

| Term | Meaning |
|---|---|
| Assembly | The unit of deployment, versioning and security: one or more files with CIL, metadata and a *manifest* (name, version, references) |
| Namespace | A logical grouping of type names (`System.IO`); an assembly may contain several, and a namespace may span assemblies |
| Executable assembly | Has an entry point `Main`; on .NET 6+ the `.dll` is started by the `dotnet` host or by a generated apphost `.exe` |
| Library assembly | `.dll` without an entry point, referenced by other projects |
| NuGet package | A `.nupkg` zip containing assemblies and metadata, downloaded from nuget.org |
| GAC | Global Assembly Cache of .NET Framework; modern .NET prefers per-application copies |

The commands you will use most:

```text
dotnet new console -n Hello        create a console project
dotnet build                       compile to bin/Debug/netX.0/
dotnet run                         build and run
dotnet add package Newtonsoft.Json add a NuGet package
dotnet publish -c Release          produce files for deployment
```
## 1.6 CLR and the .NET Framework

The words ".NET Framework" are used in two senses, and the TU outline uses both. In the narrow sense, the **.NET Framework** is the original Windows-only implementation (versions 1.0 to 4.8). In the wide sense, "the .NET framework" is the layered platform of runtime plus class library plus tools. The wide sense is the one to describe in an answer:

```svgfig label="1.3" caption="Layers of the .NET platform. Applications sit on application models (ASP.NET, Windows Forms, WPF, MAUI); these use the base class library, which runs on the CLR, which runs on the operating system."
f = Fig(560, 250)
f.box(60, 14, 440, 40, "Your application (C#, F#, Visual Basic)", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(60, 62, 104, 44, "ASP.NET\nCore", fill=SAND, stroke=AMBER, size=10)
f.box(172, 62, 104, 44, "Windows\nForms, WPF", fill=SAND, stroke=AMBER, size=10)
f.box(284, 62, 104, 44, "MAUI\n(mobile)", fill=SAND, stroke=AMBER, size=10)
f.box(396, 62, 104, 44, "Console and\nservices", fill=SAND, stroke=AMBER, size=10)
f.box(60, 114, 440, 44, "Base Class Library: System, Collections, IO, Linq, Net, Data, Threading", fill=MINT, stroke=TEAL, size=10.5)
f.box(60, 166, 440, 40, "CLR: class loader, JIT compiler, garbage collector, exception handling, threads", fill="#ffffff", stroke=NAVY, size=10.5)
f.box(60, 214, 440, 30, "Operating system: Windows, Linux, macOS, Android, iOS", fill=SOFT, stroke=SLATE, size=10.5)
```

The services the CLR provides to every program are worth listing:

| Service | What it does |
|---|---|
| Loading and verification | Finds assemblies, checks that CIL is type safe |
| JIT compilation | Turns CIL into native code for the real processor |
| Garbage collection | Allocates and reclaims heap memory (Section 1.4) |
| Exception handling | One uniform `try`/`catch`/`finally` model across all languages |
| Thread management | Thread pool, synchronisation, the `Task` model |
| Security and sandboxing | Code access security in old .NET Framework; modern .NET relies on operating-system and container isolation |
| Interoperability | P/Invoke to native libraries, COM interop on Windows |
| Reflection | Reads metadata and creates types at run time |

## 1.7 Platform support and the other frameworks

Several products carry the .NET name. Students often mix them up, so keep this table:

| Implementation | Platforms | Status and use |
|---|---|---|
| **.NET Framework** (1.0 to 4.8.1) | Windows only | Ships with Windows; receives security fixes only; used by older desktop and ASP.NET Web Forms systems |
| **.NET Core** (1.0 to 3.1) | Windows, Linux, macOS | Open source rewrite from 2016; modular, fast, cloud friendly; ended with 3.1 |
| **.NET 5 and later** (5, 6, 7, 8, 9, 10) | Windows, Linux, macOS, plus Android and iOS through MAUI and WebAssembly through Blazor | The single current product; yearly releases, LTS in even years |
| **Mono** | Linux, macOS, Android, iOS, WebAssembly | Older open-source runtime; now maintained inside the .NET repository and used for mobile and WebAssembly workloads |
| **Xamarin** | Android and iOS | Mono-based mobile toolkit; replaced by **.NET MAUI** (Multi-platform App UI); Xamarin support ended in 2024 |
| **Unity** | Games on almost every device | Uses a C# scripting layer on Mono or IL2CPP |
| **UWP** and **WinUI** | Windows 10/11 devices | Modern Windows app models |

::: note Which one should a new project choose?
Choose the current LTS version of .NET (8 or 10). Choose .NET Framework only when you must maintain an existing Windows-only application that depends on Web Forms, WCF server or other technologies that did not move to modern .NET. Modern .NET runs the same C# code, starts faster, and deploys to Linux containers, which is why most hosting and job advertisements now ask for it.
:::

**Platform support** means three different things: the *development* platform (you can build on Windows, macOS or Linux with the SDK), the *target* platform (where the app runs), and the *API surface* available there. The Windows-only APIs (Windows Forms, WPF, the registry) are not available on Linux even though the CLR is. This is the main practical limit of "cross-platform".

## 1.8 Framework overview and .NET Standard 2.0

The **Base Class Library (BCL)** is the collection of classes that every .NET program may use. You will use these namespaces throughout the course:

| Namespace | Contents |
|---|---|
| `System` | Basic types (`Object`, `String`, `Int32`, `DateTime`, `Math`, `Console`, `Exception`) |
| `System.Collections`, `System.Collections.Generic` | `List<T>`, `Dictionary<TKey,TValue>`, `Queue<T>`, `Stack<T>`, `HashSet<T>` |
| `System.IO` | Files, directories, streams, readers and writers |
| `System.Linq` | Query operators over sequences |
| `System.Text` | `StringBuilder`, encodings, `System.Text.Json` |
| `System.Threading`, `System.Threading.Tasks` | Threads, `Task`, `async`/`await` |
| `System.Net`, `System.Net.Http` | Sockets and `HttpClient` |
| `System.Data` | ADO.NET: connections, commands, data sets |
| `System.Reflection` | Inspecting assemblies and types at run time |
| `System.Xml` | XML documents and readers |

Above the BCL sit the **application frameworks**: Windows Forms and WPF for desktop, ASP.NET Core for web, MAUI for mobile, and libraries such as Entity Framework Core and ML.NET.

### .NET Standard

By 2016 there were three runtimes (.NET Framework, .NET Core, Xamarin) with different sets of classes. A library author who wanted to serve all of them had to build three versions. **.NET Standard** solved this by defining a *specification of APIs* (not an implementation). If a class library targets `netstandard2.0`, it can be referenced from any runtime that implements that version of the standard.

| .NET Standard | Implemented by (minimum) | Note |
|---|---|---|
| 1.x | .NET Framework 4.5 to 4.6.1, .NET Core 1.0, ... | Small API set |
| **2.0** (2017) | .NET Framework 4.6.1, .NET Core 2.0, Mono 5.4, Xamarin | About 32,000 APIs; the broadest reach; the version named in the TU outline |
| 2.1 (2018) | .NET Core 3.0 and later, Mono, Xamarin | Larger API set; **not** supported by .NET Framework |

Today .NET Standard is in maintenance. For new code, target `net8.0` (or later) for applications, and use `netstandard2.0` only for a library that must still work with .NET Framework. A project can list several targets, for example `<TargetFrameworks>netstandard2.0;net8.0</TargetFrameworks>`, to give each runtime the best version.

### Applied technologies

| Technology | Use |
|---|---|
| Console applications | Tools, scripts, learning, background workers |
| Windows Forms | Event-driven desktop forms with drag-and-drop designers; simple business applications |
| WPF (Windows Presentation Foundation) | Desktop applications with XAML markup, data binding and rich graphics |
| ASP.NET Core | Web sites (MVC, Razor Pages, Blazor), web APIs and real-time services (SignalR) |
| ADO.NET and Entity Framework Core | Database access (Unit 4) |
| .NET MAUI | One C# code base for Android, iOS, Windows and macOS apps |
| WCF and gRPC | Service communication; WCF for older SOAP systems, gRPC for modern services |
| ML.NET | Machine learning in C# |
| Azure Functions and containers | Cloud-hosted .NET code |

## 1.9 Your first programs

Install the **.NET SDK** from dotnet.microsoft.com (or with `winget`, `apt`, `brew`) and check it with `dotnet --version`. Then create and run a project:

```text
dotnet new console -n Hello
cd Hello
dotnet run
```

In .NET 6 and later, the template creates a *top-level program* of one line. The compiler wraps the statements in a hidden `Main` method:

```csharp
// noexec
Console.WriteLine("Hello, Nepal!");
```

The same program written out in full, the way older books and the exam show it, is below. Every line is explained after the output.

```csharp
using System;

namespace Hello
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, Nepal!");
            Console.WriteLine("Arguments received: " + args.Length);
        }
    }
}
```
```output
Hello, Nepal!
Arguments received: 0
```

1. `using System;` imports the namespace so that `Console` can be written without the prefix `System.`.
2. `namespace Hello { ... }` groups the types of this program and prevents clashes with names from other libraries.
3. `class Program` declares a class; in C# every method must belong to a type.
4. `static void Main(string[] args)` is the **entry point**. It is `static` so that the runtime can call it without creating an object, `void` because it returns nothing (it may return `int` as an exit code), and `args` holds the command-line arguments. C# is case sensitive, so `main` is not an entry point.
5. `Console.WriteLine` writes the text and a new line to standard output.

The next program reads input, uses a variable, a condition and string interpolation, and shows the basic shape of the console programs you will write in the laboratory. (The comment on the first line supplies the typed input in this book's checking script.)

```csharp
// stdin: 42
using System;

class Grade
{
    static void Main()
    {
        Console.Write("Enter your mark: ");
        int mark = int.Parse(Console.ReadLine());
        string result = mark >= 40 ? "Pass" : "Fail";
        Console.WriteLine($"Mark {mark}: {result}");
    }
}
```
```output
Enter your mark: Mark 42: Pass
```

The typed input was `42` (not echoed in the captured output).

A **Windows Forms** "hello" has the same logic in an event handler and is compiled but not run here, because the sandbox that checks the book's code has no screen:

```csharp
// compile-only
using System;
using System.Windows.Forms;

class HelloForm : Form
{
    HelloForm()
    {
        Text = "Hello";
        Button b = new Button { Text = "Click me", Left = 20, Top = 20 };
        b.Click += (s, e) => MessageBox.Show("Hello, Nepal!");
        Controls.Add(b);
    }

    [STAThread]
    static void Main() { Application.Run(new HelloForm()); }
}
```

::: caution Three first-day errors
(1) A missing semicolon gives `CS1002: ; expected`; read the line number. (2) `Console.ReadLine()` returns `string`, so you must convert with `int.Parse` or `int.TryParse`. (3) C# is case sensitive: `console.writeline` fails, `Console.WriteLine` works.
:::
## 1.10 Summary and exercises

C# is a statically typed, object-oriented language; .NET is the platform of runtime, libraries and tools that runs it. The compiler produces CIL and metadata in an assembly; the CLR loads, verifies, JIT-compiles and runs it, and the garbage collector reclaims heap memory by generations. Type safety is enforced at compile time and at run time. .NET Framework (Windows only), .NET Core and .NET 5 or later, Mono and Xamarin are different implementations; .NET Standard 2.0 is the API specification that let one library serve several of them; today's choice is the current LTS release of .NET.

1. Define C# and .NET. State the difference between a language, a runtime and a class library.
2. List the four principles of object orientation and give one C# feature for each.
3. What is type safety? Name three ways in which C# enforces it.
4. Explain value types and reference types with the places where they are stored.
5. Describe generational garbage collection. Why does it improve performance?
6. Why does the GC not remove the need for `using` and `IDisposable`?
7. What is CIL? Why does .NET compile to CIL instead of directly to machine code?
8. Explain the work of the CLR. Draw the compilation and execution process.
9. Distinguish CTS, CLS and CLI. How do they provide language interoperability?
10. What is an assembly? What does it contain?
11. Compare .NET Framework, .NET Core and .NET 5+. Where do Mono and Xamarin fit?
12. What is .NET Standard 2.0? Why was it introduced and why is it less important today?
13. List five namespaces of the base class library and the types they hold.
14. Write a C# program that reads two integers and prints their sum, and explain each line.
15. What is the role of `Main`? What happens if a program has two `Main` methods?

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the CLR and its services.**

The Common Language Runtime is the execution engine of .NET. It loads assemblies, verifies that their CIL is type safe, compiles each method from CIL to native code just in time, runs the code and provides services while it runs: automatic memory management by the garbage collector, a uniform exception-handling model, thread management, security and isolation, and interoperability with native code through P/Invoke. Code that runs under this control is called managed code. Because the CLR works on CIL, a program written in any .NET language receives the same services.

**Q2 (5 marks). Distinguish value types and reference types.**

| Point | Value type | Reference type |
|---|---|---|
| Examples | `int`, `double`, `bool`, `char`, `struct`, `enum` | `class`, `string`, arrays, delegates, interfaces |
| Contents of the variable | the data itself | a reference to an object on the heap |
| Assignment `b = a` | copies the data; `a` and `b` are independent | copies the reference; both refer to the same object |
| Default value | zero or false | `null` |
| Memory | usually the stack (or inside the owning object) | the managed heap, reclaimed by the GC |

**Q3 (5 marks). Explain generational garbage collection.**

The managed heap is divided into generations 0, 1 and 2 (plus the large object heap for objects of 85,000 bytes or more). New objects start in generation 0. When it fills, the GC marks all objects reachable from the roots, frees the rest, compacts the survivors and promotes them to generation 1; survivors of a generation 1 collection move to generation 2. Because most objects die young, collecting generation 0 is cheap and frequent, and the expensive full collection of generation 2 is rare. The pause time of an average collection is therefore short.

**Q4 (10 marks). Describe how a C# program is compiled and executed in .NET. Draw a diagram.**

1. *Write* the source in a `.cs` file. 2. The **C# compiler (Roslyn)** checks the syntax and types and produces an **assembly** (`.dll` or `.exe`) that contains CIL, metadata and a manifest; no machine code is produced yet (Figure 1.2). 3. When the program is started, the **CLR** loads the assembly and the types it needs. 4. The **verifier** checks that the CIL is type safe. 5. The **JIT compiler** translates each method into native code for the actual processor the first time the method is called; the native code is cached for later calls. Tiered compilation re-optimises hot methods. 6. The native code runs under the CLR, which allocates objects, collects garbage, handles exceptions and manages threads. 7. When the process ends, the runtime releases its resources.

The advantages of this two-step design are: one assembly runs on every platform with a runtime; all languages share one runtime and one class library; the JIT can use the features of the processor in use; and the runtime can verify safety. The costs are a start-up delay for JIT compilation, reduced by ReadyToRun and Native AOT.

**Q5 (10 marks). Compare .NET Framework, .NET Core and modern .NET, and explain the role of .NET Standard.**

.NET Framework (2002 to 2019, final version 4.8) runs only on Windows, is installed with the operating system and supports Windows Forms, WPF, ASP.NET Web Forms and WCF; it now receives only security and reliability fixes. .NET Core (2016) was a new, modular, open-source and cross-platform runtime with a smaller footprint and better performance; it supports ASP.NET Core, console apps and later desktop apps on Windows. In 2020 .NET 5 merged the lines under the name ".NET" with a single base class library and yearly releases (even versions are LTS). Mono and Xamarin, the older open-source implementation and its mobile toolkit, were absorbed: Mono now powers Blazor WebAssembly and mobile builds, and .NET MAUI replaced Xamarin.

Before the merger a library author had to build separately for each runtime. **.NET Standard** was a formal list of APIs: a library targeting `netstandard2.0` ran on .NET Framework 4.6.1 or later, .NET Core 2.0 or later, Mono and Xamarin. Version 2.1 added APIs but dropped .NET Framework. Since .NET 5 all new runtimes share one library, so new libraries target `net8.0` or later; `netstandard2.0` remains useful only when .NET Framework consumers must be supported.
