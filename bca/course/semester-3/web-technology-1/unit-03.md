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

## 3.9 Seeing JavaScript: people, scope, events and the loop

JavaScript is a small language with a few ideas that surprise beginners: scope, type coercion, event flow and the single-threaded event loop. The plate shows the two people most linked to the language and its data format; the figures draw the ideas and the code blocks next to them were run in Node.js 22 so that every printed value is real.

```photogrid label="3.1" cols="3" ratio="1.0" caption="(a) Brendan Eich, who wrote the first JavaScript prototype at Netscape in May 1995 in about ten days; it was first called Mocha and then LiveScript before the name JavaScript. (b) Douglas Crockford, who named and promoted JSON, the text format that grew out of JavaScript object literals and is now the standard way for web services to exchange data. (c) The milestones in between. ECMAScript is the official standard name of the language."
@ photo id="bca203/eich" cap="Brendan Eich"
fit 1.0
focus 0.5 0.62
@ photo id="bca203/crockford" cap="Douglas Crockford"
fit 1.0
focus 0.5 0.62
@ svg cap="JavaScript milestones"
f = Fig(300, 300)
ev = [("1995", "Created at Netscape"), ("1997", "ECMAScript 1 standard"), ("2001", "JSON described"), ("2009", "ES5 and Node.js"), ("2015", "ES2015: let, const, =>"), ("Today", "Yearly ES releases")]
for i, (y, t) in enumerate(ev):
    yy = 22 + i * 46
    f.box(8, yy, 56, 28, y, fill=BLUE, stroke=NAVY, size=12.5, bold=True)
    f.text(72, yy + 14, t, size=12.5, color=SLATE, bold=True, anchor="start")
    if i < 5: f.line(36, yy + 28, 36, yy + 46, color=SLATE)
```

```svgfig label="3.1" caption="The event loop explains why the code below prints A, D, C, B. The call stack runs the synchronous lines first (A, then D). The timer callback is placed in the macrotask queue and the promise callback in the microtask queue. When the stack is empty the loop runs all microtasks (C) before taking the next macrotask (B), even though the timer delay was 0 ms. A long loop on the stack blocks everything, including clicks and painting."
f = Fig(580, 214)
f.box(10, 20, 150, 170, "", fill=BLUE, stroke=NAVY)
f.text(85, 12, "Call stack", size=11, color=NAVY, bold=True)
f.box(24, 140, 122, 36, "log('A')  then  log('D')", fill=SOFT, stroke=NAVY, size=9.5, bold=True)
f.box(220, 20, 160, 76, "", fill=MINT, stroke=TEAL)
f.text(300, 12, "Microtask queue", size=11, color=TEAL, bold=True)
f.box(236, 44, 128, 34, "promise then: log('C')", fill=SOFT, stroke=TEAL, size=9.5, bold=True)
f.box(220, 114, 160, 76, "", fill=SAND, stroke=AMBER)
f.text(300, 108, "Macrotask queue", size=11, color=AMBER, bold=True)
f.box(236, 138, 128, 34, "setTimeout: log('B')", fill=SOFT, stroke=AMBER, size=9.5, bold=True)
f.arrow([(160, 158), (220, 158)], color=SLATE, dash=True); f.arrow([(160, 60), (220, 60)], color=SLATE, dash=True)
f.box(420, 40, 150, 132, "Output order\n\n1  A\n2  D\n3  C\n4  B", fill=ROSE, stroke=RED, size=12, bold=True)
```

```js
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
```

```output
A
D
C
B
```

```svgfig label="3.2" caption="Scope chain. Function g can see z (its own), y (from f) and x (from the global scope), so g() returns 1 + 2 + 3 = 6. Lookup walks outwards and never inwards: the global code cannot read y or z. let and const are block-scoped and sit in the temporal dead zone until their line runs, so reading them early throws ReferenceError, whereas var is function-scoped and hoisted as undefined."
f = Fig(580, 200)
f.box(10, 8, 330, 184, "", fill=BLUE, stroke=NAVY)
f.box(40, 40, 270, 140, "", fill=MINT, stroke=TEAL)
f.box(70, 72, 210, 96, "", fill=SAND, stroke=AMBER)
f.text(20, 24, "global:  let x = 1", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(50, 56, "function f:  let y = 2", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(80, 90, "function g:  let z = 3", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(80, 130, "return x + y + z", size=11, color=RED, bold=True, anchor="start")
f.text(360, 40, "Lookup of x inside g:", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(360, 62, "1. g has no x", size=10.5, color=SLATE, anchor="start")
f.text(360, 82, "2. f has no x", size=10.5, color=SLATE, anchor="start")
f.text(360, 102, "3. global has x = 1  found", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(360, 134, "f() returns 6", size=12, color=RED, bold=True, anchor="start")
f.text(360, 156, "typeof undeclaredName is 'undefined'", size=9.5, color=SLATE, anchor="start")
f.text(360, 172, "but reading a let early: ReferenceError", size=9.5, color=SLATE, anchor="start")
```

