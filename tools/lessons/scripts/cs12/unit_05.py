import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _cs as C  # noqa: E402


def cls_box(name, attrs, methods, color=th.SKY, w=3.6, size=22):
    top = VGroup(RoundedRectangle(corner_radius=0.08, width=w, height=0.6, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25), T(name, size=size + 4, color=th.INK, weight="BOLD"))
    top[1].move_to(top[0])
    at = VGroup(*[Text(a, font=C.MONO, font_size=size, color=th.INK) for a in attrs]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    me = VGroup(*[Text(m, font=C.MONO, font_size=size, color=th.MINT) for m in methods]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    ab = RoundedRectangle(corner_radius=0.05, width=w, height=at.height + 0.3, stroke_color=color, stroke_width=2, fill_color=th.PANEL, fill_opacity=1)
    mb = RoundedRectangle(corner_radius=0.05, width=w, height=me.height + 0.3, stroke_color=color, stroke_width=2, fill_color=th.PANEL, fill_opacity=1)
    VGroup(top, ab, mb).arrange(DOWN, buff=0)
    at.move_to(ab).align_to(ab, LEFT).shift(RIGHT * 0.2)
    me.move_to(mb).align_to(mb, LEFT).shift(RIGHT * 0.2)
    return VGroup(top, ab, at, mb, me)


class Lesson(Lesson):
    SUBJECT = "cs"
    GRADE = 12
    UNIT = 5
    TITLE = "Object-Oriented Programming"
    SUBTITLE = "Programs built from objects"
    SECTIONS = ["Programming paradigms", "Classes and objects", "Encapsulation and abstraction", "Inheritance", "Polymorphism", "Advantages and applications"]
    NEXT = "Unit 6 · Software Process Model"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        g = VGroup(RoundedRectangle(corner_radius=0.1, width=3.2, height=1.0, stroke_color=th.CORAL, stroke_width=3, fill_color=th.PANEL, fill_opacity=1), Text("marks = 78", font=C.MONO, font_size=28, color=th.INK)).move_to([-3.4, 1.2, 0])
        g[1].move_to(g[0])
        fns = VGroup(*[C.node(t_, th.MUTED, w=2.0, h=0.7, size=24) for t_ in ["print()", "grade()", "bug()"]]).arrange(RIGHT, buff=0.4).move_to([-3.4, -1.2, 0])
        lns = VGroup(*[Line(f_.get_top(), g.get_bottom(), color=th.FAINT) for f_ in fns])
        bad = Text("marks = -500", font=C.MONO, font_size=28, color=th.CORAL).move_to(g[0])
        obj = VGroup(Circle(radius=1.6, stroke_color=th.MINT, stroke_width=4, fill_color=th.PANEL, fill_opacity=1), Circle(radius=0.75, stroke_color=th.INK, stroke_width=2).set_stroke(opacity=0.6), Text("marks", font=C.MONO, font_size=24, color=th.INK)).move_to([3.6, 0.0, 0])
        obj[2].move_to(obj[1])
        meths = VGroup(*[Text(t_, font=C.MONO, font_size=22, color=th.MINT).move_to(obj[0].get_center() + 1.18 * np.array([np.cos(a), np.sin(a), 0])) for t_, a in [("setMarks()", PI / 2), ("grade()", -PI / 6), ("show()", 7 * PI / 6)]])
        rej = T("setMarks(-500) → rejected", size=24, color=th.MINT).next_to(obj, DOWN, buff=0.3)
        VGroup(obj, meths).scale(1.25)
        rej.next_to(obj, DOWN, buff=0.3)
        with self.say("In an ordinary C program, data often sits out in the open, and any function can change it. One buggy function sets a student's marks to minus five hundred, and every report that reads it is now wrong."):
            self.play(FadeIn(g), FadeIn(fns), Create(lns))
            self.play(Indicate(fns[2], color=th.CORAL), Transform(g[1], bad))
        with self.say("Object oriented programming seals the data inside an object. The only way in is through the object's own methods, which can check what they are given. Minus five hundred is simply rejected."):
            self.play(FadeIn(obj), FadeIn(meths))
            self.play(FadeIn(rej))
            nb = C.neby_in(self, "cool", height=1.3)
        C.neby_out(self, nb)
        self.play(FadeOut(VGroup(g, fns, lns, obj, meths, rej)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Computer Science, Unit 5: Object Oriented Programming."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Programming paradigms. Classes and objects. Encapsulation and abstraction. Inheritance. Polymorphism. And the advantages and applications of OOP.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = C.head(self, "Three paradigms")
        cards = VGroup()
        for t_, d_, c_ in [("Procedural", "a sequence of instructions grouped into functions; data mostly global; top-down. FORTRAN, COBOL, C", th.SKY), ("Structured", "procedural with discipline: only sequence, selection, iteration; no goto; modules talk by parameters. C", th.AMBER),
                           ("Object-oriented", "organised around data: objects bundle data with the functions that act on it; bottom-up. C++, Java, Python", th.MINT)]:
            box = RoundedRectangle(corner_radius=0.15, width=3.9, height=3.6, stroke_color=c_, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
            cards.add(VGroup(box, VGroup(T(t_, size=28, color=c_, weight="BOLD"), para(d_, width=3.4, size=22, color=th.BODY)).arrange(DOWN, buff=0.3).move_to(box)))
        cards.arrange(RIGHT, buff=0.3).move_to([0, -0.2, 0])
        with self.say("A paradigm is a style of organising a program. Procedural programming is a sequence of instructions grouped into functions, usually sharing global data, designed top down. Structured programming adds discipline: only sequence, selection and loops, no goto, and modules that talk through parameters. C is both. Object oriented programming organises the program around the data instead: objects that bundle data with the functions that act on it, designed bottom up."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.4))
        self.play(FadeOut(VGroup(h, cards)))
        h = C.head(self, "The same job, two ways: area of a rectangle")
        c1 = C.code(["struct Rect { float len, bre; };", "float area(struct Rect r) {", "    return r.len * r.bre;", "}", "struct Rect r = {12.5, 8.0};"], lang="c", size=22, title="procedural C", max_width=6.4).move_to([-3.5, 0.6, 0])
        c2 = C.code(["class Rect {", "    float len, bre;  // private", "  public:", "    Rect(float l, float b)", "        { len = l; bre = b; }", "    float area()", "        { return len * bre; }", "};", "Rect r(12.5, 8.0);"], lang="c", size=22, title="object-oriented C++", max_width=6.6).move_to([3.5, 0.0, 0])
        nt = VGroup(T("anyone can write r.len = -5;", size=24, color=th.CORAL).next_to(c1, DOWN, buff=0.4), T("r.len is unreachable: only area()", size=24, color=th.MINT).next_to(c2, DOWN, buff=0.4))
        with self.say("Compare. In C, the data and the area function are separate, and nothing stops another part of the program writing a negative length. In C plus plus, the length and breadth are private inside the class; the only way in is the constructor and the only way out is area."):
            self.play(FadeIn(h), FadeIn(c1), FadeIn(c2))
            self.play(FadeIn(nt[0]))
            self.play(FadeIn(nt[1]))
        self.play(FadeOut(VGroup(h, c1, c2, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = C.head(self, "A class is a blueprint; objects are the real things")
        cb = cls_box("Student", ["- name", "- roll", "- marks[3]"], ["+ total()", "+ display()"], th.SKY, w=3.4).move_to([-4.2, 0.0, 0])
        objs = VGroup()
        for k, (nm, r, m) in enumerate([("Sita Rai", 1, "78 85 92"), ("Bikash Thapa", 2, "55 61 48"), ("Mina Gurung", 3, "90 88 95")]):
            box = RoundedRectangle(corner_radius=0.1, width=5.4, height=1.2, stroke_color=th.MINT, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
            txt = VGroup(Text(f"s{k + 1}: Student", font=C.MONO, font_size=22, color=th.MINT), Text(f"{nm}, {r}, [{m}]", font=C.MONO, font_size=20, color=th.INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(box)
            objs.add(VGroup(box, txt).move_to([3.4, 1.7 - 1.6 * k, 0]))
        arrs = VGroup(*[Arrow(cb.get_right(), o_.get_left(), buff=0.15, color=th.FAINT, stroke_width=3) for o_ in objs])
        lab = VGroup(T("class: no memory, just the design", size=22, color=th.SKY).next_to(cb, DOWN, buff=0.3), T("objects: each holds its own values", size=22, color=th.MINT).next_to(objs, DOWN, buff=0.3))
        with self.say("A class is a user defined type that binds data members and member functions under one name. It is only a blueprint: it uses no memory for data. An object is an instance, a real variable of that class, created at run time with its own copy of the data. One Student class, three student objects."):
            self.play(FadeIn(h), FadeIn(cb), FadeIn(lab[0]))
            for a_, o_ in zip(arrs, objs):
                self.play(GrowArrow(a_), FadeIn(o_, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(lab[1]))
        self.play(FadeOut(VGroup(h, cb, objs, arrs, lab)))
        h = C.head(self, "Constructors and destructors")
        cd = C.code(["class Student {", "    string name;  int roll;", "  public:", "    static int count;", '    Student() { name = "not admitted"; roll = 0; count++; }', "    Student(string n, int r) { name = n; roll = r; count++; }", '    ~Student() { cout << "bye "; }', "};", 'Student s1("Sita Rai", 1);    // parameterised'], lang="c", size=24, max_width=12.4).move_to([0, 0.3, 0])
        notes = VGroup(T("same name as the class, no return type", size=24, color=th.AMBER), T("runs automatically on creation", size=24, color=th.AMBER), T("~ destructor runs on destruction", size=24, color=th.CORAL), T("static: one copy shared by all", size=24, color=th.SKY)).arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.18), col_alignments="ll")
        notes.scale_to_fit_width(min(notes.width, 12.4)).next_to(cd, DOWN, buff=0.25)
        with self.say("A constructor is a member function with the same name as the class and no return type. It runs automatically when an object is created, to give the data its starting values. You can have a default constructor and a parameterised one. The destructor, with a tilde, runs automatically when the object is destroyed. And a static member has one copy shared by every object: here, a count of students created."):
            self.play(FadeIn(h))
            C.type_code(self, cd, per_line=0.25)
            self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.25))
        self.play(FadeOut(VGroup(h, cd, notes)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = C.head(self, "Encapsulation: data hiding with access specifiers")
        rings = VGroup()
        c0 = np.array([-3.6, -0.3, 0])
        for r, t_, m_, c_ in [(2.8, "public", "total(), display()", th.SKY), (2.0, "protected", "schoolCode", th.AMBER), (1.2, "private", "name, roll,\nmarks", th.CORAL)]:
            ring = Circle(radius=r, stroke_color=c_, stroke_width=4, fill_color=c_, fill_opacity=0.08).move_to(c0)
            if r > 1.5:
                labs = VGroup(T(t_, size=24, color=c_, weight="BOLD").move_to(c0 + UP * (r - 0.4)), T(m_, size=22, color=c_).move_to(c0 + DOWN * (r - 0.4)))
            else:
                labs = VGroup(T(t_, size=24, color=c_, weight="BOLD"), T(m_, size=20, color=c_)).arrange(DOWN, buff=0.1).move_to(c0)
            rings.add(VGroup(ring, labs))
        outside = VGroup(T("main()", size=26, color=th.INK, weight="BOLD").move_to([2.0, 1.8, 0]), T("derived class", size=26, color=th.INK, weight="BOLD").move_to([2.4, -0.4, 0]))
        a1 = Arrow(outside[0].get_left(), [-1.6, 1.2, 0], buff=0.1, color=th.SKY, stroke_width=4)
        a2 = Arrow(outside[1].get_left(), [-2.2, -0.4, 0], buff=0.1, color=th.AMBER, stroke_width=4)
        blk = VGroup(DashedLine(outside[0].get_left() + DOWN * 0.2, [-2.6, 0.0, 0], color=th.CORAL), Cross(scale_factor=0.18, stroke_color=th.CORAL).move_to([-2.0, 0.4, 0]))
        tb = C.table([["specifier", "same class", "derived", "outside"], ["private", "yes", "no", "no"], ["protected", "yes", "yes", "no"], ["public", "yes", "yes", "yes"]], [2.0, 1.7, 1.4, 1.4], row_h=0.55, size=22, colors=[th.AMBER, th.MINT, th.INK, th.INK]).move_to([3.4, -2.2, 0])
        with self.say("Encapsulation wraps data and its functions into one unit, the class. The result is data hiding. Private members can be used only inside the class. Protected members are also visible to derived classes. Public members form the interface everyone can use. Outside code reaches only the public part."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(r_) for r_ in rings], lag_ratio=0.3))
            self.play(FadeIn(outside), GrowArrow(a1), GrowArrow(a2))
            self.play(Create(blk))
            C.reveal_table(self, tb, 2.0)
        self.play(FadeOut(VGroup(h, rings, outside, a1, a2, blk, tb)))
        h = C.head(self, "Only the interface can change the data")
        cd = C.code(["void setMarks(int i, int m) {", "    if (i >= 0 && i < 3 && m >= 0 && m <= 100)", "        marks[i] = m;", '    else cout << "Invalid mark rejected";', "}", "s2.setMarks(1, 105);    // rejected", "s1.marks[0] = 999;      // compile-time error: private"], lang="c", size=24, max_width=9.6).move_to([0, 0.6, 0])
        ab = VGroup(T("encapsulation = HOW it is hidden (bundling + access specifiers)", size=24, color=th.SKY), T("abstraction = WHAT the user sees (the interface)", size=24, color=th.MINT), T("abstract class: has a pure virtual function, = 0; cannot be instantiated", size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ab.scale_to_fit_width(min(ab.width, 12)).move_to([0, -2.4, 0])
        with self.say("Because marks is private, every change goes through a public setter that can check it. Set a mark of one hundred and five: rejected. Write to marks directly from outside: the compiler refuses. Abstraction is the other side: the user sees only what the object does, not how it is stored. Encapsulation is how it is hidden; abstraction is what is shown."):
            self.play(FadeIn(h))
            C.type_code(self, cd, per_line=0.3)
            self.play(LaggedStart(*[FadeIn(a_) for a_ in ab], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, cd, ab)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = C.head(self, "Inheritance: a Teacher is a Person")

        def nd(t_, p_, col=th.SKY):
            return C.node(t_, col, w=1.95, h=0.66, size=22).move_to(p_)

        def up(a, b):
            return Arrow(a.get_top(), b.get_bottom(), buff=0.05, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.25)

        forms = VGroup()
        specs = [("single", [("Person", (0, 0.9)), ("Student", (0, -0.6))], [(1, 0)]), ("multilevel", [("Person", (0, 1.2)), ("Student", (0, 0.0)), ("Hostel St.", (0, -1.2))], [(1, 0), (2, 1)]),
                 ("multiple", [("Student", (-1.0, 0.9)), ("Athlete", (1.0, 0.9)), ("Scholar", (0, -0.6))], [(2, 0), (2, 1)]), ("hierarchical", [("Person", (0, 0.9)), ("Student", (-1.0, -0.6)), ("Teacher", (1.0, -0.6))], [(1, 0), (2, 0)])]
        for k, (nm, ns, es) in enumerate(specs):
            c = np.array([-5.0 + 3.35 * k, 0.0, 0])
            nodes = [nd(t_, c + np.array([x * 1.05, y, 0])) for t_, (x, y) in ns]
            g = VGroup(*nodes, *[up(nodes[a], nodes[b]) for a, b in es], T(nm, size=24, color=th.AMBER, weight="BOLD").move_to(c + DOWN * 2.0))
            forms.add(g)
        nt = para("Derived class acquires the base class's members, adds its own, may redefine them. Hybrid = a mix of these. Arrows point from derived to base (UML).", width=11.5, size=22, color=th.BODY).move_to([0, -2.9, 0])
        with self.say("Inheritance lets a derived class acquire everything in a base class, then add or redefine members. It gives reuse, and expresses an is a relationship: a teacher is a person. Single inheritance: one base, one derived. Multilevel: a chain. Multiple: one class with two bases. Hierarchical: one base, many derived. And hybrid mixes them."):
            self.play(FadeIn(h))
            for f_ in forms:
                self.play(FadeIn(f_, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, forms, nt)))
        h = C.head(self, "Construction base-first, destruction derived-first")
        steps = VGroup(*[C.node(t_, c_, w=2.2, h=0.8, size=22) for t_, c_ in [("Person()", th.SKY), ("Teacher()", th.SKY), ("in use", th.MUTED), ("~Teacher()", th.CORAL), ("~Person()", th.CORAL)]]).arrange(RIGHT, buff=0.35).move_to([0, 0.6, 0])
        ar = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.03, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.35) for k in range(4)])
        cd = C.code(["class Teacher : public Person { … };"], lang="c", size=26).move_to([0, -1.4, 0])
        with self.say("Create a Teacher object and the Person constructor runs first, then the Teacher constructor: build the foundation before the house. When the object dies, destructors run in exactly the reverse order. A favourite one mark question."):
            self.play(FadeIn(h), FadeIn(cd))
            for k, s_ in enumerate(steps):
                self.play(FadeIn(s_, scale=1.1), *([GrowArrow(ar[k - 1])] if k else []), run_time=0.6)
        self.play(FadeOut(VGroup(h, steps, ar, cd)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = C.head(self, "Compile-time polymorphism: overloading")
        call = C.code(["volume(5, 4, 3)"], lang="c", size=30).move_to([-0.8, 1.8, 0])
        sigs = VGroup(*[C.code([s_], lang="c", size=26) for s_ in ["int volume(int s)                → s*s*s", "int volume(int l, int b, int h)  → l*b*h", "double volume(double r, double h) → πr²h"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -0.45, 0])
        pick = SurroundingRectangle(sigs[1], color=th.MINT, buff=0.06)
        out = T("= 60", size=34, color=th.MINT, font=C.MONO).next_to(call, RIGHT, buff=0.4)
        nt = T("the compiler picks the version whose signature matches", size=24, color=th.MUTED).move_to([0, -2.6, 0])
        with self.say("Polymorphism means many forms: one name, several behaviours. With function overloading, several functions share a name but differ in their parameters. Call volume with three integers, and the compiler, before the program even runs, picks the matching version: sixty. That is compile time polymorphism."):
            self.play(FadeIn(h), FadeIn(call), LaggedStart(*[FadeIn(s_) for s_ in sigs], lag_ratio=0.2))
            self.play(Create(pick), FadeIn(out))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, call, sigs, pick, out, nt)))
        h = C.head(self, "Run-time polymorphism: virtual functions")
        cd = C.code(["class Base {", "  public:", '    void show()         { cout << "Base::show"; }', '    virtual void draw() { cout << "Base::draw"; }', "};", "class Derived : public Base { ... };  // overrides both", "Derived d;  Base *bp = &d;", "bp->show();   // ?", "bp->draw();   // ?"], lang="c", size=22, max_width=8.8).move_to([-2.0, 0.3, 0])
        res = VGroup(VGroup(T("Base::show", size=26, color=th.CORAL, font=C.MONO), T("early binding (not virtual)", size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08), VGroup(T("Derived::draw", size=26, color=th.MINT, font=C.MONO), T("late binding (virtual)", size=22, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([4.8, -0.4, 0])
        with self.say("Run time polymorphism. A base class pointer holds a derived object. Call show, which is not virtual: the compiler binds it early, by the pointer's type, and the base version runs. Call draw, which is virtual: the choice waits until the program runs, looks at the real object, and the derived version runs. That late, dynamic binding is what lets one loop treat teachers and students differently."):
            self.play(FadeIn(h))
            C.type_code(self, cd, per_line=0.25)
            self.play(Indicate(cd.lines[7], color=th.CORAL), FadeIn(res[0]))
            self.play(Indicate(cd.lines[8], color=th.MINT), FadeIn(res[1]))
        self.play(FadeOut(VGroup(h, cd, res)))
        rows = [["", "overloading", "overriding"], ["where", "same class", "base and derived class"], ["signature", "must differ", "must be identical"], ["binding", "early, compile time", "late, run time"], ["needs", "nothing special", "virtual in the base"]]
        tb = C.table(rows, [2.6, 4.2, 4.6], row_h=0.66, size=26, colors=[th.AMBER, th.SKY, th.MINT]).move_to([0, 0.6, 0])
        msg = T("message passing: s1.display() sends a message to the object s1", size=24, color=th.MUTED).move_to([0, -2.3, 0])
        with self.say("Overloading against overriding. Overloading is in one class, with different signatures, resolved at compile time. Overriding redefines a base function in a derived class with the identical signature, resolved at run time, and needs the word virtual. Objects interact by sending messages: calling a member function on a named object.") as v:
            C.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(msg))
        self.play(FadeOut(VGroup(tb, msg)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = C.head(self, "Why OOP?")
        adv = C.bullets(["Reusability: extend a tested class by inheritance", "Data security: private data can't be corrupted by unrelated code", "Easier maintenance: a bug in percentage() lives inside Student", "Modelling: one object per real thing (student, invoice, bus route)",
                         "Extensibility: add a Staff class without touching main()", "Team work: programmers agree only on public interfaces"], width=11.5, size=26).move_to([0, 0.4, 0])
        cost = T("costs: bigger programs, slightly slower, longer design; overkill for a 20-line calculation", size=22, color=th.CORAL).move_to([0, -2.8, 0])
        cost.scale_to_fit_width(min(cost.width, 12.4))
        with self.say("Why use objects? Tested classes can be reused and extended. Private data is safe. A bug can only be in the class that owns the data. Objects mirror real things, so designs are easier to discuss. New features often mean a new class, not edits everywhere. And teams can split the work by class. The costs: larger, slightly slower programs and more design time.") as v:
            self.play(FadeIn(h))
            C.reveal_list(self, adv, v.dur * 0.75)
            self.play(FadeIn(cost))
        self.play(FadeOut(VGroup(h, adv, cost)))
        rows = [["area", "why OOP fits", "tools"], ["user interfaces", "every widget is an object", "Qt, Android"], ["games", "player, enemy, bullet share a base", "Unity, Unreal"], ["simulation", "each entity is an object", "Simula's purpose"], ["web frameworks", "model, controller classes", "Laravel, Django"], ["banking, ERP", "account, customer objects", "Java, C#"]]
        tb = C.table(rows, [3.0, 5.6, 3.4], row_h=0.62, size=25, colors=[th.AMBER, th.INK, th.MUTED]).move_to([0, 0.4, 0])
        with self.say("And where it is used: graphical interfaces, games, simulations, web frameworks, banking and enterprise systems. For a single formula, though, a short procedural program is still the right tool.") as v:
            C.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        self.quiz("When an object of a derived class is created, which constructor runs first?",
                  ["the derived class's", "the base class's", "the destructor", "whichever is virtual"], 1,
                  "Pause and think.",
                  "The base class constructor runs first; destructors run in the reverse order.")
        self.quiz("Function overriding with a virtual function is an example of",
                  ["compile-time polymorphism", "run-time polymorphism", "encapsulation", "multiple inheritance"], 1,
                  "One more.",
                  "Run time polymorphism: the version is chosen from the real object while the program runs.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Procedural/structured: functions + shared data, top-down. OOP: objects, bottom-up.",
            "Class = blueprint; object = instance; constructor (same name, no return type), destructor ~.",
            "Encapsulation + access specifiers (private, protected, public) give data hiding; abstraction shows the interface.",
            "Inheritance: single, multilevel, multiple, hierarchical, hybrid; base constructor first.",
            "Polymorphism: overloading (compile time) vs virtual overriding (run time).",
        ], "Quick recap. Paradigms. Classes, objects, constructors and destructors. Encapsulation and abstraction. The five kinds of inheritance. And polymorphism, at compile time and at run time.")
        self.outro("That was object oriented programming. Next, the software process model: how real software is planned, built and tested. See you there.")
