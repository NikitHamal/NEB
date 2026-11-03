---
subject: Web Technology I
grade: BCA Semester 3
unit: 6
title: Introduction to jQuery
area: BCA 203 · Web Technology I · Unit 6
---

**jQuery** is a small JavaScript library that makes selecting elements, changing the page, handling events and calling the server shorter and consistent across browsers. Its motto: *write less, do more*. Modern JavaScript has absorbed many of its features, but jQuery is still on millions of sites and is part of this syllabus.

::: key What this unit gives you
- Including jQuery and the `$` function, `ready`.
- Selecting and filtering elements; getting and setting content, attributes, CSS and classes.
- Adding and removing elements, events, effects, chaining, AJAX.
- Every example below was run in a simulated browser (jsdom) with jQuery 3; the output is real.
:::

## 6.1 Setting up

```html
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script>
  $(document).ready(function () {     // or the short form: $(function () { ... });
    $("#hello").text("jQuery is ready");
  });
</script>
```

Load jQuery from a CDN or your own copy before your script. **`$`** is an alias of **`jQuery`**: `$(selector)` returns a jQuery object wrapping all matching elements; **`$(function(){…})`** runs the code when the DOM is ready. The basic pattern is **select → act**: `$(selector).action()`.

## 6.2 Selectors and filtering

jQuery uses CSS selectors (Unit 4) plus extras.

```jquery
<ul id="list">
  <li class="item">One</li>
  <li class="item done">Two</li>
  <li class="item">Three</li>
  <li class="other">Four</li>
</ul>
//---
console.log($("li").length);                       // by tag
console.log($(".item").length, $("#list").length); // by class, by id
console.log($("li.done").text());                  // combined
console.log($("#list > li").first().text(), $("li").last().text());
console.log($("li").eq(2).text());                 // index 2
console.log($("li").not(".item").text());          // exclusion
console.log($("li:even").length);                  // even positions (0, 2)
console.log($(".done").prev().text(), $(".done").next().text());
console.log($("li").filter(function () { return $(this).text().length > 3; }).length);
```
```output
4
3 1
Two
One Four
Three
Four
2
One Three
2
```

`$("li").length` counts matches (0 if none: always safe). Other helpers: `.parent()`, `.children()`, `.siblings()`, `.find("p")` (descendants), `.closest(".box")`.

## 6.3 Getting and setting content, attributes, CSS, classes

| Method | Use |
|---|---|
| `.text()`, `.html()`, `.val()` | get/set text, HTML, form value |
| `.attr("href")`, `.prop("checked")`, `.data("id")` | attribute, property, `data-*` |
| `.css("color", "red")` | inline style (getter with one argument) |
| `.addClass()`, `.removeClass()`, `.toggleClass()`, `.hasClass()` | class manipulation (preferred to `.css`) |

```jquery
<h1 id="title">Old title</h1>
<a id="link" href="http://old.example" data-id="42">link</a>
<input id="name" value="Sita">
<p class="msg">message</p>
//---
$("#title").text("New title");
console.log($("#title").text());
console.log($("#link").attr("href"), $("#link").data("id"));
$("#link").attr("href", "https://new.example");
console.log($("#link").attr("href"));
console.log($("#name").val());
$("#name").val("Ram");
console.log($("#name").val());
$(".msg").addClass("big important").css({ color: "red", "font-size": "20px" });
console.log($(".msg").hasClass("big"), $(".msg").attr("class"), $(".msg").css("color"));
$(".msg").toggleClass("big");
console.log($(".msg").attr("class"));
$("#title").html("<em>Styled</em> title");
console.log($("body").html().replace(/\s+/g, " ").slice(0, 60));
```
```output
New title
http://old.example 42
https://new.example
Sita
Ram
true msg big important rgb(255, 0, 0)
msg important
<h1 id="title"><em>Styled</em> title</h1> <a id="link" href=
```

## 6.4 Adding, removing and cloning elements

