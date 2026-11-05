---
subject: Web Technology II
grade: BCA Semester 4
unit: 5
title: Object-Oriented Programming in PHP
hours: 7
area: BCA 255 · Web Technology II · Unit 5
---

Modern PHP applications and frameworks such as Laravel are built from classes. If you know Java (Semester II) or Python classes (Unit 6 of the Python book), PHP's object model will feel familiar, with its own syntax: `->` for members, `::` for static members, and `$this`.

::: key What this unit gives you
- Classes and objects, properties and methods, constructors and destructors.
- Visibility and encapsulation; inheritance, overriding, polymorphism.
- Static members, abstract classes, interfaces, traits; exceptions.
:::

## 5.1 Classes, objects, constructors and destructors

```php
<?php
class Student {
    public static int $count = 0;
    public function __construct(private string $name, private array $marks = []) {   // constructor promotion (PHP 8)
        self::$count++;
    }
    public function addMark(int $m): static { $this->marks[] = $m; return $this; }
    public function average(): float { return $this->marks ? array_sum($this->marks) / count($this->marks) : 0.0; }
    public function getName(): string { return $this->name; }
    public function __toString(): string { return sprintf("%s (avg %.1f)", $this->name, $this->average()); }
    public function __destruct() { echo "[{$this->name} destroyed]\n"; }
}
$s = new Student("Sita");
$s->addMark(88)->addMark(92)->addMark(75);
echo $s, " | ", Student::$count, "\n";
$t = new Student("Ram", [70, 64]);
echo $t, " | ", Student::$count, " | ", $t instanceof Student ? "is a Student" : "", "\n";
unset($t);
echo "end of script\n";
```
```output
Sita (avg 85.0) | 1
Ram (avg 67.0) | 2 | is a Student
[Ram destroyed]
end of script
[Sita destroyed]
```
A **class** declares **properties** and **methods**; `new` creates an **object**; `$this` is the current object; `->` accesses members. `__construct` runs on creation (PHP 8's *constructor promotion* declares and assigns properties in the parameter list); `__destruct` runs when the last reference disappears (here at `unset`, and for `$s` at script end). `__toString` lets `echo $object` work. Returning `$this` allows **method chaining**.

## 5.2 Visibility and encapsulation

| Modifier | Accessible from |
|---|---|
| `public` | anywhere |
| `protected` | the class and its subclasses |
| `private` | the declaring class only |

Keep properties `private`/`protected` and expose behaviour through methods, with validation in setters. `readonly` properties (PHP 8.1) can be set once.

```php
<?php
class Account {
    public function __construct(public readonly string $owner, private float $balance = 0) {}
    public function deposit(float $amt): void {
        if ($amt <= 0) throw new InvalidArgumentException("deposit must be positive");
        $this->balance += $amt;
    }
    public function getBalance(): float { return $this->balance; }
}
$a = new Account("Ram", 100);
$a->deposit(50);
echo $a->owner, " ", $a->getBalance(), "\n";
try { $a->balance = 1; } catch (Error $e) { echo get_class($e), ": ", $e->getMessage(), "\n"; }
try { $a->owner = "Hari"; } catch (Error $e) { echo get_class($e), ": ", $e->getMessage(), "\n"; }
try { $a->deposit(-5); } catch (InvalidArgumentException $e) { echo "rejected: ", $e->getMessage(), "\n"; }
```
```output
Ram 150
Error: Cannot access private property Account::$balance
Error: Cannot modify readonly property Account::$owner
rejected: deposit must be positive
```
## 5.3 Inheritance, overriding and polymorphism

```php
<?php
class Employee {
    public function __construct(protected string $name, protected float $base) {}
    public function pay(): float { return $this->base; }
    public function describe(): string { return static::class . ": {$this->name} earns " . number_format($this->pay()); }
}
class Manager extends Employee {
    public function __construct(string $name, float $base, private float $bonus) { parent::__construct($name, $base); }
    public function pay(): float { return parent::pay() + $this->bonus; }
}
final class Intern extends Employee {
    public function pay(): float { return $this->base * 0.5; }
}
$staff = [new Employee("Hari", 40000), new Manager("Gita", 60000, 15000), new Intern("Bikash", 20000)];
foreach ($staff as $e) { echo $e->describe(), "\n"; }
echo array_sum(array_map(fn(Employee $e) => $e->pay(), $staff)), " ", $staff[1] instanceof Employee ? "Manager is an Employee" : "", "\n";
```
```output
Employee: Hari earns 40,000
Manager: Gita earns 75,000
Intern: Bikash earns 10,000
125000 Manager is an Employee
```
`extends` inherits; `parent::` calls the parent version; **overriding** replaces a method; **polymorphism**: the loop calls `pay()` and each object responds according to its class (late binding; `static::class` gives the real class). PHP has **single inheritance**; `final` prevents extension or overriding.

## 5.4 Abstract classes, interfaces and traits

```php
<?php
interface Payable { public function amount(): float; }
abstract class Shape {
    abstract public function area(): float;
    public function report(): string { return sprintf("%s area %.2f", static::class, $this->area()); }
}
trait Loggable {
    private array $log = [];
    public function log(string $m): void { $this->log[] = $m; }
    public function logs(): array { return $this->log; }
}
class Circle extends Shape implements Payable {
    use Loggable;
    public function __construct(private float $r) {}
    public function area(): float { return M_PI * $this->r ** 2; }
    public function amount(): float { return $this->area() * 10; }
}
$c = new Circle(2);
$c->log("created");
echo $c->report(), " | price ", round($c->amount(), 1), " | ", implode(",", $c->logs()), "\n";
try { $x = new Shape(); } catch (Error $e) { echo $e->getMessage(), "\n"; }
var_dump($c instanceof Payable, $c instanceof Shape);
```
```output
Circle area 12.57 | price 125.7 | created
Cannot instantiate abstract class Shape
bool(true)
bool(true)
```
An **abstract class** cannot be instantiated and may declare abstract methods that subclasses must implement. An **interface** lists methods a class promises to provide; a class may implement many. A **trait** is a reusable bundle of methods and properties inserted with `use`, a workaround for single inheritance.

## 5.5 Static members, constants and class methods

```php
<?php
class MathUtil {
    const PI = 3.14159;
    private static array $cache = [];
    public static function fib(int $n): int {
        return self::$cache[$n] ??= $n < 2 ? $n : self::fib($n - 1) + self::fib($n - 2);
    }
    public static function circle(float $r): float { return static::PI * $r * $r; }
}
echo MathUtil::fib(40), " ", MathUtil::circle(2), " ", MathUtil::PI, "\n";
class Config {
    private static ?Config $instance = null;
    private function __construct(public array $data = ["site" => "BCA Portal"]) {}
    public static function get(): Config { return self::$instance ??= new Config(); }
}
var_dump(Config::get() === Config::get());
```
```output
102334155 12.56636 3.14159
bool(true)
```
`static` members belong to the class, not to objects (`ClassName::member`; `self::` inside). `const` defines class constants. The **singleton** pattern above (private constructor, static accessor) guarantees a single shared object, for example a database connection.

## 5.6 Exceptions

```php
<?php
class InsufficientFunds extends RuntimeException {
    public function __construct(public readonly float $short) { parent::__construct("short by $short"); }
}
function withdraw(float $balance, float $amt): float {
    if ($amt <= 0) throw new InvalidArgumentException("amount must be positive");
    if ($amt > $balance) throw new InsufficientFunds($amt - $balance);
    return $balance - $amt;
}
foreach ([300, 5000, -1] as $amt) {
    try {
        echo "left: ", withdraw(1000, $amt), "\n";
    } catch (InsufficientFunds $e) {
        echo "refused: ", $e->getMessage(), "\n";
    } catch (InvalidArgumentException | TypeError $e) {
        echo "invalid: ", $e->getMessage(), "\n";
    } finally {
        echo "(checked $amt)\n";
    }
}
```
```output
left: 700
(checked 300)
left: refused: short by 4000
(checked 5000)
left: invalid: amount must be positive
(checked -1)
```
`throw` raises an exception object; `catch` handles it; `finally` always runs. Custom exceptions extend `Exception`/`RuntimeException`. PHP 7+ also throws `Error` (and `TypeError`, `DivisionByZeroError`) for engine problems.

## 5.7 Seeing the ideas: classes, objects and contracts

A class is a design and an object is one thing made from it, exactly as a cookie cutter is a shape and every biscuit pressed from it is a cookie. The plate shows this everyday picture beside the PHP version, and the figures then show visibility, inheritance, interfaces and exceptions with the real results of PHP 8.2.35.

```photogrid label="5.1" cols="2" ratio="1.5" caption="Class and object. (a) A tin cookie cutter is the class: one fixed shape that says what every product will look like. Each biscuit pressed from it is an object, a separate thing with its own state (one may be burnt, one may have a chocolate chip) but the same shape. (b) In PHP the keyword class describes the shape, and new Student(...) presses an object; the static counter belongs to the class, not to any single object."
@ photo id="bca254/cutter" cap="Cookie cutter: the class"
fit 1.5
focus 0.5 0.5
@ svg cap="One class, three objects, one shared counter"
f = Fig(450, 300)
f.box(110, 8, 230, 84, "", fill=BLUE, stroke=NAVY)
f.text(225, 28, "class Student", size=16, color=NAVY, bold=True)
f.text(225, 52, "name, marks   addMark()   average()", size=12.5, color=SLATE)
f.text(225, 76, "static count = 3 (one copy)", size=13, color=AMBER, bold=True)
for i, (n, m) in enumerate([("Sita", "85.0"), ("Ram", "67.0"), ("Hari", "71.5")]):
    x = 8 + i * 148
    f.arrow([(225, 94), (x + 66, 150)], color=SLATE, sw=1.5)
    f.box(x, 152, 132, 130, "", fill=MINT, stroke=TEAL)
    f.text(x + 66, 176, "object " + str(i + 1), size=13, color=TEAL, bold=True)
    f.text(x + 66, 206, n, size=15, color=SLATE, bold=True)
    f.text(x + 66, 236, "avg " + m, size=14, color=SLATE)
    f.text(x + 66, 264, "own data", size=12.5, color=TEAL)
```

```svgfig label="5.1" caption="Visibility in PHP, with the real error messages. A public member can be read from anywhere. A protected member can be used inside the class and in classes that extend it, but outside code gets the fatal Error 'Cannot access protected property' with the class and the property name. A private member is visible only inside the class that declares it: even the subclass B does not see it (its own access to the name finds nothing, so the real output shows 'undefined'), and outside code gets the same kind of Error for a private property. Making data private and offering methods is called encapsulation."
f = Fig(580, 214)
cols = [("Where the code is", 8, 160), ("public", 176, 120), ("protected", 304, 130), ("private", 442, 130)]
for t, x, w in cols:
    f.box(x, 8, w, 28, t, fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
rows = [("inside the class", ["yes", "yes", "yes"]), ("inside a subclass B", ["yes", "yes", "no"]), ("outside code", ["yes", "Error", "Error"])]
for i, (lab, vals) in enumerate(rows):
    y = 44 + i * 38
    f.box(8, y, 160, 32, lab, fill=SOFT, stroke=SLATE, size=10.5, bold=True, r=3)
    for (t, x, w), v in zip(cols[1:], vals):
        ok = v == "yes"
        f.box(x, y, w, 32, v, fill=MINT if ok else ROSE, stroke=TEAL if ok else RED, size=11.5, bold=True, r=3)
f.text(8, 170, "real messages from PHP 8.2", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(8, 188, "outside, protected:  Cannot access protected property A::$pro", size=10, color=RED, anchor="start")
f.text(8, 204, "outside, private:     Cannot access private property A::$pri", size=10, color=RED, anchor="start")
```

```svgfig label="5.2" caption="Inheritance and polymorphism with an abstract class. Shape declares the abstract method area() and the concrete method describe(); it cannot be instantiated (real message: Cannot instantiate abstract class Shape). Circle and Rect extend it and each supplies its own area(). The same call describe() on three different objects gives three different results, which is polymorphism: Circle of radius 7 gives 153.94, Rect 4 by 5 gives 20.00 and Rect 3 by 3 gives 9.00, a total of 182.94."
f = Fig(580, 218)
f.box(180, 8, 220, 58, "", fill=SAND, stroke=AMBER)
f.text(290, 26, "abstract class Shape", size=11.5, color=AMBER, bold=True)
f.text(290, 44, "abstract area(): float", size=10, color=SLATE)
f.text(290, 58, "describe() uses area()", size=10, color=SLATE)
f.line(290, 66, 290, 84, color=SLATE, sw=1.4)
f.line(110, 84, 470, 84, color=SLATE, sw=1.4)
f.line(110, 84, 110, 98, color=SLATE, sw=1.4)
f.line(470, 84, 470, 98, color=SLATE, sw=1.4)
f.box(10, 98, 200, 54, "", fill=MINT, stroke=TEAL)
f.text(110, 116, "class Circle", size=11.5, color=TEAL, bold=True)
f.text(110, 134, "area() = pi x r squared", size=10, color=SLATE)
f.box(370, 98, 200, 54, "", fill=MINT, stroke=TEAL)
f.text(470, 116, "class Rect", size=11.5, color=TEAL, bold=True)
f.text(470, 134, "area() = w x h", size=10, color=SLATE)
res = [("Circle(7)", "153.94"), ("Rect(4, 5)", "20.00"), ("Rect(3, 3)", "9.00")]
for i, (a, b) in enumerate(res):
    x = 10 + i * 146
    f.box(x, 166, 136, 34, "", fill="#ffffff", stroke=NAVY, r=4)
    f.text(x + 68, 178, a, size=10, color=SLATE, bold=True)
    f.text(x + 68, 192, "area " + b, size=10, color=NAVY, bold=True)
f.text(500, 178, "total", size=11, color=TEAL, bold=True)
f.text(500, 194, "182.94", size=12, color=TEAL, bold=True)
f.text(290, 212, "same call describe(), three different results", size=10, color=NAVY, bold=True)
```

```svgfig label="5.3" caption="Three ways to share design, compared. An abstract class is a partly finished parent: it may hold data and finished methods, and a class can extend only one. An interface is a pure contract of method names with no code, and a class may implement many of them. A trait is a bundle of finished methods and properties that is copied into any class with use. In the real run, class Wallet implements Payable and uses the trait Logs: two payments of 50 and 25.5 were logged (count 2) and the object is an instance of the interface Payable."
f = Fig(580, 196)
heads = [("abstract class", AMBER, SAND), ("interface", NAVY, BLUE), ("trait", TEAL, MINT)]
rows = [("holds code", ["yes, partly", "no", "yes"]), ("holds data", ["yes", "constants only", "yes"]), ("how many per class", ["one (extends)", "many (implements)", "many (use)"]), ("object possible", ["no", "no", "no"]), ("main purpose", ["common base", "a contract", "reuse code"])]
for j, (h, st, fl) in enumerate(heads):
    f.box(150 + j * 146, 8, 138, 28, h, fill=fl, stroke=st, size=11.5, bold=True, r=3)
for i, (lab, vals) in enumerate(rows):
    y = 42 + i * 28
    f.box(8, y, 136, 24, lab, fill=SOFT, stroke=SLATE, size=10, bold=True, r=3)
    for j, v in enumerate(vals):
        f.box(150 + j * 146, y, 138, 24, v, fill="#ffffff", stroke=heads[j][1], size=10, r=3)
f.text(8, 196 - 10, "real run: Wallet implements Payable + use Logs, two payments logged, count 2", size=10, color=TEAL, bold=True, anchor="start")
```

```svgfig label="5.4" caption="Exception flow with finally, from a real run of the withdraw function. Withdrawing 40 from a balance of 100 prints 'ok', the finally block runs, and the function returns done. Withdrawing 400 throws InsufficientFunds (a class that extends Exception, so it is also a Throwable): PHP leaves the try block at once, the matching catch prints the message 'need 400, have 100', the finally block still runs, and the function returns failed. The finally block runs in both paths, which makes it the right place to close files and connections."
f = Fig(580, 188)
f.box(8, 8, 120, 40, "try { ... }", fill=BLUE, stroke=NAVY, size=12, bold=True)
f.arrow([(130, 28), (190, 28)], color=TEAL, sw=1.6)
f.text(160, 18, "no error", size=9.5, color=TEAL, bold=True)
f.box(192, 8, 130, 40, "ok  (draw 40)", fill=MINT, stroke=TEAL, size=11, bold=True)
f.arrow([(68, 50), (68, 100)], color=RED, sw=1.6)
f.text(112, 78, "throw", size=9.5, color=RED, bold=True)
f.box(8, 102, 160, 52, "", fill=ROSE, stroke=RED)
f.text(88, 120, "catch InsufficientFunds", size=10.5, color=RED, bold=True)
f.text(88, 138, "need 400, have 100", size=10, color=SLATE)
f.arrow([(170, 128), (360, 128)], color=SLATE, sw=1.4)
f.arrow([(257, 50), (257, 80), (420, 80), (420, 100)], color=SLATE, sw=1.4)
f.box(362, 102, 208, 52, "", fill=SAND, stroke=AMBER)
f.text(466, 120, "finally { ... }", size=11.5, color=AMBER, bold=True)
f.text(466, 138, "runs in BOTH paths", size=10.5, color=SLATE)
f.text(8, 176, "draw(100, 40): ok finally -> done", size=10, color=TEAL, bold=True, anchor="start")
f.text(300, 176, "draw(100, 400): caught finally -> failed", size=10, color=RED, bold=True, anchor="start")
```

### 5.7.1 Eight advantages of object-oriented programming in PHP

1. **Data and actions stay together.** A `Student` object holds its marks and has its own `average()` method. The code that works with marks is found in one place and not scattered across the page. A result system for a college stays easy to read as it grows.
2. **Encapsulation protects data.** Private properties can be changed only through methods that check the new value (Fig. 5.1). A mark of 150 can be refused inside `addMark()`. No other script can break the rule by accident.
3. **Inheritance avoids repeated code.** A `Circle` and a `Rect` take the shared `describe()` from `Shape` and write only what is different (Fig. 5.2). A bug fixed in the parent is fixed for every child. A school system can reuse one `Person` class for students and teachers.
4. **Polymorphism removes long `if` chains.** The code calls `$shape->area()` and each object does the right thing. A new shape needs a new class and no change in the old code. This keeps a payment page open to new payment methods.
5. **Interfaces give a contract.** A class that implements `Payable` promises to have a `pay()` method, so the rest of the program can use any such class. eSewa-style and bank-card payers can be exchanged without rewriting the checkout. This helps teams who work on different parts.
6. **Traits share code across unrelated classes.** A logging trait can be added to a `Wallet`, an `Order` and a `Report` (Fig. 5.3). PHP allows only one parent class, and traits remove that limit. The same code is not copied three times.
7. **Exceptions separate errors from normal code.** The normal path stays short, and the `catch` block handles the failure in one place (Fig. 5.4). The `finally` block closes files and connections in both cases. A failed fee payment can therefore be reported clearly to the user.
8. **Modern frameworks are built on classes.** Laravel, Symfony and WordPress plugins are all written with classes, namespaces and interfaces. A student who understands objects can read their code and extend it. This is also the way large Nepali software teams organise their projects.

```photogrid label="5.2" cols="2" ratio="1.2" caption="Encapsulation as a safety rule. (a) One cookie cutter is the class and every cookie cut from it is an object: the shape is written once and many objects share it. (b) A bank account that exposes its balance as a public field lets any code subtract any amount. In a simulation of 10,000 accounts, each with five random withdrawals of Rs 50 to 300 from Rs 1,000 (fixed seed), 1,254 accounts (13 per cent) ended below zero, Rs 161,350 overdrawn in total. The same accounts with a private balance and a withdraw method that checks the amount refused 1,298 bad requests and none went negative. The logic is modelled in Python but is exactly what a PHP class with a private property and a public method does, and it is the practical reason for the visibility keywords."
@ photo id="bcawt/cookies" cap="One cutter (class), many cookies (objects)"
fit 1.2
focus 0.5 0.5
@ svg cap="10,000 accounts: public field vs checked method"
import random
random.seed(2081)
class Open:
    def __init__(self):
        self.balance = 1000
class Safe:
    def __init__(self):
        self._b = 1000
        self.refused = 0
    def withdraw(self, x):
        if 0 < x <= self._b:
            self._b -= x
        else:
            self.refused += 1
    @property
    def balance(self):
        return self._b
A = 10000
neg = 0
lost = 0
refused = 0
for _ in range(A):
    o, s = Open(), Safe()
    for _ in range(5):
        x = random.choice([50, 100, 150, 200, 300])
        o.balance -= x
        s.withdraw(x)
    if o.balance < 0:
        neg += 1
        lost += -o.balance
    refused += s.refused
    assert s.balance >= 0
assert neg > 0
facts = dict(A=format(A, ","), neg=format(neg, ","), pct=round(100 * neg / A), lost=format(lost, ","), ref=format(refused, ","))
f = Fig(300, 236)
f.text(150, 12, "5 random withdrawals from Rs 1,000, per account", size=10.5, color=NAVY, bold=True)
f.box(8, 26, 134, 70, "public field\n$acct->balance -= x", fill="#fecaca", stroke=RED, size=10.5, bold=True, r=4, sw=1)
f.box(158, 26, 134, 70, "private + method\nwithdraw(x) checks", fill="#bbf7d0", stroke=TEAL, size=10.5, bold=True, r=4, sw=1)
f.text(75, 118, "%s negative" % format(neg, ","), size=12, color=RED, bold=True)
f.text(75, 136, "accounts of %s" % format(A, ","), size=10.5, color=RED)
f.text(225, 118, "0 negative", size=12, color=TEAL, bold=True)
f.text(225, 136, "%s requests refused" % format(refused, ","), size=10.5, color=TEAL)
f.text(150, 170, "overdrawn in total: Rs %s" % format(lost, ","), size=10.5, color=RED, bold=True)
f.text(150, 192, "the class guards its own rule", size=10.5, color=NAVY, bold=True)
f.text(150, 210, "(same logic modelled in Python)", size=10.5, color=SLATE)
```

## Formula and fact sheet

- `class A extends B implements I { use T; }`; `new A()`; `$this->prop`; `A::STATIC`; `parent::`/`self::`/`static::`.
- Visibility `public`/`protected`/`private`; `readonly`; `final`.
- `abstract`, `interface`, `trait`; `__construct`, `__destruct`, `__toString`.
- `try { } catch (A | B $e) { } finally { }`.

## Chapter summary

- PHP objects bundle state and behaviour, with constructor promotion and visibility modifiers for encapsulation.
- Inheritance, abstract classes and interfaces give polymorphism and contracts; traits reuse code.
- Static members and the singleton pattern share state; exceptions make errors explicit.

## Practice

1. Write a class `Rectangle` with a constructor, `area()` and `perimeter()`.
2. Explain public, protected and private with an example.
3. Demonstrate method overriding and `parent::` with classes `Vehicle` and `Car`.
4. Differentiate an abstract class and an interface.
5. What is a trait and why does PHP need it?
6. Write a static method counting how many objects of a class were created.
7. Create a custom exception and catch it.

::: note Answers and worked solutions
**1.**

```php
<?php
class Rectangle {
    public function __construct(private float $w, private float $h) {}
    public function area(): float { return $this->w * $this->h; }
    public function perimeter(): float { return 2 * ($this->w + $this->h); }
}
$r = new Rectangle(3, 5);
echo $r->area(), " ", $r->perimeter(), "\n";
```
```output
15 16
```
**2.** `public`: anywhere; `protected`: the class and subclasses; `private`: only the declaring class (Section 5.2 shows `private $balance` rejected from outside).
**3.**

```php
<?php
class Vehicle { public function describe(): string { return "a vehicle"; } }
class Car extends Vehicle {
    public function describe(): string { return "a car, which is " . parent::describe(); }
}
echo (new Car)->describe(), "\n";
```
```output
a car, which is a vehicle
```
**4.** An abstract class can have properties, constructor and implemented methods plus abstract ones, and a class extends only one. An interface has only method signatures (and constants), and a class can implement several.
**5.** A trait is a group of methods/properties that can be inserted into several unrelated classes with `use`. Because PHP allows only one parent class, traits share code horizontally.
**6.**

```php
<?php
class Widget {
    private static int $made = 0;
    public function __construct() { self::$made++; }
    public static function made(): int { return self::$made; }
}
new Widget; new Widget; new Widget;
echo Widget::made(), "\n";
```
```output
3
```
**7.** See `InsufficientFunds` in Section 5.6: extend `RuntimeException`, throw it, and catch it by class.
:::

## Model answers (5 and 10 marks)

**Q1. Explain classes, objects, constructors and the visibility modifiers of PHP with a program. (10 marks)**

**Introduction.** Object-oriented programming (OOP) models a program as a set of objects, each having data (**properties**) and actions (**methods**). A **class** is the design, like a cookie cutter, and an **object** is one thing made from it with `new` (Plate 5.1). PHP has supported a full object model since PHP 5, and PHP 8 added constructor promotion and stronger types.

**Main parts of a class.**

1. **Properties** are the variables of an object, such as `$name` and `$marks`. They may have a type: `private array $marks`.
2. **Methods** are the functions of the class. Inside a method, `$this` means the current object.
3. **Constructor** `__construct()` runs automatically when an object is made and sets the first state. PHP 8 lets the parameters become properties directly (*constructor promotion*).
4. **Destructor** `__destruct()` runs when the object is removed, for example by `unset()` or at the end of the script; it is used to close files.
5. **Static members** (`static`) belong to the class, not to an object, and are reached with `self::` or `ClassName::`; one counter is shared by all objects.
6. **Constants** are declared with `const` and read with `ClassName::NAME`.

**Visibility.**

| Modifier | Class itself | Subclass | Outside code |
|---|---|---|---|
| `public` | yes | yes | yes |
| `protected` | yes | yes | no |
| `private` | yes | no | no |

Real messages from PHP (Fig. 5.1): outside code gets `Cannot access protected property A::$pro` and `Cannot access private property A::$pri`. Hiding data behind methods is **encapsulation**; it lets the class check every change.

```php
<?php
class Student {
    public static int $count = 0;
    public function __construct(private string $name, private array $marks = []) {
        self::$count++;
    }
    public function addMark(int $m): static {
        if ($m < 0 || $m > 100) throw new InvalidArgumentException("mark $m is out of range");
        $this->marks[] = $m;
        return $this;
    }
    public function average(): float {
        return $this->marks ? array_sum($this->marks) / count($this->marks) : 0.0;
    }
    public function __toString(): string { return sprintf("%s (avg %.1f)", $this->name, $this->average()); }
}
$s = new Student("Sita");
$s->addMark(88)->addMark(92)->addMark(75);
$t = new Student("Ram", [70, 64]);
echo $s, " | ", $t, " | objects made: ", Student::$count, "\n";
try { $s->addMark(150); } catch (InvalidArgumentException $e) { echo "refused: ", $e->getMessage(), "\n"; }
try { echo $s->marks; } catch (Error $e) { echo "Error: ", $e->getMessage(), "\n"; }
```
```output
Sita (avg 85.0) | Ram (avg 67.0) | objects made: 2
refused: mark 150 is out of range
Error: Cannot access private property Student::$marks
```

**Reading the run.** Two objects were made, so the shared static counter shows 2. The mark 150 was refused by the method before it could enter the object, and direct access to the private property `marks` produced an `Error`. This is what makes a class a safe unit: its rules are enforced in one place, whoever uses it, and a result system for a college can trust that every stored mark is between 0 and 100.

**Conclusion.** A class bundles data and behaviour; the constructor builds a valid object; visibility keeps the data safe; static members hold what belongs to the whole class. Together they make larger programs organised, testable and easier to change.

**Q2. What is inheritance? Explain method overriding and polymorphism with an example. (5 marks)**

**Inheritance** lets a new class (the *child*) take the properties and methods of an existing class (the *parent*) with the keyword `extends`. PHP supports single inheritance only: a class has one parent.

1. **Reuse.** The child gets all `public` and `protected` members of the parent and adds its own (Fig. 5.2).
2. **Overriding.** The child may define a method with the same name to replace the parent's version; `parent::method()` still calls the old one.
3. **Polymorphism** ("many forms"): code that calls `$shape->area()` works with any child, and each object runs its own version.
4. **`final`** on a class or method forbids extending or overriding it.
5. **`instanceof`** tests whether an object belongs to a class or interface.

```php
<?php
abstract class Shape {
    abstract public function area(): float;
    public function describe(): string { return sprintf("%s area %.2f", static::class, $this->area()); }
}
class Circle extends Shape {
    public function __construct(private float $r) {}
    public function area(): float { return M_PI * $this->r ** 2; }
}
class Rect extends Shape {
    public function __construct(private float $w, private float $h) {}
    public function area(): float { return $this->w * $this->h; }
}
$total = 0;
foreach ([new Circle(7), new Rect(4, 5), new Rect(3, 3)] as $s) { echo $s->describe(), "\n"; $total += $s->area(); }
printf("total %.2f\n", $total);
try { new Shape; } catch (Error $e) { echo $e->getMessage(), "\n"; }
```
```output
Circle area 153.94
Rect area 20.00
Rect area 9.00
total 182.94
Cannot instantiate abstract class Shape
```

The child classes keep only what is different (the formula), while the parent keeps what is common (the description). Overriding means a child supplies its own version of a parent's method. One loop handles three objects of different classes, which is why a new shape can be added without changing the loop. The abstract parent cannot be instantiated, as the last line shows.

**Q3. Differentiate between abstract class, interface and trait in PHP. When is each used? Give an example. (10 marks)**

**Introduction.** PHP allows only one parent class, so it offers three tools for sharing design: the abstract class, the interface and the trait. They answer different questions: *what is the common base*, *what must a class be able to do*, and *how do unrelated classes share code*.

**1. Abstract class.** Declared with `abstract class`. It may contain abstract methods (no body) that children must write, finished methods and properties. It cannot be instantiated. A class can extend only one. Use it when the children are variations of one idea, such as `Shape`.

**2. Interface.** Declared with `interface`. It contains only method signatures and constants. A class that `implements` it must define every method. A class may implement many interfaces. Use it for a contract that unrelated classes can satisfy, for example `Payable`, `Countable`.

**3. Trait.** Declared with `trait`. It holds finished methods and properties that are copied into any class with `use`. It removes the limit of single inheritance for code reuse, but a trait is not a type, so `instanceof` does not work for it.

| Point | Abstract class | Interface | Trait |
|---|---|---|---|
| Code inside | partly | none | yes |
| Properties | yes | constants only | yes |
| Per class | one (`extends`) | many (`implements`) | many (`use`) |
| Object can be made | no | no | no |
| Purpose | common base | contract | code reuse |

```php
<?php
interface Payable { public function pay(float $a): string; }
trait Logs {
    private array $log = [];
    public function note(string $m): void { $this->log[] = $m; }
    public function count(): int { return count($this->log); }
}
class Wallet implements Payable {
    use Logs;
    public function pay(float $a): string { $this->note("paid $a"); return "paid $a"; }
}
$w = new Wallet;
echo $w->pay(50), " | ", $w->pay(25.5), " | log size ", $w->count(), "\n";
var_dump($w instanceof Payable);
```
```output
paid 50 | paid 25.5 | log size 2
bool(true)
```

**Reading the example (Fig. 5.3).** `Wallet` promises to be `Payable`, and gets its logging code from the trait. Any code that needs a `Payable` accepts the wallet, a bank card class or a cash class alike.

In a real project the choice is often made by a simple test. If the classes are kinds of the same thing, extend a base class. If different kinds of things must be used in the same way, give them one interface. If only a few lines of code are repeated, put them in a trait.

**Conclusion.** Choose an abstract class for a shared base with partly finished code, an interface for a pure promise of behaviour, and a trait to reuse code in unrelated classes. Modern PHP code often uses all three together.

**Q4. Explain exception handling in PHP with `try`, `catch`, `finally` and a custom exception. (5 marks)**

An **exception** is an object that signals an error and interrupts the normal flow; it is *thrown* with `throw` and *caught* by a matching `catch`. It keeps error handling separate from the normal code (Fig. 5.4).

1. **try** holds the code that may fail.
2. **catch** (`Type $e`) handles one kind of exception; several `catch` blocks, or `A | B`, are allowed, and the most specific type must come first.
3. **finally** runs in every case, with or without an error, and is used for cleanup.
4. **Custom exceptions** extend `Exception`, as in `class InsufficientFunds extends Exception {}`; they are also `Throwable`.
5. **Methods:** `getMessage()`, `getCode()`, `getLine()` and `getTraceAsString()`.

```php
<?php
class InsufficientFunds extends Exception {}
function draw(int $balance, int $amount): string {
    try {
        if ($amount > $balance) throw new InsufficientFunds("need $amount, have $balance");
        echo "ok | ";
        return "done";
    } catch (InsufficientFunds $e) {
        echo "caught: ", $e->getMessage(), " | ";
        return "failed";
    } finally {
        echo "finally runs | ";
    }
}
echo draw(100, 40), "\n", draw(100, 400), "\n";
var_dump(new InsufficientFunds instanceof Throwable);
```
```output
ok | finally runs | done
caught: need 400, have 100 | finally runs | failed
bool(true)
```

The `finally` line printed in both runs, even though the function had already decided to return. A custom exception also makes the code easier to read, because `catch (InsufficientFunds $e)` says exactly what went wrong, while a bare `catch (Exception $e)` would hide the difference between a low balance and a broken database. Errors a script cannot repair should be caught once, near the top, logged, and shown to the visitor as a short polite message.
