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
