import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _cs as C  # noqa: E402

DARK = "#222631"


class Lesson(Lesson):
    SUBJECT = "cs"
    GRADE = 12
    UNIT = 3
    TITLE = "Web Technology II"
    SUBTITLE = "JavaScript in the browser, PHP on the server"
    SECTIONS = ["Client-side vs server-side", "JavaScript basics", "Control structures and functions", "Objects, events and validation", "PHP basics", "PHP objects and operators", "PHP and MySQL"]
    NEXT = "Unit 4 · Programming in C"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        br = C.browser("neb.gov.np/result.php", w=6.8, h=3.8).move_to([-3.0, 0.0, 0])
        form = VGroup(Text("Symbol no:", font=C.MONO, font_size=22, color=DARK), RoundedRectangle(corner_radius=0.05, width=2.2, height=0.45, stroke_color="#999", stroke_width=2), RoundedRectangle(corner_radius=0.08, width=1.4, height=0.42, stroke_width=0, fill_color=th.SKY, fill_opacity=1)).arrange(RIGHT, buff=0.2).move_to(br.area).shift(UP * 0.6)
        btn = Text("Check", font=C.MONO, font_size=18, color=WHITE).move_to(form[2])
        typed = Text("2079012345", font=C.MONO, font_size=18, color=DARK).move_to(form[1])
        srv = C.node("web server\nPHP + MySQL", th.MINT, w=2.6, h=1.4, size=26).move_to([5.0, 0.0, 0])
        req = C.packet(th.AMBER, w=0.9, h=0.4, label="request")
        res = C.packet(th.MINT, w=0.9, h=0.4, label="HTML")
        out = Text("GPA 3.65 — PASSED", font=C.MONO, font_size=22, color="#1E7A46").move_to(br.area).shift(DOWN * 0.5)
        with self.say("Results day. You type your symbol number into the board's website and press check. Two kinds of program run. In your browser, JavaScript checks that you typed a sensible number, instantly. Then the request travels to the server, where PHP looks you up in a database and builds a page just for you."):
            self.play(FadeIn(br), FadeIn(form), FadeIn(btn), FadeIn(srv))
            self.play(AddTextLetterByLetter(typed), run_time=1.0)
            self.play(Indicate(form[2], color=th.AMBER))
            req.move_to(br.get_right())
            self.play(FadeIn(req), req.animate.move_to(srv.get_left()), run_time=1.0)
            self.play(Indicate(srv, color=th.MINT))
            res.move_to(srv.get_left())
            self.play(FadeOut(req), FadeIn(res), res.animate.move_to(br.get_right()), run_time=1.0)
            self.play(FadeOut(res), FadeIn(out))
        with self.say("Client side and server side, working together. This unit teaches both: JavaScript for the browser, and PHP with MySQL for the server."):
            nb = C.neby_in(self, "cool", height=1.3)
        C.neby_out(self, nb)
        self.play(FadeOut(VGroup(br, form, btn, typed, srv, out)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Computer Science, Unit 3: Web Technology Two."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Seven parts. Client side and server side scripting. JavaScript basics. Control structures and functions. Objects, events and form validation. PHP basics. PHP objects and operators. And connecting PHP to a MySQL database.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = C.head(self, "Where does the script run?")
        br = C.browser("school.edu.np", w=4.6, h=3.0).move_to([-4.0, 0.3, 0])
        srv = C.node("web server", th.MINT, w=2.6, h=1.0, size=26).move_to([4.0, 0.9, 0])
        db = C.node("database", th.AMBER, w=2.2, h=0.8, size=24).move_to([4.0, -0.9, 0])
        dbl = Line(srv.get_bottom(), db.get_top(), color=th.MUTED, stroke_width=3)
        js = VGroup(T("JavaScript", size=26, color=th.SKY, weight="BOLD"), T("runs here, after the page arrives", size=22, color=th.SKY)).arrange(DOWN, buff=0.08).next_to(br, DOWN, buff=0.25)
        php = VGroup(T("PHP", size=26, color=th.MINT, weight="BOLD"), T("runs here, before the page is sent", size=22, color=th.MINT)).arrange(DOWN, buff=0.08).next_to(db, DOWN, buff=0.25)
        arrs = VGroup(Arrow(br.get_right() + UP * 0.4, srv.get_left() + UP * 0.2, buff=0.1, color=th.AMBER, stroke_width=4), Arrow(srv.get_left() + DOWN * 0.2, br.get_right() + DOWN * 0.2, buff=0.1, color=th.MINT, stroke_width=4))
        al = VGroup(T("HTTP request", size=20, color=th.AMBER).next_to(arrs[0], UP, buff=0.05), T("HTML response", size=20, color=th.MINT).next_to(arrs[1], DOWN, buff=0.05))
        with self.say("A scripting language is interpreted line by line as it runs. On the web there are two places a script can run. Client side scripts, in JavaScript, are downloaded with the page and run in the visitor's browser. Server side scripts, like PHP, run on the web server before the page is sent; the visitor only ever sees their output."):
            self.play(FadeIn(h), FadeIn(br), FadeIn(srv), FadeIn(db), Create(dbl))
            self.play(GrowArrow(arrs[0]), FadeIn(al[0]))
            self.play(GrowArrow(arrs[1]), FadeIn(al[1]))
            self.play(FadeIn(js), FadeIn(php))
        self.play(FadeOut(VGroup(h, br, srv, db, dbl, js, php, arrs, al)))
        rows = [["", "client-side (JavaScript)", "server-side (PHP)"], ["runs in", "the browser", "the web server"], ["source code", "visible to anyone", "never leaves the server"], ["response", "instant, no round trip", "needs a round trip"],
                ["database", "no direct access", "yes: its main job"], ["security", "weak: user can disable it", "strong"], ["typical job", "validation, rollovers", "login, storing data"]]
        tb = C.table(rows, [2.8, 4.6, 4.6], row_h=0.62, size=26, colors=[th.AMBER, th.SKY, th.MINT]).move_to([0, 0.2, 0])
        with self.say("Compare them. Client side code is visible to anyone, answers instantly and costs the server nothing, but cannot reach the database and can be switched off by the user. Server side code is hidden and secure, and can use the database, but every action needs a trip to the server.") as v:
            C.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h = C.head(self, "What happens when you open a page")
        steps = VGroup(*[C.node(t_, c_, w=2.4, h=0.9, size=22) for t_, c_ in [("1 type URL", th.SKY), ("2 DNS → IP", th.AMBER), ("3 HTTP request", th.PINK), ("4 server runs PHP", th.MINT), ("5 HTML back", th.MINT)]]).arrange(RIGHT, buff=0.3).move_to([0, 1.2, 0])
        ar = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.03, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.4) for k in range(4)])
        url = VGroup(T("https://", size=30, color=th.SKY), T("www.neb.gov.np", size=30, color=th.AMBER), T("/notices/result.php", size=30, color=th.MINT), T("?year=2082", size=30, color=th.PINK)).arrange(RIGHT, buff=0.05).move_to([0, -0.6, 0])
        ul = VGroup(*[T(t_, size=20, color=c_).next_to(u_, DOWN, buff=0.15) for t_, c_, u_ in [("protocol", th.SKY, url[0]), ("domain", th.AMBER, url[1]), ("path", th.MINT, url[2]), ("query", th.PINK, url[3])]])
        nt = T("HTTPS = HTTP inside TLS encryption, port 443", size=24, color=th.MUTED).move_to([0, -2.4, 0])
        with self.say("Type an address and five things happen. DNS, the internet's directory, turns the domain name into an IP address. The browser sends an HTTP request. The server runs any script and sends back HTML, which the browser draws. A URL has a protocol, a domain, a path and sometimes a query string. HTTPS is the same protocol, encrypted."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.2), LaggedStart(*[GrowArrow(a_) for a_ in ar], lag_ratio=0.2))
            self.play(FadeIn(url), FadeIn(ul))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, steps, ar, url, ul, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = C.head(self, "JavaScript: types and operators")
        cd = C.code(["var a = 25;        // number", 'var b = "Nepal";   // string', "var c = true;      // boolean", "var d = null;      // null", "var e;             // undefined", "var arr = [10, 20, 30];", "console.log(typeof a, typeof b, typeof arr);"], lang="js", size=24).move_to([-2.2, 0.5, 0])
        out = C.output(["number string object"], size=24).next_to(cd, DOWN, buff=0.3).align_to(cd, LEFT)
        side = VGroup(T("in the page:", size=24, color=th.MUTED), T("<script> … </script>", size=24, color=th.INK, font=C.MONO), T("or in a file:", size=24, color=th.MUTED), T('<script src="app.js">', size=24, color=th.INK, font=C.MONO), para("var / let / const declare variables", width=3.6, size=24, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        side.scale_to_fit_width(min(side.width, 3.7)).move_to([4.85, 0.6, 0])
        with self.say("JavaScript lives in script tags in the page, or in a separate file. Variables are declared with var, let or const, and need no type: the value decides it. Number, string, boolean, null, undefined, and objects such as arrays. The typeof operator tells you which."):
            self.play(FadeIn(h))
            C.type_code(self, cd, per_line=0.3)
            self.play(FadeIn(out), FadeIn(side))
        self.play(FadeOut(VGroup(h, cd, out, side)))
        h = C.head(self, "== compares value; === compares value AND type")
        cd = C.code(["var x = 17, y = 5;", "console.log(x + y, x % y, x / y);", 'console.log(x == "17");', 'console.log(x === "17");', 'console.log("Ram" + " " + "Bahadur");'], lang="js", size=28).move_to([-2.4, 0.8, 0])
        outs = VGroup(*[T(t_, size=28, color=c_, font=C.MONO) for t_, c_ in [("22 2 3.4", th.INK), ("true", th.MINT), ("false", th.CORAL), ("Ram Bahadur", th.INK)]])
        for o_, ln in zip(outs, cd.lines[1:]):
            o_.move_to([4.2, ln.get_y(), 0])
        expl = para("== converts the string \"17\" to a number first; === refuses because the types differ. Prefer ===.", width=11, size=24, color=th.AMBER).move_to([0, -2.2, 0])
        with self.say("Operators. Arithmetic, including percent for the remainder. Then a favourite exam question: seventeen double equals the string seventeen is true, because JavaScript converts the string to a number first. Triple equals is false: the types differ. Use triple equals unless you really want the conversion. And plus between strings joins them."):
            self.play(FadeIn(h), FadeIn(cd))
            for o_ in outs:
                self.play(FadeIn(o_, shift=LEFT * 0.2), run_time=0.6)
            self.play(FadeIn(expl))
        self.play(FadeOut(VGroup(h, cd, outs, expl)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = C.head(self, "A loop, traced")
        cd = C.code(["var sum = 0;", "for (var i = 1; i <= 10; i++) {", "    sum = sum + i;", "}", 'console.log("Sum 1..10 =", sum);'], lang="js", size=28).move_to([-2.8, 0.6, 0])
        it = ValueTracker(0)
        rd = always_redraw(lambda: VGroup(VGroup(T("i =", size=30, color=th.MUTED), Integer(int(it.get_value()), font_size=40, color=th.AMBER)).arrange(RIGHT, buff=0.15),
                                          VGroup(T("sum =", size=30, color=th.MUTED), Integer(int(it.get_value()) * (int(it.get_value()) + 1) // 2, font_size=40, color=th.MINT)).arrange(RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, 0.8, 0]))
        hl = SurroundingRectangle(cd.lines[2], color=th.AMBER, buff=0.06)
        out = C.output(["Sum 1..10 = 55"], size=26).move_to([0, -2.2, 0])
        with self.say("Control structures decide which statements run and how often. A for loop has a start, a test and a step. Trace it: i is one, sum becomes one; i is two, sum becomes three; and so on, until i passes ten. The sum is fifty five."):
            self.play(FadeIn(h), FadeIn(cd))
            self.add(rd)
            self.play(Create(hl))
            for k in range(1, 11):
                self.play(it.animate.set_value(k), run_time=0.35 if k > 3 else 0.6)
            self.play(FadeIn(out))
        self.play(FadeOut(VGroup(h, cd, hl, out)), FadeOut(rd))
        self.remove(rd)
        rows = [["structure", "use", "example"], ["if … else if … else", "two or more choices", "division from marks"], ["switch … case … break", "one of many values", "day number → day name"], ["for", "a known number of times", "sum 1 to 10"],
                ["while", "test first, may run 0 times", "factorial"], ["do … while", "test last, runs at least once", "odd numbers 1 to 9"]]
        tb = C.table(rows, [4.2, 4.4, 3.6], row_h=0.62, size=25, colors=[th.SKY, th.INK, th.MUTED]).move_to([0, 0.5, 0])
        fn = C.code(["function area(l, b) { return l * b; }", "console.log(area(8, 5));   // 40"], lang="js", size=26).move_to([0, -2.3, 0])
        with self.say("The full set: if else for choices, switch for one of many values, for for a known count, while which tests first, and do while which always runs at least once. A function is a named block that takes parameters and can return a value: area of eight by five is forty.") as v:
            C.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(fn))
        self.play(FadeOut(VGroup(tb, fn)))
        C.worked(self, "Print the multiplication table of n = 7 from 1 to 10. Why must (n * i) be in brackets?",
                 [C.code(["for (var i = 1; i <= 10; i++)", '    document.write(n + " x " + i + " = " + (n * i) + "<br>");'], lang="js", size=26), C.output(["7 x 1 = 7", "7 x 2 = 14", "…", "7 x 10 = 70"], size=24),
                  T('without brackets: "7 x 1 = " + 7 + 1 → "7 x 1 = 71"', size=26, color=th.CORAL)],
                 ["A classic.", "Loop i from one to ten and write one line each time.", "The output: seven, fourteen, up to seventy.", "Without the brackets, plus works left to right on a string, so seven and one are glued on: seventy one. The brackets force the multiplication first."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = C.head(self, "Objects: properties and methods")
        cd = C.code(["function Student(name, marks) {", "    this.name  = name;", "    this.marks = marks;", "    this.result = function () {", '        return this.marks >= 40 ? "Pass" : "Fail";', "    };", "}", 'var s1 = new Student("Anisha", 78);', "console.log(s1.name, s1.result());"], lang="js", size=24).move_to([-1.6, 0.4, 0])
        out = C.output(["Anisha Pass"], size=24).next_to(cd, RIGHT, buff=0.4).align_to(cd, DOWN)
        nt = T("JavaScript is object-based: objects, constructors, built-ins (String, Math, Array, Date)", size=22, color=th.MUTED).move_to([0, -2.8, 0])
        with self.say("An object bundles data, its properties, with functions, its methods. A constructor function builds objects: new Student creates one with a name, marks, and a result method. JavaScript is called object based: it has objects and built in ones like Math and Array."):
            self.play(FadeIn(h))
            C.type_code(self, cd, per_line=0.25)
            self.play(FadeIn(out), FadeIn(nt))
        self.play(FadeOut(VGroup(h, cd, out, nt)))
        h = C.head(self, "Events: when something happens, run a handler")
        br = C.browser("events.html", w=5.0, h=3.2).move_to([-3.6, 0.2, 0])
        btn = VGroup(RoundedRectangle(corner_radius=0.08, width=1.8, height=0.5, stroke_width=0, fill_color=th.SKY, fill_opacity=1), Text("Click me", font=C.MONO, font_size=20, color=WHITE)).move_to(br.area).shift(UP * 0.5)
        msg = Text("Namaste!", font=C.MONO, font_size=26, color="#1E7A46").move_to(br.area).shift(DOWN * 0.5)
        cur = Triangle(stroke_width=0, fill_color=WHITE, fill_opacity=1).scale(0.12).rotate(PI / 6).move_to(br.area.get_corner(DR) + UL * 0.4)
        cd = C.code(['<button onclick="greet()">Click me</button>', '<p id="msg"></p>', "<script>", "function greet() {", '  document.getElementById("msg")', '          .innerHTML = "Namaste!";', "}", "</script>"], lang="js", size=22).move_to([3.0, 0.2, 0])
        ev = T("onclick · onload · onmouseover · onchange · onsubmit · onkeyup", size=24, color=th.AMBER).move_to([0, -2.7, 0])
        with self.say("An event is something that happens on the page: a click, a key press, the page loading. An event handler is the function that runs in response. Click the button: onclick calls greet, which finds the paragraph by its id and changes its contents."):
            self.play(FadeIn(h), FadeIn(br), FadeIn(btn), FadeIn(cd), FadeIn(cur))
            self.play(cur.animate.move_to(btn.get_center() + DR * 0.1), run_time=0.8)
            self.play(Indicate(btn, color=th.AMBER), Indicate(cd.lines[0], color=th.AMBER))
            self.play(Indicate(VGroup(cd.lines[4], cd.lines[5]), color=th.MINT), FadeIn(msg, scale=1.3))
            self.play(FadeIn(ev))
        self.play(FadeOut(VGroup(h, br, btn, msg, cur, cd, ev)))
        h = C.head(self, "Form validation: check before sending")
        flow = VGroup(*[C.node(t_, c_, w=3.2, h=0.8, size=22) for t_, c_ in [("user fills the form", th.SKY), ("JavaScript check", th.AMBER), ("send to server", th.MUTED), ("PHP check", th.AMBER), ("save to database", th.MINT)]]).arrange(DOWN, buff=0.35).move_to([-3.6, -0.3, 0])
        far = VGroup(*[Arrow(flow[k].get_bottom(), flow[k + 1].get_top(), buff=0.04, color=th.MUTED, stroke_width=3) for k in range(4)])
        rej = VGroup(*[VGroup(Arrow(flow[k].get_right(), flow[k].get_right() + RIGHT * 1.2, buff=0.05, color=th.CORAL, stroke_width=3), T(t_, size=20, color=th.CORAL).next_to(flow[k].get_right() + RIGHT * 1.2, RIGHT, buff=0.1)) for k, t_ in ((1, "alert, return false"), (3, "reject, resend form"))])
        cd = C.code(["function validate() {", '  if (f.uname.value === "") {', '    alert("Name must not be empty");', "    return false;   // cancels submit", "  }", '  if (f.email.value.indexOf("@") === -1)', "    return false;", "  return true;", "}"], lang="js", size=20).move_to([3.8, -0.4, 0])
        with self.say("Form validation checks what the user typed before it is sent. The form's onsubmit calls a function; returning false cancels the submission, returning true lets it go. The browser check is for convenience: instant feedback. But users can switch JavaScript off, so the server must check again before anything is saved."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(f_) for f_ in flow], lag_ratio=0.15), LaggedStart(*[GrowArrow(a_) for a_ in far], lag_ratio=0.15))
            self.play(FadeIn(rej))
            self.play(FadeOut(rej), FadeIn(cd))
        self.play(FadeOut(VGroup(h, flow, far, cd)))
        rows = [["task", "plain JavaScript", "jQuery"], ["select by id", 'document.getElementById("msg")', '$("#msg")'], ["change content", 'el.innerHTML = "hi"', '$("#msg").html("hi")'], ["handle a click", "el.onclick = fn", '$("#btn").click(fn)'], ["fade out", "several lines", '$("#box").fadeOut(500)']]
        tb = C.table(rows, [3.0, 5.6, 4.0], row_h=0.62, size=24, colors=[th.INK, th.SKY, th.MINT]).move_to([0, 0.3, 0])
        nt = T('jQuery (2006): "write less, do more" — a library that wraps the DOM in $', size=24, color=th.AMBER).move_to([0, -2.2, 0])
        with self.say("jQuery is a JavaScript library whose motto is write less, do more. It wraps everything in one function, the dollar sign: select by id, change content, handle clicks, and animate, each in a short line.") as v:
            C.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = C.head(self, "The server stack: XAMPP / LAMP")
        layers = VGroup(*[C.node(t_, c_, w=6.6, h=0.75, size=24) for t_, c_ in [("MySQL / MariaDB — stores the data", th.MINT), ("PHP interpreter — runs .php files", th.PINK), ("Apache web server", th.SKY), ("Operating system: Linux / Windows", th.MUTED)]]).arrange(DOWN, buff=0.12).move_to([-2.4, 0.2, 0])
        side = VGroup(T("1  save in htdocs/", size=26, color=th.INK), T("2  start Apache and MySQL", size=26, color=th.INK), T("3  open localhost/file.php", size=26, color=th.AMBER), para("double-clicking the file won't run PHP", width=4.8, size=24, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        side.scale_to_fit_width(min(side.width, 5.0)).move_to([4.0, 0.2, 0])
        with self.say("PHP, created by Rasmus Lerdorf in nineteen ninety four, runs on a web server stack: an operating system, the Apache web server, the PHP interpreter and a MySQL database. XAMPP bundles them. Save your file in the htdocs folder, start Apache and MySQL, and open it through localhost. Double clicking the file will not run the PHP at all."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(l_, shift=UP * 0.15) for l_ in reversed(layers)], lag_ratio=0.2))
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, layers, side)))
        h = C.head(self, "PHP syntax: $variables, echo, foreach")
        cd = C.code(["<?php", "$name  = \"Anisha\";      // string", "$marks = array(\"Computer\" => 78,", "               \"Maths\" => 65);", "foreach ($marks as $sub => $m) {", "    echo \"$sub = $m\\n\";", "}", "echo array_sum($marks);", "?>"], lang="js", size=24).move_to([-2.0, 0.3, 0])
        out = C.output(["Computer = 78", "Maths = 65", "143"], size=24).move_to([4.4, 0.9, 0])
        rules = VGroup(*[para(t_, width=4.4, size=24, color=th.MUTED) for t_ in ["statements end with ;", "variables start with $, case sensitive", "8 types: int, float, string, bool, array, object, NULL, resource"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.5, -1.5, 0])
        with self.say("PHP code sits between less than question mark php and question mark greater than. Every variable starts with a dollar sign, and every statement ends with a semicolon. An associative array stores key value pairs, and foreach walks through them. Double quotes substitute variables into the text."):
            self.play(FadeIn(h))
            C.type_code(self, cd, per_line=0.3)
            self.play(FadeIn(out), FadeIn(rules))
        self.play(FadeOut(VGroup(h, cd, out, rules)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = C.head(self, "PHP is fully object-oriented")
        cd = C.code(["class Student {", "    public $name, $marks;", "    function __construct($n, $m) {", "        $this->name = $n;  $this->marks = $m;  }", "    function result() {", '        return $this->marks >= 40 ? "Pass" : "Fail";  }', "}",
                     "class ScienceStudent extends Student { … }", '$s = new Student("Chandra", 85);', "echo $s->name, $s->result();"], lang="js", size=24, max_width=8.6).to_edge(LEFT, buff=0.3).set_y(-0.35)
        notes = VGroup(*[para(t_, width=3.7, size=24, color=th.AMBER) for t_ in ["$this-> reaches the object's own members", "new ClassName(…) makes an object", "-> (not .) reaches a member", "extends = inheritance; parent:: calls the base"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        notes.move_to([4.95, -0.3, 0])
        with self.say("Unlike JavaScript, PHP has full classes. A class declares properties and methods; the constructor sets them up. Inside the class, this arrow refers to the object's own members. new creates an object, and the arrow, not a dot, reaches its members. extends gives inheritance."):
            self.play(FadeIn(h))
            C.type_code(self, cd, per_line=0.22)
            self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.25))
        self.play(FadeOut(VGroup(h, cd, notes)))
        h = C.head(self, "In PHP, + adds and . joins")
        rows = VGroup(*[VGroup(C.code([a], lang="js", size=28), T("→", size=30, color=th.MUTED), T(b, size=30, color=c_, font=C.MONO)).arrange(RIGHT, buff=0.4) for a, b, c_ in [('"5" + 3    // PHP', "8", th.MINT), ('"5" . 3    // PHP', '"53"', th.AMBER), ('"5" + 3    // JavaScript', '"53"', th.CORAL), ("2 + 3 * 4", "14", th.INK)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.4, 0])
        nt = para("Precedence: () first, then * / %, then + − ., then comparisons, then && ||, then assignment. When in doubt, add brackets.", width=11, size=24, color=th.MUTED).move_to([0, -2.6, 0])
        with self.say("A trap when switching languages. In PHP, plus always adds: the string five plus three is the number eight. To join strings, PHP uses a dot. JavaScript does the opposite: plus with a string joins. And remember precedence: multiplication before addition, so two plus three times four is fourteen."):
            self.play(FadeIn(h))
            for r_ in rows:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, rows, nt)))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        h = C.head(self, "Five steps to talk to MySQL")
        steps = [("1 CONNECT", '$conn = new mysqli("localhost", "root", "", "school");'), ("2 CHECK", 'if ($conn->connect_error) die("failed");'), ("3 QUERY", '$res = $conn->query("SELECT … FROM students");'),
                 ("4 FETCH", "while ($row = $res->fetch_assoc()) echo $row[\"name\"];"), ("5 CLOSE", "$conn->close();")]
        rows = VGroup(*[VGroup(C.node(a, th.AMBER, w=2.0, h=0.62, size=20), C.code([b], lang="js", size=20)).arrange(RIGHT, buff=0.3) for a, b in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, 0.0, 0])
        with self.say("Every PHP program that uses a database follows the same five steps. Connect, with the host, user, password and database name. Check the connection. Send a query. Fetch the rows, usually in a while loop, because fetch returns false when the rows run out. And close the connection."):
            self.play(FadeIn(h))
            for r_ in rows:
                self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.7)
        self.play(FadeOut(VGroup(h, rows)))
        h = C.head(self, "From a result set to an HTML table")
        cd = C.code(['echo "<table border=\'1\'>";', "while ($row = $res->fetch_assoc()) {", '    echo "<tr><td>" . $row["roll"] . "</td>"', '       . "<td>" . $row["name"] . "</td></tr>";', "}", 'echo "</table>";'], lang="js", size=22).move_to([-2.8, 0.6, 0])
        br = C.browser("localhost/list.php", w=5.0, h=3.6).move_to([4.1, 0.0, 0])
        names = ["Anisha Shrestha", "Bikash Tamang", "Chandra Gurung", "Deepa Yadav", "Eliza Rai"]
        tbl = VGroup(*[VGroup(Rectangle(width=0.8, height=0.4, stroke_color="#555", stroke_width=1.5), Rectangle(width=3.2, height=0.4, stroke_color="#555", stroke_width=1.5)).arrange(RIGHT, buff=0) for _ in range(5)]).arrange(DOWN, buff=0).move_to(br.area)
        txt = VGroup(*[VGroup(Text(str(k + 1), font=C.MONO, font_size=18, color=DARK).move_to(tbl[k][0]), Text(n_, font=C.MONO, font_size=18, color=DARK).move_to(tbl[k][1])) for k, n_ in enumerate(names)])
        hl = SurroundingRectangle(VGroup(cd.lines[1], cd.lines[2], cd.lines[3]), color=th.AMBER, buff=0.06)
        fx = [["function", "read the name"], ["fetch_assoc()", '$row["name"]'], ["fetch_row()", "$row[1]"], ["fetch_array()", "either"], ["fetch_object()", "$row->name"]]
        ft = C.table(fx, [3.4, 3.0], row_h=0.44, size=22, colors=[th.SKY, th.AMBER]).move_to([-3.4, -2.3, 0])
        with self.say("The commonest practical question: print a query's rows as an HTML table. Echo the opening table tag, then loop: each fetched row becomes one table row. The browser draws the result. fetch assoc gives an array keyed by column name; fetch row by number; fetch object gives an object."):
            self.play(FadeIn(h), FadeIn(cd), FadeIn(br), Create(hl))
            for k in range(5):
                self.play(FadeIn(tbl[k]), FadeIn(txt[k]), Indicate(hl, color=th.AMBER), run_time=0.45)
            C.reveal_table(self, ft, 2.5)
        self.play(FadeOut(VGroup(h, cd, br, tbl, txt, hl, ft)))
        h = C.head(self, "SQL injection, and how to stop it")
        bad = C.code(['"SELECT * FROM users WHERE name=\'" . $_POST["u"] . "\'"'], lang="js", size=24).move_to([0, 1.6, 0])
        typed = C.code(["user types:  ' OR '1'='1"], lang="none", size=26).move_to([0, 0.6, 0])
        res = T("WHERE name='' OR '1'='1'  → true for EVERY row", size=26, color=th.CORAL, font=C.MONO).move_to([0, -0.3, 0])
        good = C.code(['$stmt = $conn->prepare("SELECT name FROM students WHERE marks > ?");', '$stmt->bind_param("i", $limit);', "$stmt->execute();"], lang="js", size=22).move_to([0, -1.9, 0])
        with self.say("Never paste user input straight into a query. If someone types quote, OR one equals one, the condition becomes true for every row, and they get everything. That is SQL injection. Use a prepared statement instead: the query has a question mark placeholder, and the value is bound separately, so it can never change the query's meaning."):
            self.play(FadeIn(h), FadeIn(bad))
            self.play(FadeIn(typed))
            self.play(FadeIn(res))
            self.play(FadeIn(good))
        self.play(FadeOut(VGroup(h, bad, typed, res, good)))
        self.quiz("In JavaScript, 17 === \"17\" evaluates to",
                  ["true", "false", "17", "an error"], 1,
                  "Pause and think.",
                  "False: triple equals checks the type too, and a number is not a string. Double equals would say true.")
        self.quiz("Which is TRUE of server-side scripting?",
                  ["its source code is sent to the browser", "it can access the database", "it runs without a web server", "it cannot be secured"], 1,
                  "One more.",
                  "It can access the database: that is its main job. Its source never reaches the browser.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Client-side (JavaScript) runs in the browser; server-side (PHP) runs on the server and reaches the database.",
            "JS: var/let, typeof, === vs ==, if/switch/for/while/do-while, functions, objects.",
            "Events (onclick, onsubmit…) run handlers; validation returns false to cancel; jQuery uses $.",
            "PHP: <?php … ?>, $vars, arrays, foreach; classes with $this->, new, extends; . joins strings.",
            "MySQL from PHP: connect, check, query, fetch in a loop, close; use prepared statements.",
        ], "Quick recap. JavaScript in the browser, PHP on the server. JavaScript types, operators and control structures. Events and validation. PHP syntax and classes. And the five steps of database connectivity, with prepared statements against SQL injection.")
        self.outro("That was web technology. Next, programming in C: functions, pointers, structures and files. See you there.")
