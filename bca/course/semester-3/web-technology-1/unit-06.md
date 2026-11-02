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