`.append()` / `.prepend()` add inside at the end / start; `.after()` / `.before()` add outside; `.remove()` deletes the element, `.empty()` clears its children; `.clone()` copies; `.wrap()`, `.replaceWith()`. `.each(function (i, el) { … })` loops over matches.

```jquery
<ul id="menu"><li>Home</li><li>Courses</li></ul>
//---
$("#menu").append("<li>Contact</li>").prepend("<li class='first'>Logo</li>");
console.log($("#menu li").length, $("#menu li:first").text());
$("#menu li").last().after("<li>Footer</li>");
$("#menu li:contains('Courses')").remove();
$("#menu li").each(function (i) { $(this).text((i + 1) + ". " + $(this).text()); });
console.log($("#menu").text());
const copy = $("#menu").clone();
console.log(copy.find("li").length, $("#menu").find("li").length);
$("#menu").empty();
console.log($("#menu").children().length);
```
```output
4 Logo
1. Logo2. Home3. Courses4. Contact5. Footer
5 5
0
```

## 6.5 Events

`.on(event, [selector], handler)` attaches; `.off()` removes; shortcuts include `.click()`, `.hover()`, `.submit()`, `.keyup()`, `.change()`. Inside a handler, `this` is the element and `e.preventDefault()` / `e.stopPropagation()` are available. **Delegated** form `$("#list").on("click", "li", fn)` also works for elements added later. `.trigger("click")` fires an event from code.

```jquery
<button id="inc">+1</button> <span id="count">0</span>
<ul id="todo"><li>A</li></ul>
//---
let clicks = 0;
$("#inc").on("click", function () { clicks++; $("#count").text(clicks); });
$("#inc").trigger("click").trigger("click").trigger("click");
console.log("count shows", $("#count").text());
$("#todo").on("click", "li", function () { $(this).toggleClass("done"); });
$("#todo").append("<li>B (added later)</li>");
$("#todo li").last().trigger("click");
console.log($("#todo li.done").text());
$("#inc").off("click");
$("#inc").trigger("click");
console.log("after off:", $("#count").text());
```
```output
count shows 3
B (added later)
after off: 3
```

## 6.6 Effects and chaining

Effects: `.show()`, `.hide()`, `.toggle()`, `.fadeIn()`, `.fadeOut()`, `.slideUp()`, `.slideDown()`, and `.animate({height: "200px", opacity: .5}, 500)`. Each accepts a duration (ms) and a **callback** run when it finishes. **Chaining** works because most methods return the jQuery object: `$("#box").addClass("on").fadeIn(300).text("Done");`.

```jquery
<div id="box">Hello</div>
//---
$("#box").hide();
console.log("display after hide():", $("#box").css("display"));
$("#box").show();
console.log("display after show():", $("#box").css("display"));
$("#box").addClass("on").css("color", "green").text("Done");
console.log($("#box").text(), $("#box").attr("class"), $("#box").css("color"));
```
```output
display after hide(): none
display after show(): block
Done on rgb(0, 128, 0)
```

## 6.7 AJAX with jQuery

**AJAX** (Asynchronous JavaScript And XML) requests data from the server in the background and updates part of the page without a reload. jQuery wraps it:

```text
$("#result").load("notice.html #latest");                  // fetch HTML fragment into an element

$.get("/api/students", function (data) { ... });            // GET
$.post("/api/students", { name: "Sita" }, function (res) { ... });

$.ajax({
  url: "/api/students/1", method: "GET", dataType: "json",
  success: function (s) { $("#name").text(s.name); },
  error:   function (xhr, status) { alert("Failed: " + status); }
});

// modern equivalent without jQuery:
fetch("/api/students/1").then(r => r.json()).then(s => { document.getElementById("name").textContent = s.name; });
```

These calls need a real server, so they are shown but not executed here. Browsers apply the **same-origin policy**: a page may call only its own origin unless the server allows others with CORS headers. `$.getJSON(url, cb)` is shorthand for a JSON GET.

## 6.8 jQuery versus plain JavaScript

