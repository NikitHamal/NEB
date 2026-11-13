# DotNet Technology - BCA 406 (Semester VII, Elective II, 3 credits)

Study notes for the TU DotNet Technology elective (course code CACS302 in the TU outline, Year III/IV, 6 hours a week: 3 theory and 3 practical). Four units follow the outline, its topic order and its hours (7, 12, 12 and 14).

| Unit | Title | Hours | Outline topics covered |
|---|---|---|---|
| 1 | Introducing C# and the .NET Framework | 7 | object orientation, type safety, memory management, platform support, C# and CLR, CLR and .NET Framework, other frameworks, framework overview, .NET Standard 2.0, applied technologies |
| 2 | The C# Language Basics | 12 | console and GUI applications, identifiers and keywords, comments, data types, expressions and operators, strings and characters, arrays, variables and parameters, statements, namespaces |
| 3 | Creating Types in C# | 12 | classes, constructors and deconstructors, `this`, properties, indexers, static constructors and classes, finalizers, dynamic binding, operator overloading, inheritance, abstract classes, `base`, overloading, `object`, structs, access modifiers, interfaces, enums, generics |
| 4 | Advanced C# | 14 | delegates, events, lambda expressions, exception handling, LINQ, working with databases (ADO.NET, EF Core overview), ASP.NET (Core MVC, Razor Pages, minimal APIs, middleware, Web Forms); plus async/await, files and the laboratory map |

## Verification

Every `csharp` code block is compiled and run by `bca/tools/fill_cs_outputs.py` (Mono `mcs`, C# 7, with `Mono.Data.Sqlite` for the ADO.NET programs) and the printed output in the book is the real output of that run. Blocks marked `// compile-only` (Windows Forms) are compiled but not run because the sandbox has no screen; blocks marked `// noexec` show syntax newer than C# 7 (switch expressions, top-level statements, records, EF Core, ASP.NET Core) or need packages Mono lacks, and their behaviour is described in the text. One program (the garbage-collector generation demo, Section 1.4) is not run by the script because Mono's collector numbers its generations differently from .NET; the typical .NET output is given and labelled. Namespaces, class names and method names for ADO.NET with SQLite are identical in `Microsoft.Data.Sqlite`, and the text states the changes needed for SQL Server.

## Source and honesty

Units, topics and hours follow the TU CACS302 outline (Introducing C# and the .NET Framework 7 h; The C# Language Basics 12 h; Creating Types in C# 12 h; Advanced C# 14 h) as reproduced at notebahadur.com and edu-mate.com; the main text of the syllabus is Joseph and Ben Albahari, *C# 7.0 in a Nutshell*. The elective list of the revised curriculum names DotNet Technology among the Elective II options; each college runs a subset. Release dates and version numbers of .NET and C# (up to .NET 10 and C# 14) are stated as widely published; check dotnet.microsoft.com for the current LTS version. Nothing here has had a subject-teacher review.
