import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _cs as C  # noqa: E402


def cell(val, color=th.SKY, w=1.3, h=0.8, size=30):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
    return VGroup(r, Text(str(val), font=C.MONO, font_size=size, color=th.INK).move_to(r))


class Lesson(Lesson):
    SUBJECT = "cs"
    GRADE = 12
    UNIT = 4
    TITLE = "Programming in C"
    SUBTITLE = "Functions, recursion, structures, pointers and files"
    SECTIONS = ["Functions", "Storage classes", "Recursion", "Structures and unions", "Pointers", "Data files"]
    NEXT = "Unit 5 · Object-Oriented Programming"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        cd = C.code(["void swap(int a, int b) {", "    int t = a; a = b; b = t;", "}", "int main() {", "    int x = 10, y = 20;", "    swap(x, y);", '    printf("%d %d", x, y);', "}"], lang="c", size=28).move_to([-2.8, 0.3, 0])
        out = C.output(["10 20"], size=32).move_to([4.0, 0.9, 0])
        q = VGroup(T("Why didn't they swap?", size=32, color=th.CORAL, weight="BOLD"), para("swap() changed its own copies. To change x and y, it needs their addresses: pointers.", width=5.0, size=24, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, -1.0, 0])
        with self.say("Here is a function that swaps two numbers. Call it with ten and twenty, print them, and you get ten twenty. Nothing swapped. Why?"):
            C.type_code(self, cd, per_line=0.3)
            self.play(FadeIn(out))
        with self.say("Because C passes copies. The function swapped its own copies and threw them away. To reach the originals it needs their addresses: pointers. By the end of this unit you will be able to fix it, and much more."):
            self.play(FadeIn(q))
            nb = C.neby_in(self, "think", height=1.3)
        C.neby_out(self, nb)
        self.play(FadeOut(VGroup(cd, out, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Computer Science, Unit 4: Programming in C."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Functions: prototypes, definitions and calls. Storage classes. Recursion. Structures and unions. Pointers, with call by value and call by reference. And data files.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = C.head(self, "A function: prototype, call, definition")
        cd = C.code(["#include <stdio.h>", "int larger(int a, int b);        /* prototype */", "int main() {", "    int x = 47, y = 92;", '    printf("%d", larger(x, y));  /* call */', "    return 0;", "}", "int larger(int a, int b) {        /* definition */", "    if (a > b) return a;", "    return b;", "}"],
                    lang="c", size=24, max_width=7.4).to_edge(LEFT, buff=0.35).set_y(-0.1)
        lab = VGroup(*[para(t_, width=4.0, size=24, color=c_) for t_, c_ in [("prototype: tells the compiler the name, return type, parameters", th.AMBER), ("call: jumps to the function with the arguments", th.SKY), ("definition: the body; return sends a value back", th.MINT)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, 0.4, 0])
        with self.say("A function is a named block that does one job. Library functions, like printf, come with C; user defined functions you write yourself. Three parts. The prototype announces the function before main. The call, here inside printf, jumps to it with the arguments forty seven and ninety two. The definition is the body, and return sends the answer back."):
            self.play(FadeIn(h), FadeIn(cd))
            self.play(Indicate(cd.lines[1], color=th.AMBER), FadeIn(lab[0]))
            self.play(Indicate(cd.lines[4], color=th.SKY), FadeIn(lab[1]))
            a1 = CurvedArrow(np.array([cd.box.get_right()[0], cd.lines[4].get_y(), 0]), np.array([cd.box.get_right()[0], cd.lines[7].get_y(), 0]), angle=-PI / 2, color=th.SKY)
            self.play(Create(a1))
            self.play(Indicate(VGroup(cd.lines[8], cd.lines[9]), color=th.MINT), FadeIn(lab[2]))
            a2 = CurvedArrow(np.array([cd.box.get_left()[0], cd.lines[9].get_y(), 0]), np.array([cd.box.get_left()[0], cd.lines[4].get_y(), 0]), angle=-PI / 2, color=th.MINT)
            self.play(Create(a2))
        out = C.output(["92"], size=28).move_to([4.6, -2.0, 0])
        adv = T("advantages: reuse, easier testing, shorter and clearer programs", size=22, color=th.MUTED).to_edge(DOWN, buff=0.35)
        with self.say("It prints ninety two. Functions let you reuse code, test it piece by piece, and keep programs short and clear."):
            self.play(FadeIn(out), FadeIn(adv))
        self.play(FadeOut(VGroup(h, cd, lab, a1, a2, out, adv)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = C.head(self, "auto vs static: born again, or remembered?")
        cd = C.code(["int counter_auto(void) {", "    auto int c = 0;  c++;  return c;", "}", "int counter_static(void) {", "    static int c = 0;  c++;  return c;", "}"], lang="c", size=24).move_to([0, 1.05, 0])
        ab = cell(0, th.SKY).move_to([-3.6, -1.75, 0])
        sb = cell(0, th.AMBER).move_to([3.0, -1.75, 0])
        al = T("auto c (stack)", size=24, color=th.SKY).next_to(ab, UP, buff=0.15)
        sl = T("static c (data segment)", size=24, color=th.AMBER).next_to(sb, UP, buff=0.15)
        aout, sout = VGroup(), VGroup()
        with self.say("Call each counter three times. The automatic variable is created fresh, on the stack, every call: set to nought, increased to one, returned, destroyed. One, one, one. The static variable is created once and lives for the whole program: one, two, three."):
            self.play(FadeIn(h), FadeIn(cd), FadeIn(al), FadeIn(sl))
            for k in range(3):
                a_new = cell(1, th.SKY).move_to(ab)
                self.play(FadeIn(a_new, scale=1.2), run_time=0.35)
                o = T("1", size=30, color=th.SKY, font=C.MONO).move_to([-3.6 + 0.6 * k, -2.85, 0])
                self.play(FadeIn(o), FadeOut(a_new, scale=0.6), run_time=0.35)
                aout.add(o)
                s_new = cell(k + 1, th.AMBER).move_to(sb)
                self.play(Transform(sb, s_new), run_time=0.35)
                o2 = T(str(k + 1), size=30, color=th.AMBER, font=C.MONO).move_to([3.0 + 0.6 * k - 0.6, -2.85, 0])
                self.play(FadeIn(o2), run_time=0.3)
                sout.add(o2)
        self.play(FadeOut(VGroup(h, cd, ab, sb, al, sl, aout, sout)))
        rows = [["class", "stored in", "default", "scope", "lifetime"], ["auto", "stack", "garbage", "its block", "until the block ends"], ["extern", "data segment", "0", "whole program", "whole program"], ["static", "data segment", "0", "its block / file", "whole program"], ["register", "CPU register", "garbage", "its block", "until the block ends"]]
        tb = C.table(rows, [2.0, 2.6, 1.8, 2.8, 3.2], row_h=0.66, size=24, colors=[th.AMBER, th.INK, th.CORAL, th.INK, th.MINT]).move_to([0, 0.5, 0])
        nt = para("An automatic variable without '= 0' contains rubbish, not zero. Only extern and static start at 0.", width=11, size=24, color=th.CORAL).move_to([0, -2.4, 0])
        with self.say("A storage class decides where a variable lives, its starting value, where it can be seen, and how long it lasts. Auto is the default for local variables. Extern variables are global, visible everywhere. Static ones keep their value. Register asks for a fast CPU register. And beware: an automatic variable you forget to initialise contains rubbish, not zero.") as v:
            C.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = C.head(self, "Recursion: factorial(4)")
        cd = C.code(["long factorial(int n) {", "    if (n == 0 || n == 1) return 1;   /* base case */", "    return n * factorial(n - 1);     /* recursive case */", "}"], lang="c", size=24).move_to([0, 2.0, 0])
        frames = VGroup()
        for k, n in enumerate([4, 3, 2, 1]):
            txt = f"factorial({n}) = {n} * factorial({n - 1})" if n > 1 else "factorial(1) = 1   base case"
            b = VGroup(RoundedRectangle(corner_radius=0.08, width=6.4, height=0.62, stroke_color=th.AMBER if n == 1 else th.SKY, stroke_width=3, fill_color=th.PANEL, fill_opacity=1), Text(txt, font=C.MONO, font_size=22, color=th.INK))
            b[1].move_to(b[0])
            b.move_to([-1.6, 0.5 - 0.75 * k, 0])
            frames.add(b)
        rets = VGroup(*[T(f"= {v}", size=30, color=th.MINT, font=C.MONO).next_to(frames[k], RIGHT, buff=0.4) for k, v in enumerate([24, 6, 2, 1])])
        with self.say("Recursion is a function calling itself. Every recursive function needs a base case that stops it, and a recursive case that moves towards it. Call factorial of four. It needs factorial of three, which needs factorial of two, which needs factorial of one: the base case. Each waiting call sits on the stack."):
            self.play(FadeIn(h), FadeIn(cd))
            for f_ in frames:
                self.play(FadeIn(f_, shift=DOWN * 0.2), run_time=0.6)
        with self.say("Now the stack unwinds. Factorial of one returns one. Two times one is two. Three times two is six. Four times six is twenty four."):
            for r_ in reversed(rets):
                self.play(FadeIn(r_, shift=LEFT * 0.2), run_time=0.6)
        self.play(FadeOut(VGroup(h, cd, frames, rets)))
        rows = [["", "recursion", "loop"], ["stops when", "base case reached", "condition false"], ["memory", "a stack frame per call", "one set of variables"], ["speed", "slower", "faster"], ["code", "short, like the maths", "longer, plainer"], ["danger", "stack overflow", "infinite loop"]]
        tb = C.table(rows, [2.6, 4.6, 4.4], row_h=0.62, size=25, colors=[th.AMBER, th.SKY, th.MINT]).move_to([0, 0.5, 0])
        fib = C.output(["Fibonacci: 0 1 1 2 3 5 8 13 21 34"], size=24).move_to([0, -2.6, 0])
        with self.say("Recursion against a loop. Recursion is shorter and mirrors the mathematical definition, but every call costs a stack frame, so it is slower and can overflow. The Fibonacci series is the other classic: each term is the sum of the two before it.") as v:
            C.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(fib))
        self.play(FadeOut(VGroup(tb, fib)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = C.head(self, "A structure groups different types")
        cd = C.code(["struct student {", "    int  roll;   char  name[20];", "    char faculty[12];  float marks;", "};", "struct student s1 =", '    {1, "Anisha", "Science", 78.5};'], lang="c", size=24, max_width=7.0).to_edge(LEFT, buff=0.4).set_y(0.75)
        seg = [("roll", 4, th.SKY), ("name[20]", 20, th.MINT), ("faculty[12]", 12, th.AMBER), ("marks", 4, th.PINK)]
        mem = VGroup()
        x = -6.2
        for nm, b, c_ in seg:
            w = b * 0.3
            r = Rectangle(width=w, height=0.7, stroke_color=th.BG, stroke_width=2, fill_color=c_, fill_opacity=0.6).move_to([x + w / 2, -1.8, 0])
            mem.add(VGroup(r, T(nm, size=20 if w > 1.5 else 16, color=th.INK).move_to(r), T(f"{b} B", size=18, color=th.MUTED).next_to(r, DOWN, buff=0.08)))
            x += w
        tot = T("sizeof = 4 + 20 + 12 + 4 = 40 bytes", size=26, color=th.MINT).move_to([0, -3.0, 0])
        acc = VGroup(T("s1.roll, s1.marks   (dot operator)", size=24, color=th.AMBER), T('strcpy(s2.name, "Deepa");  (not =)', size=24, color=th.CORAL), T("struct student cls[3];  array of structures", size=24, color=th.SKY)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        acc.scale_to_fit_width(min(acc.width, 5.6)).move_to([4.0, 1.0, 0])
        with self.say("A structure is a user defined type that bundles several variables, of different types, under one name: a student's roll, name, faculty and marks. The definition is only a template; memory is used when you declare a variable. Every member gets its own space, so the size is the sum: forty bytes."):
            self.play(FadeIn(h))
            C.type_code(self, cd, per_line=0.3)
            self.play(LaggedStart(*[GrowFromEdge(m_, LEFT) for m_ in mem], lag_ratio=0.25))
            self.play(FadeIn(tot))
        with self.say("Reach a member with a dot. Strings must be copied with strcpy, not the equals sign. And an array of structures holds a whole class list."):
            self.play(LaggedStart(*[FadeIn(a_) for a_ in acc], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, cd, mem, tot, acc)))
        h = C.head(self, "A union overlays its members in one space")
        un = C.code(["union value { int i; float f; char s[8]; };"], lang="c", size=26).move_to([0, 2.0, 0])
        box = Rectangle(width=8 * 0.6, height=0.8, stroke_color=th.CORAL, stroke_width=3).move_to([0, 0.6, 0])
        bars = VGroup(Rectangle(width=4 * 0.6, height=0.8, stroke_width=0, fill_color=th.SKY, fill_opacity=0.5).align_to(box, LEFT).set_y(0.6), Rectangle(width=4 * 0.6, height=0.8, stroke_width=0, fill_color=th.MINT, fill_opacity=0.5).align_to(box, LEFT).set_y(0.6),
                      Rectangle(width=8 * 0.6, height=0.8, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.35).align_to(box, LEFT).set_y(0.6))
        bl = VGroup(T("int i", size=22, color=th.SKY).move_to(bars[0]), T("float f", size=22, color=th.MINT).move_to(bars[0]), T("char s[8]", size=22, color=th.AMBER).next_to(bars[0], RIGHT, buff=0.3))
        sz = T("sizeof = size of the LARGEST member = 8 bytes", size=26, color=th.CORAL).move_to([0, -0.4, 0])
        demo = C.output(["v.i = 65;     v.i → 65", "v.f = 3.14;   v.f → 3.14,  v.i → 1078523331 (corrupted)"], size=22).move_to([0, -1.8, 0])
        with self.say("A union looks like a structure, but all its members share the same memory. Its size is the size of its largest member: eight bytes here. Only one member is valid at a time."):
            self.play(FadeIn(h), FadeIn(un), Create(box))
            for b_, l_ in zip(bars, bl):
                self.play(FadeIn(b_), FadeIn(l_), run_time=0.6)
            self.play(FadeIn(sz))
        with self.say("Store sixty five in i, and i reads sixty five. Store three point one four in f, and now i reads a huge meaningless number: the float's bits read as an integer. Writing one member destroys the others. Unions save memory when you need only one field at a time."):
            self.play(FadeIn(demo))
        self.play(FadeOut(VGroup(h, un, box, bars, bl, sz, demo)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = C.head(self, "A pointer stores an address")
        n_ = cell(25, th.SKY, w=1.6, h=1.0, size=36).move_to([-3.0, 0.6, 0])
        p_ = cell("0x7ffc…26bc", th.MINT, w=3.0, h=1.0, size=24).move_to([3.0, 0.6, 0])
        nl = VGroup(T("n", size=30, color=th.SKY, weight="BOLD").next_to(n_, UP, buff=0.15), T("address 0x7ffc…26bc", size=20, color=th.MUTED).next_to(n_, DOWN, buff=0.15))
        pl = VGroup(T("p", size=30, color=th.MINT, weight="BOLD").next_to(p_, UP, buff=0.15), T("int *p;  p = &n;", size=22, color=th.MINT, font=C.MONO).next_to(p_, DOWN, buff=0.15))
        arr = CurvedArrow(p_.get_left(), n_.get_right(), angle=0.4, color=th.MINT)
        ops = VGroup(T("&n → the address of n", size=26, color=th.AMBER, font=C.MONO), T("*p → the value at that address (25)", size=26, color=th.AMBER, font=C.MONO), T("*p = *p + 5;   changes n to 30", size=26, color=th.CORAL, font=C.MONO)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -2.0, 0])
        with self.say("Every variable lives at an address in memory. A pointer is a variable that stores such an address. Declare p as a pointer to an int, and set it to ampersand n, the address of n. Now p points at n."):
            self.play(FadeIn(h), FadeIn(n_), FadeIn(nl))
            self.play(FadeIn(p_), FadeIn(pl))
            self.play(Create(arr))
        with self.say("Two operators. Ampersand gives an address. Star, the indirection operator, follows the pointer to the value there: star p is twenty five. And star p equals star p plus five changes n itself, through the pointer."):
            self.play(FadeIn(ops[0]))
            self.play(FadeIn(ops[1]))
            n2 = cell(30, th.CORAL, w=1.6, h=1.0, size=36).move_to(n_)
            self.play(FadeIn(ops[2]), Transform(n_, n2))
        self.play(FadeOut(VGroup(h, n_, nl, p_, pl, arr, ops)))
        h = C.head(self, "Call by value vs call by reference")
        xv, yv = cell(10, th.SKY).move_to([-4.6, 1.2, 0]), cell(20, th.SKY).move_to([-3.0, 1.2, 0])
        av, bv = cell(10, th.MUTED).move_to([-4.6, -0.8, 0]), cell(20, th.MUTED).move_to([-3.0, -0.8, 0])
        lv = VGroup(T("main: x, y", size=22, color=th.SKY).next_to(VGroup(xv, yv), UP, buff=0.15), T("swap(x, y): copies a, b", size=22, color=th.MUTED).next_to(VGroup(av, bv), DOWN, buff=0.15))
        xr, yr = cell(10, th.MINT).move_to([2.2, 1.2, 0]), cell(20, th.MINT).move_to([3.8, 1.2, 0])
        ar_, br_ = cell("&x", th.MUTED).move_to([2.2, -0.8, 0]), cell("&y", th.MUTED).move_to([3.8, -0.8, 0])
        lr = VGroup(T("main: x, y", size=22, color=th.MINT).next_to(VGroup(xr, yr), UP, buff=0.15), T("swap(&x, &y): addresses", size=22, color=th.MUTED).next_to(VGroup(ar_, br_), DOWN, buff=0.15))
        ptrs = VGroup(Arrow(ar_.get_top(), xr.get_bottom(), buff=0.05, color=th.MINT, stroke_width=4), Arrow(br_.get_top(), yr.get_bottom(), buff=0.05, color=th.MINT, stroke_width=4))
        fix = C.code(["void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }"], lang="c", size=24).move_to([0, -2.8, 0])
        with self.say("Back to the cold open. In call by value, swap receives copies. It swaps the copies, and x and y in main never change."):
            self.play(FadeIn(h), FadeIn(xv), FadeIn(yv), FadeIn(lv[0]))
            self.play(TransformFromCopy(xv, av), TransformFromCopy(yv, bv), FadeIn(lv[1]))
            self.play(av.animate.move_to(bv.get_center()), bv.animate.move_to(av.get_center()), path_arc=PI / 2, run_time=1.0)
            self.play(Indicate(VGroup(xv, yv), color=th.CORAL))
        with self.say("In call by reference, swap receives the addresses, and works through them on the originals. Now x and y really are swapped. That is also how a function can return several results at once."):
            self.play(FadeIn(xr), FadeIn(yr), FadeIn(lr[0]), FadeIn(ar_), FadeIn(br_), FadeIn(lr[1]), GrowArrow(ptrs[0]), GrowArrow(ptrs[1]))
            self.play(xr[1].animate.move_to(yr[0].get_center()), yr[1].animate.move_to(xr[0].get_center()), path_arc=PI / 2, run_time=1.0)
            self.play(FadeIn(fix))
        self.play(FadeOut(VGroup(h, xv, yv, av, bv, lv, xr, yr, ar_, br_, lr, ptrs, fix)))
        arrp = C.code(["int arr[5] = {10, 20, 30, 40, 50};", "int *q = arr;        /* the array name is &arr[0] */", 'printf("%d %d", arr[2], *(q + 2));   /* 30 30 */'], lang="c", size=24).move_to([0, 0.6, 0])
        cells = VGroup(*[cell(v, th.SKY, w=1.1, h=0.7, size=24) for v in (10, 20, 30, 40, 50)]).arrange(RIGHT, buff=0).move_to([0, -1.6, 0])
        qa = Arrow(cells[0].get_bottom() + DOWN * 0.8, cells[0].get_bottom(), buff=0.05, color=th.MINT)
        ql = T("q", size=26, color=th.MINT, font=C.MONO).next_to(qa, DOWN, buff=0.05)
        with self.say("Pointers and arrays are close relatives. An array's name is the address of its first element. Add two to the pointer and it moves two elements along, so star of q plus two is arr two: thirty."):
            self.play(FadeIn(arrp), FadeIn(cells), GrowArrow(qa), FadeIn(ql))
            self.play(VGroup(qa, ql).animate.shift(RIGHT * 2.2), run_time=1.0)
            self.play(Indicate(cells[2], color=th.MINT))
        self.play(FadeOut(VGroup(arrp, cells, qa, ql)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = C.head(self, "A file survives after the program ends")
        steps = VGroup(*[C.code([t_], lang="c", size=24) for t_ in ["FILE *fp;", 'fp = fopen("student.txt", "w");', 'if (fp == NULL) { printf("Cannot open"); return 1; }', 'fprintf(fp, "%d %s %.1f\\n", 1, "Anisha", 78.5);', "fclose(fp);"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.14).scale_to_fit_width(min(steps.width, 12.4))
        steps.scale_to_fit_height(min(steps.height, 3.7)).move_to([0, 0, 0]).align_to(np.array([0, 2.45, 0]), UP)
        modes = C.table([["mode", '"r"', '"w"', '"a"', '"rb" "wb"'], ["meaning", "read", "write (erases!)", "append", "binary"]], [1.9, 1.5, 2.6, 1.6, 1.9], row_h=0.55, size=24, colors=[th.AMBER, th.INK, th.CORAL, th.INK, th.INK]).move_to([0, -2.35, 0])
        with self.say("Variables vanish when the program ends; a data file on disk survives. Every file program follows the same life: declare a file pointer, open the file with a mode, check it opened, read or write, and close it. The mode matters: w creates the file and erases anything already there, a appends to the end, r reads."):
            self.play(FadeIn(h))
            for s_ in steps:
                self.play(FadeIn(s_, shift=DOWN * 0.15), run_time=0.6)
            C.reveal_table(self, modes, 2.5)
        self.play(FadeOut(VGroup(h, steps, modes)))
        rows = [["function", "does"], ["putc / getc", "one character (getc returns EOF at the end)"], ["putw / getw", "one integer, in binary"], ["fprintf / fscanf", "formatted write / read, like printf / scanf"], ["fwrite / fread", "whole records (e.g. structures)"], ["fseek / ftell / rewind", "move / report / reset the file position"]]
        tb = C.table(rows, [4.2, 7.6], row_h=0.62, size=25, colors=[th.SKY, th.INK]).move_to([0, 0.4, 0])
        with self.say("The file functions. Get c and put c handle one character; get w and put w one integer; f printf and f scanf work like printf and scanf, but with a file. F write and f read move whole structures. And f seek, f tell and rewind move around the file.") as v:
            C.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        h = C.head(self, "Sequential vs random access: fseek")
        cells = VGroup(*[VGroup(Rectangle(width=1.8, height=0.9, stroke_color=th.SKY, stroke_width=3, fill_color=th.PANEL, fill_opacity=1), Text(str(11 * (k + 1)), font=C.MONO, font_size=30, color=th.INK)) for k in range(5)]).arrange(RIGHT, buff=0).move_to([0, 0.8, 0])
        for c_ in cells:
            c_[1].move_to(c_[0])
        offs = VGroup(*[T(f"{4 * k}–{4 * k + 3}", size=20, color=th.MUTED).next_to(cells[k], DOWN, buff=0.12) for k in range(5)])
        ptr = Arrow(cells[0].get_top() + UP * 0.8, cells[0].get_top(), buff=0.05, color=th.MINT)
        cd = C.code(["fseek(fp, 2 * sizeof(int), SEEK_SET);   /* byte 8 */", 'printf("%d %ld", getw(fp), ftell(fp));  /* 33 12 */'], lang="c", size=24).move_to([0, -1.9, 0])
        rule = T("offset = record number × record size", size=26, color=th.AMBER).move_to([0, -3.0, 0])
        with self.say("Five integers written with put w, four bytes each: twenty bytes. Sequential access reads them in order from the start. Random access jumps: f seek to two times the size of an int, byte eight, lands on the third number, thirty three. After reading four bytes, f tell reports position twelve. The whole idea: offset equals record number times record size."):
            self.play(FadeIn(h), FadeIn(cells), FadeIn(offs), GrowArrow(ptr))
            self.play(ptr.animate.shift(RIGHT * 1.8), run_time=0.5)
            self.play(ptr.animate.shift(RIGHT * 1.8), run_time=0.5)
            self.play(Indicate(cells[2], color=th.MINT), FadeIn(cd))
            self.play(ptr.animate.shift(RIGHT * 1.8), FadeIn(rule))
        self.play(FadeOut(VGroup(h, cells, offs, ptr, cd, rule)))
        self.quiz("A function receives int *a and changes *a. This is",
                  ["call by value", "call by reference", "recursion", "a union"], 1,
                  "Pause and think.",
                  "Call by reference: the function received an address and changed the original through it.")
        self.quiz("The size of union { int i; float f; char s[8]; } is",
                  ["16 bytes", "8 bytes", "4 bytes", "12 bytes"], 1,
                  "One more.",
                  "Eight bytes: a union is as big as its largest member. A structure with the same members would add them up.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Functions: prototype, call, definition; return sends back one value.",
            "Storage classes: auto (stack, garbage), extern and static (0, whole run), register.",
            "Recursion needs a base case; calls stack up, then unwind.",
            "struct: separate memory, size = sum; union: shared memory, size = largest member.",
            "Pointers: &n address, *p value; call by reference changes the original; files: open, check, read/write, close; fseek offsets.",
        ], "Quick recap. Functions with prototypes, calls and definitions. Storage classes. Recursion with its base case. Structures and unions. Pointers and call by reference. And data files, with random access by f seek.")
        self.outro("That was programming in C. Next, object-oriented programming: classes, objects, inheritance and polymorphism. See you there.")