| Task | jQuery | Modern JavaScript |
|---|---|---|
| Select | `$(".item")` | `document.querySelectorAll(".item")` |
| Text | `$("#a").text("x")` | `document.querySelector("#a").textContent = "x"` |
| Class | `.addClass("on")` | `el.classList.add("on")` |
| Event | `.on("click", f)` | `el.addEventListener("click", f)` |
| AJAX | `$.get(url, cb)` | `fetch(url).then(r => r.json())` |

jQuery's benefits are brevity and old-browser compatibility; its cost is an extra download (about 30 KB gzipped). New projects usually use plain JavaScript or frameworks, but legacy code and WordPress themes still rely on jQuery.

## 6.9 Seeing jQuery: selection, chaining, effects and traversal

jQuery wraps the DOM in a short, chainable API. The plate shows its creator and a timeline; the figures show how a selector picks elements, how a chain passes one object along, how the animation queue adds up in milliseconds, how traversal walks the tree and how an AJAX call is split into a request and a callback. In the figures the function is written jQuery(...), which is exactly the same function as the dollar shorthand used in the code.

```photogrid label="6.1" cols="2" ratio="1.2" caption="(a) John Resig, who released jQuery in January 2006 with the motto write less, do more. (b) The main milestones. jQuery 1.0 appeared in August 2006, the 3.x line in 2016; it hides differences between browsers, and the same selector and event code worked in browsers that did not agree on the standard DOM. Today standard JavaScript has copied many of its ideas (querySelectorAll, fetch, classList), but millions of existing sites still use it."
@ photo id="bca203/resig" cap="John Resig"
fit 1.2
focus 0.5 0.55
@ svg cap="jQuery milestones"
f = Fig(330, 275)
ev = [("2006", "jQuery announced"), ("2006", "Version 1.0"), ("2009", "Used by many sites"), ("2013", "Version 2: drops old IE"), ("2016", "Version 3.0, promises"), ("Now", "Maintained, legacy sites")]
for i, (y, t) in enumerate(ev):
    yy = 8 + i * 44
    f.box(6, yy, 58, 28, y, fill=BLUE, stroke=NAVY, size=12.5, bold=True)
    f.text(74, yy + 14, t, size=12.5, color=SLATE, bold=True, anchor="start")
    if i < 5: f.line(35, yy + 28, 35, yy + 44, color=SLATE)
```

```svgfig label="6.1" caption="What a selector matches. The list has five items; items 2 and 4 carry the class done. jQuery('li.done') returns those two; jQuery('ul > li:first') returns item 1; jQuery('li:not(.done)') returns 1, 3 and 5; jQuery('li:even') returns the items at index 0, 2 and 4 (that is items 1, 3 and 5, because indexes start at 0). The result is a jQuery object that behaves like an array: .length tells how many matched, and any method called on it applies to all of them."
f = Fig(580, 214)
f.box(10, 10, 170, 190, "", fill=SOFT, stroke=SLATE)
f.text(20, 26, "<ul>", size=10, color=SLATE, bold=True, anchor="start")
for i in range(5):
    done = i in (1, 3)
    f.box(26, 38 + i * 32, 140, 26, f"li {i+1}" + ("  .done" if done else ""), fill=MINT if done else BLUE, stroke=TEAL if done else NAVY, size=10.5, bold=True)
rows = [("jQuery('li.done')", "2, 4", "2"), ("jQuery('ul > li:first')", "1", "1"), ("jQuery('li:not(.done)')", "1, 3, 5", "3"), ("jQuery('li:even')", "1, 3, 5 (index 0, 2, 4)", "3")]
f.text(210, 26, "selector", size=10.5, color=NAVY, bold=True, anchor="start"); f.text(400, 26, "matches", size=10.5, color=NAVY, bold=True, anchor="start"); f.text(540, 26, ".length", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (a, b, c) in enumerate(rows):
    y = 40 + i * 40
    f.box(200, y, 372, 32, "", fill=SOFT, stroke="#cbd5e1")
    f.text(208, y + 16, a, size=10, color=SLATE, bold=True, anchor="start")
    f.text(392, y + 16, b if len(b) < 10 else "1, 3, 5", size=10, color=TEAL, bold=True, anchor="start")
    f.text(548, y + 16, c, size=10.5, color=RED, bold=True, anchor="start")
f.text(200, 206, "Indexes start at 0, so :even picks items 1, 3 and 5.", size=10, color=RED, bold=True, anchor="start")
```