```svgfig label="3.3" caption="Surprising results of type coercion, each run in Node.js. The + operator joins strings if either side is a string, so '5' + 3 is '53', but - always converts to numbers, so '5' - 3 is 2. == converts types before comparing (0 == '' is true) while === never does. NaN is not equal to itself, typeof null is 'object' for historical reasons, and 0.1 + 0.2 is 0.30000000000000004 because binary floating point cannot store 0.1 exactly. Sorting [10, 9, 1] without a compare function sorts as text and gives 1,10,9."
f = Fig(580, 232)
rows = [("'5' + 3", "'53'"), ("'5' - 3", "2"), ("0 == ''", "true"), ("null == undefined", "true"), ("NaN === NaN", "false"), ("typeof null", "'object'"), ("0.1 + 0.2", "0.30000000000000004"), ("[10, 9, 1].sort()", "[1, 10, 9]")]
f.box(10, 8, 270, 24, "Expression", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
f.box(280, 8, 290, 24, "Result in JavaScript", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, (a, b) in enumerate(rows):
    y = 32 + i * 24
    fill = SOFT if i % 2 == 0 else "#ffffff"
    f.box(10, y, 270, 24, a, fill=fill, stroke="#cbd5e1", color=SLATE, size=10.5, bold=True, r=0)
    f.box(280, y, 290, 24, b, fill=fill, stroke="#cbd5e1", color=RED, size=10.5, bold=True, r=0)
```

```js
console.log("5" + 3, "5" - 3, 0 == "", NaN === NaN, typeof null, 0.1 + 0.2);
```

```output
53 2 true false object 0.30000000000000004
```

```svgfig label="3.4" caption="Event flow in the DOM. A click on the button travels down the tree in the capture phase (window to button), runs the handlers on the target, then bubbles up (button to window). By default addEventListener listens in the bubbling phase, so a handler on the form also sees clicks on its buttons. This is the basis of event delegation: one listener on a table can serve a thousand rows by checking event.target. event.stopPropagation() ends the journey, and event.preventDefault() stops the default action such as submitting the form."
f = Fig(580, 200)
names = ["window", "document", "form", "button"]
for i, nm in enumerate(names):
    f.box(20 + i * 20, 10 + i * 36, 220 - i * 40, 160 - i * 36, "", fill=[SOFT, BLUE, MINT, SAND][i], stroke=[SLATE, NAVY, TEAL, AMBER][i])
    f.text(28 + i * 20, 24 + i * 36, nm, size=10.5, color=[SLATE, NAVY, TEAL, AMBER][i], bold=True, anchor="start")
f.arrow([(300, 30), (300, 150)], color=NAVY); f.text(310, 90, "1 capture: down", size=10.5, color=NAVY, bold=True, anchor="start")
f.arrow([(560, 150), (560, 30)], color=TEAL); f.text(550, 90, "3 bubble: up", size=10.5, color=TEAL, bold=True, anchor="end")
f.text(370, 170, "2 target handler runs on the button", size=10.5, color=AMBER, bold=True)
f.text(370, 190, "button.addEventListener('click', fn)", size=9.5, color=SLATE)
```

```svgfig label="3.5" caption="An array pipeline. [1,2,3,4,5,6] goes through filter(n => n % 2 === 0) to keep 2, 4, 6; map(n => n * n) turns them into 4, 16, 36; reduce((a, b) => a + b, 0) adds them: 0 + 4 = 4, 4 + 16 = 20, 20 + 36 = 56. None of the three methods changes the original array, which makes the pipeline easy to test."
f = Fig(580, 130)
def row(x, items, fill, stroke):
    for i, v in enumerate(items):
        f.box(x + i * 34, 52, 30, 30, str(v), fill=fill, stroke=stroke, size=11, bold=True)
row(8, [1, 2, 3, 4, 5, 6], BLUE, NAVY)
f.arrow([(216, 67), (252, 67)], color=SLATE); f.text(234, 46, "filter", size=10, color=RED, bold=True)
row(258, [2, 4, 6], MINT, TEAL)
f.arrow([(366, 67), (402, 67)], color=SLATE); f.text(384, 46, "map", size=10, color=RED, bold=True)
row(408, [4, 16, 36], SAND, AMBER)
f.arrow([(520, 67), (548, 67)], color=SLATE)
f.text(560, 36, "reduce", size=10, color=RED, bold=True)
f.box(540, 80, 36, 30, "56", fill=ROSE, stroke=RED, size=12, bold=True)
f.text(110, 108, "even test", size=9.5, color=SLATE); f.text(310, 108, "square", size=9.5, color=SLATE)
```

