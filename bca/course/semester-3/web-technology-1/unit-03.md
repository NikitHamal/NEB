---
subject: Web Technology I
grade: BCA Semester 3
unit: 3
title: Scripting Language (JavaScript)
area: BCA 203 · Web Technology I · Unit 3
---

**JavaScript** is the programming language of the browser: it reads and changes the page (the DOM), reacts to events and talks to servers. It also runs outside browsers (Node.js). The `js` examples in this unit were run with Node.js and their output is real; examples that touch the page are given as HTML.

::: key What this unit gives you
- Embedding scripts; variables, types, operators, control flow.
- Functions, arrays, objects, strings, Math, Date, JSON.
- The DOM, events and form validation (with regular expressions).
- Timers and error handling.
:::

## 3.1 Embedding JavaScript

```html
<script>alert("inline script");</script>       <!-- in the page -->
<script src="app.js" defer></script>           <!-- external file (preferred); defer runs it after parsing -->
<button onclick="alert('Hi')">Click</button>   <!-- inline handler: avoid in real projects -->
```

External files are cached and keep HTML clean. Output techniques: `console.log()` (developer console), `alert()`, `document.write()` (avoid), and changing the DOM (`element.textContent`). JavaScript is **case-sensitive**, **dynamically typed**, and `;` ends statements (optional but recommended).

## 3.2 Variables, data types, operators

`let` (block-scoped, reassignable), `const` (block-scoped, cannot be re-assigned), `var` (function-scoped, old; avoid). **Types:** `number`, `string`, `boolean`, `undefined`, `null`, `bigint`, `symbol` and `object` (arrays and functions are objects). `typeof x` reports the type. Operators: arithmetic `+ - * / % **`, comparison `< > <= >=`, **`===` (strict, no type conversion) versus `==` (loose)**, logical `&& || !`, assignment `+= -=`, ternary `c ? a : b`.

```js
let a = 7, b = 2;
console.log(a + b, a - b, a * b, a / b, a % b, a ** b);
console.log("5" + 3, "5" - 3, "5" * "2");
console.log(0 == "0", 0 === "0", null == undefined, null === undefined);
console.log(typeof 42, typeof "hi", typeof true, typeof undefined, typeof null, typeof [], typeof (() => 1));
console.log(0.1 + 0.2, (0.1 + 0.2).toFixed(2), Number("12px"), parseInt("12px"), parseFloat("3.14abc"));
const age = 20;
console.log(age >= 18 ? "adult" : "minor");
```
```output
9 5 14 3.5 1 49
53 2 10
true false true false
number string boolean undefined object object function
0.30000000000000004 0.30 NaN 12 3.14
adult
```

Notice `"5" + 3` is string concatenation (`"53"`) while `"5" - 3` converts to number; `0.1 + 0.2` is not exactly 0.3 (binary floating point); `typeof null` is `"object"`, a historical quirk. Falsy values: `false, 0, "", null, undefined, NaN`.

## 3.3 Control flow

```js
for (let i = 1; i <= 5; i++) {
  if (i % 2 === 0) continue;
  console.log("odd", i);
}
let n = 0;
while (n < 3) n++;
do { n--; } while (n > 0);
const day = 3;
switch (day) {
  case 1: console.log("Sun"); break;
  case 3: console.log("Tue"); break;
  default: console.log("other");
}
for (const ch of "web") console.log(ch);
for (const key in { x: 1, y: 2 }) console.log(key);
```
```output
odd 1
odd 3
odd 5
Tue
w
e
b
x
y
```

`for…of` iterates values of arrays and strings; `for…in` iterates the keys of an object. `break` leaves a loop, `continue` skips to the next iteration.

## 3.4 Functions

```js
function area(w, h = 1) { return w * h; }              // declaration, default parameter
const square = x => x * x;                             // arrow function
const counter = (() => { let c = 0; return () => ++c; })();   // closure keeps c alive
console.log(area(3, 4), area(5), square(9));
console.log(counter(), counter(), counter());
function sum(...nums) { return nums.reduce((s, x) => s + x, 0); }
console.log(sum(1, 2, 3, 4));
console.log([3, 1, 2].map(square), [1, 2, 3, 4].filter(x => x % 2 === 0));
```
```output
12 5 81
1 2 3
10
[ 9, 1, 4 ] [ 2, 4 ]
```