```svgfig label="6.2" caption="Method chaining. Most jQuery methods return the same jQuery object, so calls can be joined in one statement: jQuery('#box').addClass('on').css('color','red').fadeOut(400). Each box below receives the object, does its job and hands it on. Reading the chain from left to right tells the story, and the element is searched only once, which is faster than selecting it three times. Methods that read a value, such as .text() or .val() with no argument, return the value instead and end the chain."
f = Fig(580, 120)
steps = [("jQuery('#box')", "select"), (".addClass('on')", "add class"), (".css('color','red')", "set style"), (".fadeOut(400)", "animate")]
x = 8
for i, (a, b) in enumerate(steps):
    w = 130 if i != 2 else 150
    f.box(x, 30, w, 38, a, fill=BLUE if i == 0 else MINT, stroke=NAVY if i == 0 else TEAL, size=9.5, bold=True)
    f.text(x + w / 2, 86, b, size=10, color=SLATE, bold=True)
    if i < 3: f.arrow([(x + w, 49), (x + w + 14, 49)], color=SLATE)
    x += w + 14
f.text(290, 110, "each step returns the same jQuery object", size=10.5, color=NAVY, bold=True)
```

```svgfig label="6.3" caption="The animation queue adds up. jQuery('#msg').fadeOut(400).delay(200).slideDown(600) puts three steps in the element's queue: fade out for 400 ms (0 to 400), wait for 200 ms (400 to 600), slide down for 600 ms (600 to 1200). The chain returns at once, so the code after it runs immediately; the animation finishes 1200 ms later. A callback passed as the last argument runs only when that step is done, and .stop() clears the queue when the user clicks again."
f = Fig(580, 150)
x0, sc = 40, 0.36
steps = [("fadeOut 400", 0, 400, RED), ("delay 200", 400, 200, SLATE), ("slideDown 600", 600, 600, TEAL)]
for i, (n, s, d, c) in enumerate(steps):
    f.box(x0 + s * sc * 1.0 + 80, 14 + i * 32, d * sc, 24, n, fill=SOFT, stroke=c, color=c, size=9.5, bold=True, r=3)
f.line(x0 + 80, 118, x0 + 80 + 1200 * sc, 118, color=SLATE)
for t in (0, 400, 600, 1200):
    f.line(x0 + 80 + t * sc, 114, x0 + 80 + t * sc, 122, color=SLATE)
    f.text(x0 + 80 + t * sc, 136, f"{t} ms", size=9.5, color=SLATE)
```

```svgfig label="6.4" caption="Traversal from one element. Starting at the clicked button in a table row: .parent() gives its cell, .closest('tr') climbs to the nearest row, .siblings() gives the other cells of the same parent, .children() the direct descendants and .find('span') searches all descendants. In a delete-row button the usual line is jQuery(this).closest('tr').remove(): the button does not need to know the row number."
f = Fig(580, 200)
f.box(10, 8, 330, 184, "", fill=SOFT, stroke=SLATE)
f.text(20, 24, "tr  (closest('tr') stops here)", size=10, color=NAVY, bold=True, anchor="start")
f.box(24, 44, 100, 50, "td  name", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(132, 44, 100, 50, "td  marks", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(240, 44, 90, 50, "td  action", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(252, 124, 66, 28, "button", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.line(285, 124, 285, 94, color=SLATE)
f.box(24, 120, 100, 50, "", fill="#ffffff", stroke=SLATE, dash=True); f.text(74, 145, "other row", size=9.5, color=SLATE)
for i, (t, c) in enumerate([("this = the button", AMBER), (".parent()  = td action", TEAL), (".closest('tr') = the row", NAVY), (".siblings() = name, marks tds", SLATE), (".remove() deletes the row", RED)]):
    f.text(360, 40 + i * 28, t, size=10.5, color=c, bold=True, anchor="start")
```