```js
const total = [1, 2, 3, 4, 5, 6].filter(n => n % 2 === 0).map(n => n * n).reduce((a, b) => a + b, 0);
console.log(total);
```

```output
56
```

```svgfig label="3.6" caption="The regular expression for a Nepali mobile number, taken apart. The start anchor ^ pins the match to the beginning, 9 is a literal, [78] is one of two digits (numbers begin 98 or 97), \d{8} is exactly eight digits and the end anchor (a dollar sign) pins the match to the end. Without the anchors a longer string would pass. Test results from Node.js: 9841234567 true, 9712345678 true, 9612345678 false (third digit rule), 984123456 false (nine digits), 98412345678 false (eleven digits)."
f = Fig(580, 150)
tok = [("^", "start", 34, NAVY), ("9", "literal 9", 50, TEAL), ("[78]", "7 or 8", 60, AMBER), ("\\d{8}", "8 digits", 84, RED), ("END", "end anchor", 52, NAVY)]
x = 14
for t, d, w, c in tok:
    f.box(x, 24, w, 36, t, fill=SOFT, stroke=c, color=c, size=13, bold=True, sw=2)
    f.text(x + w / 2, 80, d, size=10, color=c, bold=True)
    x += w + 12
f.box(410, 14, 160, 124, "", fill=SOFT, stroke=SLATE)
for i, (s, ok) in enumerate([("9841234567", True), ("9712345678", True), ("9612345678", False), ("984123456", False), ("98412345678", False)]):
    f.text(420, 36 + i * 22, s, size=10.5, color=SLATE, bold=True, anchor="start")
    f.text(560, 36 + i * 22, "true" if ok else "false", size=10.5, color=TEAL if ok else RED, bold=True, anchor="end")
f.text(190, 130, "Digits only, 10 in total, prefix 97 or 98", size=10.5, color=NAVY, bold=True)
```

### 3.9.1 Eight uses of JavaScript in a web page

1. **Form validation.** JavaScript checks a field before the form is sent and shows a message at once. For example, a scholarship form can test a Nepali mobile number with the pattern in Figure 3.6 and warn the student immediately. This saves a trip to the server, although the server must repeat the check for safety.
2. **Changing the page without reloading.** Scripts change text, add rows and show or hide sections using the DOM. A live notice board can add a new notice at the top as soon as it is published. The user sees the update without losing the place on the page.
3. **Reacting to the user.** Clicks, key presses, scrolling and touches are events that call functions. A menu opens when the hamburger icon is tapped, and a search box can suggest names as the user types. Good event handling makes a page feel fast and alive.
4. **Talking to servers (AJAX and fetch).** The fetch function requests JSON in the background and updates part of the page. The NEPSE market widget on a news site loads fresh prices every few seconds this way. Only a few bytes travel, which matters for users on limited mobile data.
5. **Interactive widgets.** Image sliders, tabs, calendars, date pickers and accordions are built with scripts. A Nepali date converter between Bikram Sambat and the English calendar is a typical example. These widgets turn static pages into small applications.
6. **Storing data in the browser.** localStorage and sessionStorage keep small values such as a theme choice or a half-written form. A quiz page can save the answers so that a refresh does not lose them. Sensitive data such as passwords should never be stored there.
7. **Drawing, animation and media.** With canvas, SVG and the animation functions, scripts draw charts, games and maps. A results page can show a bar chart of pass percentage by faculty. Media players use JavaScript for play, pause and volume controls.
8. **Running on the server and in apps.** With Node.js the same language builds servers, tools and APIs, and frameworks build mobile and desktop apps. A small college can therefore use one language from the browser to the database. This is one reason JavaScript is among the most widely used languages.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Differentiate var, let and const. Explain scope and hoisting with an example.**

*Introduction.* ES2015 added let and const to fix problems of var; the three differ in scope, hoisting and re-assignment (section 3.2, Figure 3.2).

1. **var** is function-scoped, hoisted to the top of its function and initialised to undefined, can be re-declared and re-assigned. It ignores block braces, so a var declared in an if block is visible after it.
2. **let** is block-scoped, can be re-assigned but not re-declared in the same scope. It is hoisted but stays in the temporal dead zone until its line runs, so early use throws ReferenceError.
3. **const** is block-scoped like let, must be given a value when declared and cannot be re-assigned. The object it holds can still change: const list = []; list.push(1) is allowed.
4. **Scope chain.** Inner functions see variables of outer functions; the engine looks outwards, never inwards. In Figure 3.2, g sees z, y and x and f() returns 6.
5. **Good practice.** Use const by default, let when the value must change, and avoid var.