Functions are **first-class**: they can be stored in variables, passed to other functions (callbacks) and returned. A **closure** is a function that remembers the variables of the scope where it was created. Hoisting: function declarations are available before their line; `let`/`const` are not.

## 3.5 Arrays, objects, strings, Math, Date, JSON

```js
const marks = [85, 72, 91];
marks.push(64); marks.unshift(50);
console.log(marks, marks.length, marks.indexOf(91), marks.includes(72));
console.log(marks.slice(1, 3), marks.sort((a, b) => b - a), marks.join(" | "));
const student = { name: "Sita", age: 20, address: { city: "Kathmandu" }, greet() { return "Hi " + this.name; } };
student.email = "sita@example.np";
console.log(student.name, student["age"], student.address.city, student.greet(), Object.keys(student));
const s = "  Web Technology  ";
console.log(s.trim().toUpperCase(), s.length, s.trim().split(" "), s.includes("Tech"), s.trim().slice(0, 3), s.replace("Web", "Internet"));
console.log(Math.max(4, 9, 2), Math.round(2.5), Math.floor(-1.5), Math.sqrt(144), Math.PI.toFixed(4));
const d = new Date(2082, 0, 15);
console.log(d.getFullYear(), d.getMonth(), d.getDate(), d.getDay());
const json = JSON.stringify({ id: 1, tags: ["a", "b"], ok: true });
console.log(json, JSON.parse(json).tags[1]);
```
```output
[ 50, 85, 72, 91, 64 ] 5 3 true
[ 85, 72 ] [ 91, 85, 72, 64, 50 ] 91 | 85 | 72 | 64 | 50
Sita 20 Kathmandu Hi Sita [ 'name', 'age', 'address', 'greet', 'email' ]
WEB TECHNOLOGY 18 [ 'Web', 'Technology' ] true Web   Internet Technology  
9 3 -2 12 3.1416
2082 0 15 4
{"id":1,"tags":["a","b"],"ok":true} b
```

**JSON** (JavaScript Object Notation) is the standard text format for data exchange: keys in double quotes; values are strings, numbers, booleans, null, arrays, objects. `JSON.stringify` makes text from an object and `JSON.parse` does the reverse. Arrays have `map`, `filter`, `reduce`, `forEach`, `find`, `some`, `every`, `splice`, `concat`.

## 3.6 Regular expressions

A regular expression describes a text pattern: `/^[A-Za-z]+$/` (letters only), `\d` digit, `\w` word character, `.` any, `+` one or more, `*` zero or more, `{n,m}` counts, `^` and `$` anchor start and end.

```js
const email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const phone = /^9[78]\d{8}$/;                      // Nepali mobile: 97xxxxxxxx or 98xxxxxxxx
const strong = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
for (const t of ["sita@example.np", "bad@", "x y@z.com"]) console.log(t, email.test(t));
for (const t of ["9841234567", "9611111111", "984123"]) console.log(t, phone.test(t));
console.log(strong.test("Passw0rdOK"), strong.test("password"));
console.log("a1b22c333".match(/\d+/g), "2082-04-12".replace(/(\d+)-(\d+)-(\d+)/, "$3/$2/$1"));
```
```output
sita@example.np true
bad@ false
x y@z.com false
9841234567 true
9611111111 false
984123 false
true false
[ '1', '22', '333' ] 12/04/2082
```

## 3.7 The DOM and events

The **Document Object Model** is the browser's tree of the page that JavaScript can read and modify.

| Task | Code |
|---|---|
| Find an element | `document.getElementById("id")`, `document.querySelector(".cls")`, `querySelectorAll("li")` |
| Read/change text | `el.textContent = "Hi"`; `el.innerHTML` (careful: can inject scripts) |
| Change attributes/style | `el.setAttribute("href", "…")`, `el.style.color = "red"`, `el.classList.add("on")` |
| Create/insert/remove | `document.createElement("li")`, `parent.appendChild(li)`, `el.remove()` |
| Listen to events | `el.addEventListener("click", handler)` |

Common events: `click`, `dblclick`, `mouseover`, `keydown`, `input`, `change`, `submit`, `focus`, `blur`, `load`, `DOMContentLoaded`. The handler receives an **event object** (`e.target`, `e.preventDefault()`). Events **bubble** from the target up through its ancestors, so one listener on a parent can handle all children (**event delegation**).