```svgfig label="6.5" caption="An AJAX call with jQuery. (1) A click handler calls jQuery.getJSON('/api/results?roll=101', callback). (2) The browser sends the request in the background; the page stays usable. (3) The server answers with a JSON body. (4) jQuery parses it and calls the callback with a JavaScript object, and (5) the callback writes the values into the page. The three promise methods are .done() on success, .fail() on a network or HTTP error and .always() in both cases. Only the changed part of the page is updated, so the user does not see a reload."
f = Fig(580, 214)
f.box(10, 10, 160, 194, "", fill=BLUE, stroke=NAVY); f.text(90, 26, "Browser page", size=11, color=NAVY, bold=True)
f.box(410, 10, 160, 194, "", fill=SAND, stroke=AMBER); f.text(490, 26, "Server", size=11, color=AMBER, bold=True)
f.box(24, 42, 132, 34, "click handler", fill=SOFT, stroke=NAVY, size=10, bold=True)
f.box(24, 148, 132, 40, "callback: write\nresult into page", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(170, 59), (410, 59)], color=NAVY); f.text(290, 50, "1-2  GET /api/results?roll=101", size=10, color=NAVY, bold=True)
f.box(424, 100, 132, 40, "route reads the\ndatabase", fill=SOFT, stroke=AMBER, size=10, bold=True)
f.arrow([(410, 168), (170, 168)], color=TEAL); f.text(290, 158, "3-4  JSON: name, marks", size=10, color=TEAL, bold=True)
f.text(290, 110, "page stays usable", size=10, color=SLATE, bold=True)
f.text(90, 120, "5  update DOM", size=10, color=TEAL, bold=True)
```

### 6.9.1 Eight reasons to use jQuery, and when to avoid it

1. **Short code for common jobs.** One line such as `$("li.done").hide()` selects many elements and acts on all of them. The same job in older plain JavaScript needed a loop and several checks. A college notice page with hundreds of rows can be filtered with a line or two.
2. **Browser differences are hidden.** jQuery was built when browsers disagreed about events, styles and AJAX, and it gave one behaviour everywhere. Old sites in schools and offices still run on older browsers. Using the library meant the same script worked for every visitor.
3. **Powerful selectors and traversal.** CSS-style selectors, filters such as `:first` and `:even`, and methods such as `closest()` and `find()` make it easy to reach any element. A delete button can find its own table row without knowing a row number. This keeps the code short and independent of the layout.
4. **Method chaining.** Each call returns the jQuery object, so selecting, styling and animating can be done in one statement. The chain is read from left to right like a sentence. It also avoids selecting the same element repeatedly.
5. **Built-in effects.** `fadeIn`, `slideToggle` and `animate` add smooth motion without writing timers. A Nepali news site can open and close a menu or notice with a slide. The queue runs the effects in order, as shown in Figure 6.3.
6. **Simple AJAX.** `$.get`, `$.post`, `$.getJSON` and `$.ajax` send background requests with promise methods for success and failure. A form can be submitted and a message shown without reloading the page. This was a big step for Web 2.0 style pages.
7. **Plugins and an ecosystem.** Date pickers, sliders, data tables and validation plugins are available for jQuery and plug into the same selector style. Many admin templates used by Nepali software companies still include them. Reusing a tested plugin saves days of work.
8. **When to avoid it.** Modern JavaScript offers `querySelectorAll`, `classList`, `fetch` and arrow functions, and frameworks such as React and Vue manage the page themselves. A new small project may not need the 87 KB (about 30 KB compressed) library. Keep jQuery for maintaining existing sites and for quick scripts, and learn the plain DOM first.

## Formula and fact sheet