```js
console.log(typeof undeclared, (function () { try { return tdz; let tdz = 1; } catch (e) { return e.name; } })());
```

```output
undefined ReferenceError
```

| Feature | var | let | const |
|---|---|---|---|
| Scope | Function | Block | Block |
| Re-declare | Yes | No | No |
| Re-assign | Yes | Yes | No |
| Before its line | undefined | ReferenceError | ReferenceError |

*Conclusion.* Block scope with let and const makes code more predictable than var, so modern code prefers them.

**Q2 (5 marks). Explain event handling and event bubbling in JavaScript with an example. How does event delegation use it?**

*Introduction.* An event is a signal that something happened, such as a click; a handler is a function that runs in response (section 3.7, Figure 3.4).

1. **Registering.** Use element.addEventListener("click", handler). It allows many handlers for one event, unlike the old onclick property, which holds only one.
2. **The event object.** The handler receives an object with type, target (where it happened), currentTarget and methods preventDefault and stopPropagation.
3. **Flow.** The event first travels down the tree (capture), reaches the target, and then bubbles up through every ancestor. Most events bubble; focus does not.
4. **Delegation.** Instead of attaching a listener to every row of a table, attach one to the table and read event.target. It uses less memory and also works for rows added later.
5. **Control.** preventDefault stops the browser action (form submit, link follow); stopPropagation stops the bubbling.

```html
<ul id="menu"><li data-id="1">Notices</li><li data-id="2">Results</li></ul>
<script>
document.getElementById("menu").addEventListener("click", function (e) {
  if (e.target.tagName === "LI") alert("Open item " + e.target.dataset.id);
});
</script>
```

*Conclusion.* Because events bubble, one listener on a parent can handle all its children, which is the foundation of efficient delegation.

**Q3 (10 marks). Write a JavaScript program to validate a registration form (name not empty, valid Nepali mobile number, password of at least 8 characters) and explain the DOM, event and regular-expression concepts used.**

*Introduction.* Client-side validation gives instant feedback and reduces server traffic. It uses three ideas of this unit: the DOM to read and change the page, events to run code at the right time, and regular expressions to test patterns. The server must still validate again because JavaScript can be switched off or altered (sections 3.6 and 3.7, Figures 3.4 and 3.6).

1. **Selecting elements.** document.getElementById or querySelector returns the node of the input, the error paragraph or the form.
2. **Reading values.** input.value is a string; trim() removes spaces at the ends so that a name of only spaces is rejected.
3. **Listening for submit.** form.addEventListener("submit", fn) runs fn when the form is sent. Inside it, event.preventDefault() stops submission if any rule fails.
4. **Regular expression.** `/^9[78]\d{8}$/` accepts exactly ten digits beginning 97 or 98; test() returns true or false (Figure 3.6).
5. **Showing errors.** Collect messages in an array and write them with textContent into the error element; textContent is safer than innerHTML because it does not run markup.
6. **Accessibility.** Set aria-live="polite" on the error area so screen readers announce the message.
7. **Clearing.** Reset the message at the start of each attempt so old errors do not remain.
8. **Server check.** After the client check passes the form is sent, and the server validates again.

```html
<form id="reg"><input id="nm"><input id="ph"><input id="pw" type="password">
<button>Register</button><p id="err" aria-live="polite"></p></form>
<script>
const form = document.getElementById("reg");
form.addEventListener("submit", function (e) {
  const errors = [];
  if (document.getElementById("nm").value.trim() === "") errors.push("Name is required.");
  if (!/^9[78]\d{8}$/.test(document.getElementById("ph").value)) errors.push("Enter a 10-digit mobile number starting 97 or 98.");
  if (document.getElementById("pw").value.length < 8) errors.push("Password needs at least 8 characters.");
  document.getElementById("err").textContent = errors.join(" ");
  if (errors.length > 0) e.preventDefault();
});
</script>
```

| Concept | Where used | Purpose |
|---|---|---|
| DOM | getElementById, textContent | Read and change the page |
| Event | submit listener | Run code when the form is sent |
| Regex | test() | Check the phone pattern |
| preventDefault | inside the handler | Block an invalid submission |

*Conclusion.* The program reads values from the DOM, tests them when the submit event fires, shows all errors together and blocks submission if any exist. It improves the user experience but is never a replacement for server-side validation.