```html
<ul id="todo"></ul>
<input id="item" placeholder="New task"> <button id="add">Add</button>
<script>
  const list = document.getElementById("todo");
  document.getElementById("add").addEventListener("click", () => {
    const box = document.getElementById("item");
    if (box.value.trim() === "") return;
    const li = document.createElement("li");
    li.textContent = box.value.trim();
    list.appendChild(li);
    box.value = "";
  });
  list.addEventListener("click", e => { if (e.target.tagName === "LI") e.target.remove(); });  // delegation
</script>
```

### Form validation

```html
<form id="reg" novalidate>
  <input id="email" name="email" placeholder="Email"> <span id="emsg" style="color:red"></span>
  <input id="pass" type="password" placeholder="Password (8+, upper, lower, digit)">
  <button>Register</button>
</form>
<script>
  document.getElementById("reg").addEventListener("submit", e => {
    const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(document.getElementById("email").value);
    document.getElementById("emsg").textContent = ok ? "" : "Enter a valid email";
    if (!ok) e.preventDefault();            // stop submission
  });
</script>
```

## 3.8 Timers, errors and asynchronous code

```js
function risky(x) { if (x < 0) throw new Error("negative not allowed"); return Math.sqrt(x); }
try { console.log(risky(16)); console.log(risky(-4)); }
catch (err) { console.log("caught:", err.message); }
finally { console.log("done"); }
setTimeout(() => console.log("after 10 ms"), 10);
console.log("this prints first");
const wait = ms => new Promise(res => setTimeout(() => res("waited " + ms), ms));
(async () => { console.log(await wait(20)); })();
```
```output
4
caught: negative not allowed
done
this prints first
after 10 ms
waited 20
```

`setTimeout(fn, ms)` runs once, `setInterval(fn, ms)` repeatedly (stop with `clearInterval`). JavaScript is **single-threaded**; slow work (network) is handed off and its callback or **Promise** continues later, which is why "this prints first" appears before "after 10 ms". `async`/`await` write promise code in a straight line. **AJAX** with `fetch("/api").then(r => r.json())` loads data without reloading the page (Unit 6).

## Formula and fact sheet

- `let`/`const` block scope; `===` strict equality; falsy: false, 0, "", null, undefined, NaN.
- Functions are first-class; closures remember scope; arrow `x => x * x`.
- JSON: `stringify`/`parse`. Array methods: map, filter, reduce, forEach.
- DOM: `querySelector`, `textContent`, `addEventListener`, `createElement`, events bubble.
- Validate with regular expressions in the browser *and* on the server.

## Chapter summary

- JavaScript adds behaviour: variables and types, control flow, functions and closures, arrays, objects and JSON.
- The DOM and events let scripts read and change the page; forms are validated before submission.
- Errors use try/catch/finally; timers and promises handle work that finishes later.

## Practice

1. Differentiate `let`, `const` and `var`; `==` and `===`.
2. Write a function that returns the largest of an array without `Math.max`.
3. Predict the output: `console.log("3" + 4, "3" * "4", [] + [], typeof NaN)`.
4. Write a regex for a six-digit PIN and test it.
5. Write the DOM code to change a paragraph's colour to blue when a button is clicked.
6. What is a closure? Give an example.
7. Explain event bubbling and delegation.
8. Why does `setTimeout(f, 0)` run after the code that follows it?

::: note Answers and worked solutions
**1.** `let`: block-scoped, reassignable; `const`: block-scoped, binding cannot be reassigned; `var`: function-scoped, hoisted. `==` converts types (`0 == "0"` true); `===` compares type and value (false).
**2.** `function max(a){ let m = a[0]; for (const x of a) if (x > m) m = x; return m; }`
**3.** `"34" 12 "" "number"` (string concatenation, numeric multiplication, two empty arrays converting to empty strings, `typeof NaN` is `"number"`).
**4.** `/^\d{6}$/.test("123456")` is true; `"12345"` false.
**5.** `document.getElementById("btn").addEventListener("click", () => { document.getElementById("p").style.color = "blue"; });`
**6.** A function plus the variables of its defining scope: `const c = (() => { let n = 0; return () => ++n; })();` each call to `c()` increases the private `n`.
**7.** An event on an element propagates upward to its ancestors; a single listener on a parent can inspect `e.target` and handle events from many children, including ones added later.
**8.** The callback is queued and only runs when the current synchronous code has finished.
:::