- Pattern: `$(selector).action()`; `$(function(){ … })` runs on DOM ready.
- Get/set: `.text() .html() .val() .attr() .css()`; classes: `.addClass() .removeClass() .toggleClass()`.
- DOM: `.append() .prepend() .after() .before() .remove() .empty() .clone() .each()`.
- Events: `.on(event, [selector], fn)`, `.off()`, `.trigger()`.
- Effects: `.show() .hide() .fadeIn() .slideUp() .animate()`; chaining returns the jQuery object.
- AJAX: `$.get`, `$.post`, `$.ajax`, `.load`.

## Chapter summary

- jQuery selects elements with CSS selectors and applies short methods to all matches.
- It reads and writes content, attributes and styles, builds and removes DOM nodes, and handles events (including delegated ones).
- Effects and chaining make UI code compact; AJAX helpers load data without a page reload.

## Practice

1. Explain `$` and `$(document).ready()`.
2. Write jQuery to hide all paragraphs with class `tip` when a button `#hide` is clicked.
3. Write code to add a new `<li>` with text "Item" to `#list` and change the colour of every `li` to blue.
4. Differentiate `.text()` and `.html()`; `.remove()` and `.empty()`.
5. Explain event delegation in jQuery with an example.
6. What does chaining mean? Write a chained statement.
7. Write an AJAX GET that puts the response text into `#out`.
8. Give two reasons to prefer modern JavaScript over jQuery in a new project.

::: note Answers and worked solutions
**1.** `$` is an alias for `jQuery`; `$(document).ready(fn)` runs `fn` once the DOM is fully built so elements can safely be selected.
**2.** `$("#hide").on("click", function () { $("p.tip").hide(); });`
**3.** `$("#list").append("<li>Item</li>"); $("#list li").css("color", "blue");`
**4.** `.text()` reads/sets plain text; `.html()` reads/sets HTML markup. `.remove()` deletes the element itself; `.empty()` deletes only its children.
**5.** `$("#list").on("click", "li", fn)` attaches one handler to the list that runs for any current or future `li` clicked, via event bubbling.
**6.** Calling several methods in one statement because each returns the jQuery object: `$("#box").addClass("on").fadeIn(200).text("Hi");`
**7.** `$.get("/data.txt", function (t) { $("#out").text(t); });`
**8.** Browsers now provide `querySelector`, `classList`, `fetch` and `addEventListener`; skipping jQuery saves a download and avoids another dependency.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is jQuery? Explain its selectors and the basic syntax with examples.**

*Introduction.* jQuery is a fast, small JavaScript library that simplifies selecting elements, handling events, animating and sending AJAX requests; its basic form is `$(selector).action()` (sections 6.1 and 6.2, Figure 6.1).

1. **Setting up.** Include the library with a script tag (a local file or a CDN) and put code inside `$(document).ready(function () { ... })` or its short form `$(function () { ... })`, so it runs after the DOM is loaded.
2. **Basic selectors.** `$("p")` by element, `$(".done")` by class, `$("#menu")` by id, `$("ul li")` descendants, `$("ul > li")` direct children, `$("a, b")` groups.
3. **Attribute selectors.** `$("input[type='text']")` and `$("a[href^='https']")` select by attribute value.
4. **Filters.** `:first`, `:last`, `:even`, `:odd`, `:not(.done)`, `:eq(2)` and `:contains("Nepal")` narrow a set; indexes start at 0.
5. **The result.** A jQuery object that acts like an array: `.length` gives the number matched, and methods apply to every match.
6. **Syntax of an action.** `$("#msg").text("Saved")`, `$("p").addClass("big")` and `$(".row").hide()`.

```html
<script>
$(function () {
  $("li.done").css("color", "green");
  $("ul > li:first").addClass("first");
  alert($("li").length + " items");
});
</script>
```

*Conclusion.* A jQuery statement selects elements with a CSS-like selector and applies an action to all of them, which makes common DOM tasks one-liners.

**Q2 (5 marks). Compare jQuery with plain JavaScript. Write the jQuery equivalent of a given plain JavaScript snippet and explain method chaining.**

*Introduction.* jQuery is written in JavaScript, so everything it does can also be done without it; the difference is in the amount of code and in browser support (section 6.8, Figures 6.1 and 6.2).

1. **Selecting and acting.** Plain: `document.querySelectorAll(".done").forEach(function (e) { e.style.display = "none"; });`. jQuery: `$(".done").hide();`.
2. **Events.** Plain: `el.addEventListener("click", fn)` on one element. jQuery: `$("button").on("click", fn)` on every matching element at once.
3. **AJAX.** Plain: `fetch(url).then(r => r.json()).then(show)`. jQuery: `$.getJSON(url, show)`.
4. **Chaining.** Methods return the jQuery object, so `$("#box").addClass("on").css("color", "red").fadeOut(400)` runs three actions after one search of the page.
5. **Cost.** jQuery adds about 87 KB (30 KB compressed) and a small speed cost, while modern browsers support nearly everything natively.

| Point | jQuery | Plain JavaScript |
|---|---|---|
| Code length | Short | Longer |
| Browser differences | Hidden | Modern browsers agree |
| Page weight | Adds about 87 KB | None |
| Best for | Maintaining older sites, quick scripts | New projects |

*Conclusion.* jQuery saves code and hides old browser problems, but plain JavaScript is now enough for most new work; chaining is its most useful idea.

**Q3 (10 marks). Explain AJAX with jQuery. Write a program that fetches a student's result as JSON when a button is clicked and shows it in a table, with error handling. Name the jQuery AJAX methods.**

*Introduction.* AJAX (Asynchronous JavaScript and XML) lets a page request data from a server in the background and update only part of the page. It avoids reloading and makes web pages behave like applications. jQuery wraps the browser's XMLHttpRequest in short methods (section 6.7, Figure 6.5).

1. **load().** `$("#box").load("part.html")` fetches an HTML fragment and inserts it into the element.
2. **`$.get()` and `$.post()`.** `$.get(url, data, callback)` sends a GET request and `$.post(url, data, callback)` a POST request with the data in the body.
3. **`$.getJSON()`.** It fetches JSON and passes the parsed object to the callback.
4. **`$.ajax()`.** The general form takes an object with url, method, data, dataType, success, error and timeout; every shortcut calls it.
5. **Promises.** The calls return an object with `.done()` for success, `.fail()` for error and `.always()` for both, which keeps code readable.
6. **Asynchronous behaviour.** The statement after the call runs immediately, before the answer arrives; code that needs the data must be inside the callback.
7. **Security.** Browsers block requests to other origins unless the server allows them with CORS headers. Never insert server text with `.html()` without cleaning it; `.text()` is safe.
8. **User feedback.** Show a loading message and hide it in `.always()`.

```html
<input id="roll" value="101"> <button id="go">Show result</button>
<p id="status"></p>
<table id="res"><tbody></tbody></table>
<script>
$("#go").on("click", function () {
  $("#status").text("Loading...");
  $.getJSON("/api/results", { roll: $("#roll").val() })
    .done(function (r) {
      $("#res tbody").html("<tr><td></td><td></td></tr>");
      $("#res td:first").text(r.name);
      $("#res td:last").text(r.marks);
    })
    .fail(function () { $("#status").text("Could not load the result."); })
    .always(function () { if ($("#status").text() === "Loading...") $("#status").text(""); });
});
</script>
```

| Method | Purpose | Returns data as |
|---|---|---|
| load() | Insert HTML into an element | HTML text |
| `$.get()` | GET request | Text or object |
| `$.post()` | POST request | Text or object |
| `$.getJSON()` | GET JSON | JavaScript object |
| `$.ajax()` | Full control | Any type |

*Conclusion.* jQuery AJAX sends a request, continues at once and runs a callback when the answer comes, so only the needed part of the page changes. `.done()`, `.fail()` and `.always()` give a clear way to handle success, errors and cleanup.
