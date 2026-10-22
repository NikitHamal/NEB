import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _cs as C  # noqa: E402


class Lesson(Lesson):
    SUBJECT = "cs"
    GRADE = 12
    UNIT = 6
    TITLE = "Software Process Model"
    SUBTITLE = "How real software is planned, built and kept alive"
    SECTIONS = ["Software projects and the process", "The SDLC", "Analysts, requirements and design", "Data flow diagrams", "Software quality", "Development models"]
    NEXT = "Unit 7 · Recent Trends in Technology"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        ax = Axes(x_range=[-0.5, 4.5, 1], y_range=[0, 110, 20], x_length=7.8, y_length=4.4, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2, "include_numbers": False}).move_to([-2.5, -0.6, 0])
        names = ["requirement", "design", "coding", "testing", "maintenance"]
        vals = [1, 5, 10, 20, 100]
        cols = [th.MINT, th.MINT, th.SKY, th.AMBER, th.CORAL]
        bars = VGroup(*[Rectangle(width=1.0, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.03), stroke_width=0, fill_color=c_, fill_opacity=0.85).move_to(ax.c2p(k, 0), aligned_edge=DOWN) for k, (v, c_) in enumerate(zip(vals, cols))])
        lab = VGroup(*[T(n_, size=22, color=th.MUTED).next_to(ax.c2p(k, 0), DOWN, buff=0.2) for k, n_ in enumerate(names)])
        vl = VGroup(*[T(f"×{v}", size=26, color=c_, weight="BOLD").next_to(b_, UP, buff=0.1) for v, c_, b_ in zip(vals, cols, bars)])
        q = para("A school's fee software forgets the sibling discount. Fixing it at the requirement stage costs Rs 2 000. Found after going live: Rs 2 00 000.", width=4.2, size=26, color=th.INK).move_to([4.5, 0.4, 0])
        with self.say("A school orders fee software, and nobody notices that it ignores the sibling discount. Fixed while the requirements are being written, the mistake costs about two thousand rupees. Found in testing, twenty times that. Found after the bills have gone out, a hundred times: two lakh rupees."):
            self.play(Create(ax), FadeIn(lab))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.25), LaggedStart(*[FadeIn(v_) for v_ in vl], lag_ratio=0.25), run_time=2.5)
            self.play(FadeIn(q))
        with self.say("The earlier a mistake is caught, the cheaper it is. That one fact explains why software is built through careful processes and models. This unit is about them."):
            nb = C.neby_in(self, "think", height=1.3)
        C.neby_out(self, nb)
        self.play(FadeOut(VGroup(ax, bars, lab, vl, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Computer Science, Unit 6: Software Process Model."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Software projects and the development process. The SDLC, phase by phase. Analysts, requirements and design. Data flow diagrams. Software quality. And the development models: waterfall, prototype, incremental, spiral and agile.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = C.head(self, "Four constraints: change one, the others move")
        tri = Polygon([-3.6, 1.6, 0], [-6.0, -2.0, 0], [-1.2, -2.0, 0], stroke_color=th.SKY, stroke_width=4, fill_color=th.SKY, fill_opacity=0.08)
        labs = VGroup(T("scope", size=28, color=th.SKY, weight="BOLD").next_to(tri.get_vertices()[0], UP, buff=0.15), T("time", size=28, color=th.AMBER, weight="BOLD").next_to(tri.get_vertices()[1], DOWN, buff=0.15), T("cost", size=28, color=th.PINK, weight="BOLD").next_to(tri.get_vertices()[2], DOWN, buff=0.15),
                      T("quality", size=28, color=th.MINT, weight="BOLD").move_to([-3.6, -0.6, 0]))
        txt = para("A software project is a temporary, planned effort with a goal, budget, deadline and team. The manager plans tasks, estimates effort in person-months, tracks milestones and manages risk.", width=5.6, size=24, color=th.BODY).move_to([3.4, 0.4, 0])
        with self.say("Software is programs plus data plus documentation. A software project is a temporary, planned effort with a fixed goal, a budget, a deadline and a team. It is managed along four constraints: scope, time, cost and quality. Pull on one and the others move: add features, and it costs more or takes longer."):
            self.play(FadeIn(h), Create(tri), FadeIn(labs))
            self.play(FadeIn(txt))
        self.play(FadeOut(VGroup(h, tri, labs, txt)))
        C.worked(self, "8 developers for 5 months at Rs 60 000 a month, plus Rs 3 00 000 of hardware and licences, plus 20 % overhead. Find the effort and the cost.",
                 [r"\text{effort} = 8 \times 5 = 40 \text{ person-months}", r"\text{staff} = 40 \times 60\,000 = \text{Rs } 24\,00\,000;\quad \text{direct} = 27\,00\,000", r"\text{overhead} = 0.2 \times 27\,00\,000 = 5\,40\,000 \Rightarrow \text{total Rs } 32\,40\,000",
                  r"40 \text{ people for 1 month? No: } \tfrac{n(n-1)}{2} = 780 \text{ communication paths}"],
                 ["Estimating a project.", "Eight developers for five months is forty person months.", "Forty person months at sixty thousand is twenty four lakh; with hardware, twenty seven lakh.", "Add twenty per cent overhead: thirty two lakh forty thousand.",
                  "And effort is not time: forty people for one month would not work, because they would have seven hundred and eighty lines of communication between them."])
        h = C.head(self, "Four activities in every process")
        acts = VGroup(*[C.node(t_, c_, w=2.8, h=1.15, size=24) for t_, c_ in [("specification", th.SKY), ("design and\nimplementation", th.AMBER), ("validation", th.MINT), ("evolution", th.PINK)]]).arrange(RIGHT, buff=0.4).move_to([0, 0.6, 0])
        ar = VGroup(*[Arrow(acts[k].get_right(), acts[k + 1].get_left(), buff=0.03, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.35) for k in range(3)])
        nt = para("process = the activities;  SDLC = the standard list of phases;  process model = one particular arrangement of those phases in time.", width=11.5, size=24, color=th.AMBER).move_to([0, -1.6, 0])
        with self.say("A software development process turns a customer's need into working software. Every process has four activities: specify what it must do, design and build it, validate that it does what was wanted, and evolve it as needs change. A process model arranges those activities in time. Do not mix the three terms up in the exam."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(a_) for a_ in acts], lag_ratio=0.2), LaggedStart(*[GrowArrow(a_) for a_ in ar], lag_ratio=0.2))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, acts, ar, nt)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = C.head(self, "The SDLC: eight phases in a cycle")
        names = ["preliminary\ninvestigation", "feasibility\nstudy", "system\nanalysis", "system\ndesign", "coding", "testing", "implementation", "maintenance"]
        cols = [th.SKY, th.SKY, th.MINT, th.MINT, th.AMBER, th.AMBER, th.PINK, th.CORAL]
        pos = [(-4.8, 1.5), (-1.6, 1.5), (1.6, 1.5), (4.8, 1.5), (4.8, -0.5), (1.6, -0.5), (-1.6, -0.5), (-4.8, -0.5)]
        nodes = VGroup(*[C.node(n_, c_, w=2.5, h=1.0, size=22).move_to([x, y, 0]) for n_, c_, (x, y) in zip(names, cols, pos)])

        def link(a, b):
            if abs(a.get_y() - b.get_y()) < 0.1:
                p, q = (a.get_right(), b.get_left()) if b.get_x() > a.get_x() else (a.get_left(), b.get_right())
            else:
                p, q = (a.get_bottom(), b.get_top()) if b.get_y() < a.get_y() else (a.get_top(), b.get_bottom())
            return Arrow(p, q, buff=0.06, color=th.MUTED, stroke_width=4, max_tip_length_to_length_ratio=0.3)

        arcs = VGroup(*[link(nodes[k], nodes[(k + 1) % 8]) for k in range(8)])
        mem = T("Please Finish All Design Code Testing Installation Maintenance", size=26, color=th.AMBER).move_to([0, -1.75, 0])
        maint = para("maintenance is the longest, costliest phase: 60–70 % of lifetime cost. Corrective, adaptive, perfective, preventive.", width=11.5, size=24, color=th.CORAL).move_to([0, -2.65, 0])
        with self.say("The system development life cycle is the sequence of phases every system passes through, each producing a deliverable for the next. Preliminary investigation defines the problem. A feasibility study asks whether it is technically, economically, operationally and legally possible. Analysis gathers the requirements. Design decides how. Then coding, testing, implementation with training, and maintenance, which feeds back into the cycle."):
            self.play(FadeIn(h))
            for k in range(8):
                self.play(FadeIn(nodes[k], scale=1.1), Create(arcs[k]), run_time=0.45)
            self.play(FadeIn(mem))
        with self.say("Maintenance lasts longest and costs most, sixty to seventy per cent of a system's lifetime cost: fixing defects, adapting to change, adding features, and restructuring to make future change cheaper."):
            self.play(FadeIn(maint), Indicate(nodes[7], color=th.CORAL))
        self.play(FadeOut(VGroup(h, nodes, arcs, mem, maint)))
        rows = [["feasibility", "question"], ["technical", "do we have the technology and skills?"], ["economic", "do the benefits exceed the costs?"], ["operational", "will the staff actually use it?"], ["schedule / legal", "in time, and lawful (e.g. Electronic Transactions Act)?"]]
        tb = C.table(rows, [3.4, 8.2], row_h=0.66, size=26, colors=[th.AMBER, th.INK]).move_to([0, 0.4, 0])
        with self.say("The four kinds of feasibility are worth memorising: technical, economic, operational, and schedule or legal.") as v:
            C.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = C.head(self, "System analyst vs software engineer")
        an = VGroup(C.node("system analyst", th.SKY, w=3.4, h=0.9, size=26), C.bullets(["faces the customer and the problem", "asks WHAT the system must do", "interviews, SRS, DFDs, feasibility"], width=5.0, size=24, color=th.BODY)).arrange(DOWN, buff=0.35).move_to([-3.4, 0.0, 0])
        en = VGroup(C.node("software engineer", th.MINT, w=3.6, h=0.9, size=26), C.bullets(["faces the machine and the solution", "asks HOW the system will do it", "design, code, tests, builds"], width=5.0, size=24, color=th.BODY)).arrange(DOWN, buff=0.35).move_to([3.4, 0.0, 0])
        srs = T("the SRS is the contract between them", size=24, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("Two roles look in opposite directions. The system analyst faces the customer: studies the business problem and defines what the system must do. The software engineer faces the machine: designs, builds and tests the software that does it. The requirement specification is the contract between them."):
            self.play(FadeIn(h), FadeIn(an), FadeIn(en))
            self.play(FadeIn(srs))
        self.play(FadeOut(VGroup(h, an, en, srs)))
        rows = [["method", "strength", "weakness"], ["interview", "deep, follow-up questions", "slow, one person at a time"], ["questionnaire", "cheap, reaches many", "no follow-up, low response"], ["observation", "what people really do", "people act differently when watched"],
                ["document review", "real data and volumes", "may be out of date"], ["prototyping", "users react to a screen", "may mistake it for the product"]]
        tb = C.table(rows, [3.0, 4.6, 5.0], row_h=0.6, size=24, colors=[th.AMBER, th.MINT, th.CORAL]).move_to([0, 0.6, 0])
        good = VGroup(T("bad requirement: “the system should be fast”", size=24, color=th.CORAL), T("good: “a fee receipt shall print within 5 seconds”", size=24, color=th.MINT)).arrange(DOWN, buff=0.2).move_to([0, -2.4, 0])
        with self.say("How are requirements collected? Interviews go deep but are slow. Questionnaires reach many people cheaply. Observation shows what people really do. Documents show the real data. And prototypes let users react to a screen, which they are much better at than describing what they want. The results go into the SRS, where every requirement must be testable: the system should be fast is useless; a receipt shall print within five seconds can be checked.") as v:
            C.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(good))
        self.play(FadeOut(VGroup(tb, good)))
        h = C.head(self, "Design: logical and physical")
        cols = VGroup(VGroup(T("logical design", size=28, color=th.SKY, weight="BOLD"), para("WHAT, independent of any machine: DFDs, ER diagrams, data dictionary, decision tables", width=5.0, size=22, color=th.BODY)).arrange(DOWN, buff=0.2),
                      VGroup(T("physical design", size=28, color=th.MINT, weight="BOLD"), para("HOW it will be built: tables and indexes, file formats, screens and reports, modules, hardware", width=5.0, size=22, color=th.BODY)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=1.0).move_to([0, 0.8, 0])
        cc = VGroup(VGroup(T("cohesion", size=26, color=th.AMBER, weight="BOLD"), T("each module does ONE job → HIGH is good", size=22, color=th.BODY)).arrange(DOWN, buff=0.1), VGroup(T("coupling", size=26, color=th.AMBER, weight="BOLD"), T("modules depend on each other → LOW is good", size=22, color=th.BODY)).arrange(DOWN, buff=0.1)).arrange(RIGHT, buff=1.0)
        cc.scale_to_fit_width(min(cc.width, 12.4)).move_to([0, -1.6, 0])
        with self.say("Design turns the requirements into a blueprint. Logical design says what the system does, with diagrams that ignore the machine. Physical design says how: tables, files, screens and modules. Two words judge a design: high cohesion, each module doing one job, and low coupling, modules depending on each other as little as possible."):
            self.play(FadeIn(h), FadeIn(cols))
            self.play(FadeIn(cc))
        self.play(FadeOut(VGroup(h, cols, cc)))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = C.head(self, "DFD symbols")

        def ent(t_, p_):
            return VGroup(Rectangle(width=2.6, height=0.95, stroke_color=th.SKY, stroke_width=3, fill_color=th.PANEL, fill_opacity=1), T(t_, size=24, color=th.SKY)).move_to(p_)

        def proc(n_, t_, p_):
            c = Circle(radius=0.9, stroke_color=th.AMBER, stroke_width=3, fill_color=th.PANEL, fill_opacity=1).move_to(p_)
            return VGroup(c, VGroup(T(n_, size=20, color=th.MUTED), T(t_, size=22, color=th.AMBER)).arrange(DOWN, buff=0.05).move_to(c))

        def store(d_, t_, p_):
            g = VGroup(Line([-1.4, 0.35, 0], [1.4, 0.35, 0], color=th.MINT, stroke_width=3), Line([-1.4, -0.35, 0], [1.4, -0.35, 0], color=th.MINT, stroke_width=3), Line([-1.4, 0.35, 0], [-1.4, -0.35, 0], color=th.MINT, stroke_width=3),
                       T(f"{d_}  {t_}", size=22, color=th.MINT))
            return g.move_to(p_)

        syms = VGroup(VGroup(proc("", "process", [0, 0, 0]), T("process: verb + object", size=22, color=th.INK)).arrange(DOWN, buff=0.2), VGroup(ent("entity", [0, 0, 0]), T("external entity: a noun", size=22, color=th.INK)).arrange(DOWN, buff=0.2),
                      VGroup(store("D1", "file", [0, 0, 0]), T("data store", size=22, color=th.INK)).arrange(DOWN, buff=0.2), VGroup(Arrow(LEFT, RIGHT, color=th.INK), T("data flow: a noun", size=22, color=th.INK)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=0.6).move_to([0, 0.5, 0])
        syms.scale_to_fit_width(min(syms.width, 12.6))
        nt = para("A DFD shows how DATA moves — never control flow, never timing, never a decision diamond.", width=11, size=24, color=th.AMBER).move_to([0, -2.2, 0])
        with self.say("A data flow diagram shows how data moves through a system. Four symbols. A circle is a process that transforms data, named with a verb. A rectangle is an external entity outside the system. An open box is a data store, a file or table. And an arrow is a flow of data, labelled with a noun. It never shows control flow, timing or decisions: that would be a flowchart."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(s_) for s_ in syms], lag_ratio=0.3))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, syms, nt)))
        h = C.head(self, "Level-1 DFD: result processing")
        e1, e2 = ent("Subject teacher", [-5.2, 1.7, 0]), ent("Student", [4.8, 1.7, 0])
        p1, p2, p3 = proc("1.0", "Record\nmarks", [-1.6, 1.7, 0]), proc("2.0", "Compute\nresult", [1.6, -0.5, 0]), proc("3.0", "Print\nmark-sheet", [4.8, -0.5, 0])
        d1, d2 = store("D1", "Marks file", [-1.6, -0.5, 0]), store("D2", "Student file", [1.6, -2.6, 0])

        def flow(a, b, t_, side=UP):
            ar = Arrow(a, b, buff=0.08, color=th.INK, stroke_width=3, max_tip_length_to_length_ratio=0.12)
            return VGroup(ar, T(t_, size=22, color=th.MUTED).next_to(ar.get_center(), side, buff=0.1))

        fl = VGroup(flow(e1.get_right(), p1[0].get_left(), "subject marks"), flow(p1[0].get_bottom(), d1.get_top(), "validated marks", RIGHT), flow(d1.get_right(), p2[0].get_left(), "marks"), flow(d2.get_top(), p2[0].get_bottom(), "student record", RIGHT),
                    flow(p2[0].get_right(), p3[0].get_left(), "grade, GPA"), flow(p3[0].get_top(), e2.get_bottom(), "mark-sheet", RIGHT))
        with self.say("A level one diagram for result processing. The subject teacher sends marks to process one, record marks, which stores them in the marks file. Process two computes the result from the marks and the student file, and process three prints the mark sheet for the student. Each process is numbered, each arrow names its data. And data never jumps from one store to another, or from an entity to a store, without passing through a process."):
            self.play(FadeIn(h), FadeIn(VGroup(e1, e2)), FadeIn(VGroup(p1, p2, p3)), FadeIn(VGroup(d1, d2)))
            for f_ in fl:
                self.play(GrowArrow(f_[0]), FadeIn(f_[1]), run_time=0.55)
        self.play(FadeOut(VGroup(h, e1, e2, p1, p2, p3, d1, d2, fl)))
        h = C.head(self, "From an ER diagram to tables")
        rules = C.bullets(["each entity → a table; its key → the primary key", "1 : M relationship → put the '1' side's key into the 'M' table as a foreign key", "M : N relationship → a NEW table whose key is the pair of foreign keys"], width=11.5, size=26).move_to([0, 1.0, 0])
        tbs = VGroup(C.dbtable("STUDENT", ["roll_no", "name"], [["1", "Sita Rai"]], widths=[1.6, 2.2], size=22, pk=("roll_no",)), C.dbtable("COURSE", ["course_id", "title"], [["CS12", "Computer Sci."]], widths=[1.8, 2.4], size=22, pk=("course_id",)),
                     C.dbtable("ENROLS", ["roll_no", "course_id", "grade"], [["1", "CS12", "A"]], widths=[1.6, 1.8, 1.2], size=22, fk=("roll_no", "course_id"))).arrange(RIGHT, buff=0.5).move_to([0, -1.6, 0])
        with self.say("Database design converts the ER diagram into tables with three rules. Every entity becomes a table. A one to many relationship puts the key of the one side into the many table as a foreign key. And a many to many relationship becomes a new table, keyed by the pair of foreign keys: student enrols in course."):
            self.play(FadeIn(h))
            C.reveal_list(self, rules, 3.0)
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tbs], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, rules, tbs)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        rows = [["ISO/IEC 25010 characteristic", "question"], ["functional suitability", "does it do the required jobs correctly?"], ["performance efficiency", "fast enough, economical?"], ["usability", "can users learn and operate it?"], ["reliability", "keeps working, recovers after failure?"],
                ["security", "data protected?"], ["maintainability", "cheap to correct and improve?"], ["portability", "can it move to new environments?"]]
        tb = C.table(rows, [5.2, 6.6], row_h=0.56, size=24, colors=[th.MINT, th.INK]).move_to([0, 0.6, 0])
        nt = T("quality = conformance to requirements, standards and professional expectations (Pressman)", size=22, color=th.AMBER).move_to([0, -2.4, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Software quality is not just no bugs. It is conformance to the requirements, to development standards, and to what any professional would expect. The international standard ISO twenty five oh ten lists characteristics such as functional suitability, performance, usability, reliability, security, maintainability and portability.") as v:
            C.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h = C.head(self, "QA vs QC; verification vs validation")
        g = VGroup(*[VGroup(T(t_, size=28, color=c_, weight="BOLD"), para(d_, width=5.2, size=24, color=th.BODY)).arrange(DOWN, buff=0.12) for t_, d_, c_ in [("quality assurance", "process-oriented, prevents: reviews, standards, audits", th.SKY), ("quality control", "product-oriented, detects: testing", th.MINT),
                     ("verification", "are we building the product RIGHT?", th.AMBER), ("validation", "are we building the RIGHT product?", th.PINK)]]).arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.9)).move_to([0, 0.2, 0])
        with self.say("Quality is built in two ways. Quality assurance improves the process to prevent defects: standards, reviews and audits. Quality control tests the product to detect them. Similarly, verification asks: are we building the product right? Validation asks: are we building the right product?"):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(x_) for x_ in g], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, g)))
        C.worked(self, "A server fails every 400 hours on average and takes 5 hours to repair. 92 defects were found before delivery, 8 after. Find availability and defect removal efficiency.",
                 [r"\text{availability} = \frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}} = \frac{400}{405} = 98.77\%", r"\text{DRE} = \frac{E}{E + D} = \frac{92}{100} = 92\%", r"98.77\% \approx 4.5 \text{ days of downtime a year: too much for a payment system}"],
                 ["Two quality numbers.", "Availability is the mean time between failures over that plus the mean time to repair: ninety eight point seven seven per cent.", "Defect removal efficiency: ninety two of the hundred defects were caught before delivery.", "It sounds high, but it is four and a half days of downtime a year."])

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = C.head(self, "Waterfall: once, in order, like steps")
        names = ["requirements", "design", "coding", "testing", "deployment", "maintenance"]
        steps = VGroup(*[C.node(n_, th.SKY, w=2.6, h=0.7, size=22).move_to([-5.0 + 1.6 * k, 1.75 - 0.82 * k, 0]) for k, n_ in enumerate(names)])
        ar = VGroup(*[CurvedArrow(steps[k].get_right(), steps[k + 1].get_top(), angle=-PI / 2, color=th.MUTED, stroke_width=3) for k in range(5)])
        pc = VGroup(T("+ simple, documented, easy to manage", size=24, color=th.MINT), T("− working software only at the end", size=24, color=th.CORAL), T("− can't cope with changing requirements", size=24, color=th.CORAL), T("fits: fixed, legal, tender-based specs", size=24, color=th.AMBER)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        pc.scale_to_fit_width(min(pc.width, 5.6)).move_to([3.9, 1.1, 0])
        with self.say("The development models. Waterfall, the oldest, runs the phases once, strictly in order, each signed off before the next, like water falling down steps. It is simple, well documented and easy to manage. But the customer sees nothing until the end, and a changed requirement is very expensive. It suits short projects with a fixed specification, like a system defined by a law."):
            self.play(FadeIn(h))
            for k in range(6):
                self.play(FadeIn(steps[k]), *([Create(ar[k - 1])] if k else []), run_time=0.45)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pc], lag_ratio=0.25))
        self.play(FadeOut(VGroup(h, steps, ar, pc)))
        h = C.head(self, "Prototype and incremental")
        loop = VGroup(*[C.node(t_, th.MINT, w=2.3, h=0.7, size=22).move_to([-3.3 + 2.4 * np.cos(PI / 2 - TAU * k / 5), -0.2 + 1.8 * np.sin(PI / 2 - TAU * k / 5), 0]) for k, t_ in enumerate(["gather needs", "quick design", "build prototype", "user evaluates", "refine"])])
        la = VGroup(*[Arrow(loop[k].get_center(), loop[(k + 1) % 5].get_center(), buff=0.55, color=th.MUTED, stroke_width=3) for k in range(5)])
        pl = T("prototype: users criticise a screen", size=24, color=th.MINT).move_to([-3.3, -2.7, 0])
        inc = VGroup(*[Rectangle(width=0.9 * (k + 1), height=0.55, stroke_color=th.SKY, stroke_width=2, fill_color=th.SKY, fill_opacity=0.25 + 0.15 * k) for k in range(4)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([2.6, 0.0, 0])
        il = VGroup(*[T(t_, size=22, color=th.INK).next_to(inc[k], RIGHT, buff=0.15) for k, t_ in enumerate(["core", "+ fees", "+ attendance", "+ results"])])
        il2 = para("incremental: usable software after the first increment", width=5.4, size=24, color=th.SKY).move_to([3.6, -2.6, 0])
        with self.say("The prototype model builds a quick, rough version, lets the user try it, and refines it, round and round, until the requirements are clear. The incremental model delivers the system in slices: a working core first, then fees, then attendance, then results, so the customer has something useful after a few weeks."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(l_) for l_ in loop], lag_ratio=0.15), LaggedStart(*[GrowArrow(a_) for a_ in la], lag_ratio=0.15), FadeIn(pl))
            self.play(LaggedStart(*[GrowFromEdge(i_, LEFT) for i_ in inc], lag_ratio=0.3), FadeIn(il), FadeIn(il2))
        self.play(FadeOut(VGroup(h, loop, la, pl, inc, il, il2)))
        h = C.head(self, "Spiral: risk-driven loops")
        c0 = np.array([-3.0, -0.4, 0])
        sp = ParametricFunction(lambda t: c0 + (0.15 + 0.09 * t) * np.array([np.cos(PI / 2 + t), np.sin(PI / 2 + t), 0]), t_range=[0, 3.3 * TAU], color=th.AMBER, stroke_width=4)
        axes_ = VGroup(DashedLine(c0 + LEFT * 3.0, c0 + RIGHT * 3.0, color=th.FAINT), DashedLine(c0 + DOWN * 3.0, c0 + UP * 3.0, color=th.FAINT))
        q = VGroup(T("1 determine objectives", size=22, color=th.INK).move_to(c0 + np.array([-2.3, 2.6, 0])), T("2 identify and resolve risks", size=22, color=th.CORAL).move_to(c0 + np.array([2.2, 2.6, 0])),
                   T("3 develop and test", size=22, color=th.INK).move_to(c0 + np.array([1.8, -2.7, 0])), T("4 plan the next loop", size=22, color=th.INK).move_to(c0 + np.array([-1.8, -2.7, 0])))
        txt = para("Boehm, 1988. A prototype in every loop attacks the biggest remaining risk; radius = cost so far. Best for large, costly, safety-critical systems; expensive, needs risk experts.", width=5.2, size=22, color=th.BODY).move_to([3.8, 0.2, 0])
        with self.say("Boehm's spiral model is driven by risk. Each loop passes through four quadrants: set objectives, identify and resolve risks with a prototype, develop and test, then plan the next loop. The spiral grows as cost accumulates. It suits large, expensive, safety critical systems, but it is costly and needs real risk expertise."):
            self.play(FadeIn(h), Create(axes_), FadeIn(q))
            self.play(Create(sp), run_time=3.0)
            self.play(FadeIn(txt))
        self.play(FadeOut(VGroup(h, sp, axes_, q, txt)))
        h = C.head(self, "Agile (Scrum): working software every sprint")
        bl = VGroup(*[RoundedRectangle(corner_radius=0.05, width=1.4, height=0.35, stroke_width=0, fill_color=th.SKY, fill_opacity=0.6) for _ in range(6)]).arrange(DOWN, buff=0.08).move_to([-5.4, -0.2, 0])
        bll = T("product backlog", size=20, color=th.SKY).next_to(bl, UP, buff=0.15)
        c1 = np.array([-0.2, -0.2, 0])
        circ = Circle(radius=1.4, stroke_color=th.MINT, stroke_width=4).move_to(c1)
        cl = VGroup(T("sprint\n1–4 weeks", size=22, color=th.MINT).move_to(c1), T("daily stand-up", size=18, color=th.MUTED).next_to(circ, UP, buff=0.1))
        inc = VGroup(RoundedRectangle(corner_radius=0.08, width=2.2, height=0.8, stroke_color=th.AMBER, stroke_width=3), T("shippable\nincrement", size=20, color=th.AMBER)).move_to([3.4, -0.2, 0])
        a1, a2 = Arrow(bl.get_right(), circ.get_left(), buff=0.1, color=th.MUTED), Arrow(circ.get_right(), inc.get_left(), buff=0.1, color=th.MUTED)
        rv = T("review + retrospective → next sprint", size=20, color=th.MUTED).move_to([1.6, -2.2, 0])
        vals = T("Manifesto 2001: people, working software, collaboration, responding to change", size=22, color=th.INK).move_to([0, 2.0, 0])
        vals.scale_to_fit_width(min(vals.width, 12.2))
        with self.say("Agile methods, like Scrum, follow the Agile Manifesto of two thousand and one. The product owner keeps a prioritised backlog. The team takes the top items into a sprint of one to four weeks, meets daily for fifteen minutes, and ends with a working, shippable increment, a review and a retrospective. Requirements may change freely between sprints. The cost: little documentation, and it needs an engaged customer."):
            self.play(FadeIn(h), FadeIn(vals))
            self.play(FadeIn(bl), FadeIn(bll), GrowArrow(a1), Create(circ), FadeIn(cl))
            self.play(Rotate(circ, TAU, about_point=c1), run_time=1.5)
            self.play(GrowArrow(a2), FadeIn(inc), FadeIn(rv))
        self.play(FadeOut(VGroup(h, bl, bll, circ, cl, inc, a1, a2, rv, vals)))
        rows = [["model", "requirements", "risk handling", "best for"], ["waterfall", "fixed, known", "poor", "legal / tender specs"], ["prototype", "unclear, UI-heavy", "medium", "new services"], ["incremental", "core known", "medium", "systems that split into features"],
                ["spiral", "may change; large", "best", "large, safety-critical"], ["agile", "change constantly", "good", "startups, apps, web products"]]
        tb = C.table(rows, [2.6, 3.4, 2.6, 4.4], row_h=0.6, size=24, colors=[th.AMBER, th.INK, th.MINT, th.SKY]).move_to([0, 0.5, 0])
        with self.say("The models side by side. Fixed requirements: waterfall. Unclear ones: prototype. A system that splits into features: incremental. Large and dangerous: spiral. Constantly changing: agile.") as v:
            C.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))
        C.worked(self, "A backlog of 260 story points; velocity 40 points per 3-week sprint. How long? What if 60 points are added after sprint 2?",
                 [r"\frac{260}{40} = 6.5 \to 7 \text{ sprints} = 21 \text{ weeks}", r"260 + 60 = 320:\ \frac{320}{40} = 8 \text{ sprints} = 24 \text{ weeks}", r"\text{+3 weeks, and nothing already built is thrown away}"],
                 ["Planning sprints.", "Two sixty over forty is six and a half: seven sprints, twenty one weeks.", "Add sixty points: eight sprints, twenty four weeks.", "The change costs three weeks, and nothing already built is wasted. In waterfall it would mean redoing design, code and tests."])
        self.quiz("Which model is driven by explicit risk analysis in every loop?",
                  ["waterfall", "prototype", "spiral", "agile"], 2,
                  "Pause and think.",
                  "The spiral model: each loop identifies and resolves the biggest remaining risk.")
        self.quiz("In a DFD, a circle (bubble) represents",
                  ["an external entity", "a process", "a data store", "a decision"], 1,
                  "One more.",
                  "A process, named with a verb. DFDs have no decision symbol at all.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "A project balances scope, time, cost and quality; effort in person-months.",
            "SDLC: investigation, feasibility, analysis, design, coding, testing, implementation, maintenance.",
            "Analyst asks WHAT, engineer asks HOW; requirements must be testable; high cohesion, low coupling.",
            "DFD: process, entity, data store, data flow — data only, no decisions.",
            "Waterfall (fixed), prototype (unclear), incremental, spiral (risk), agile (changing).",
        ], "Quick recap. Projects and their four constraints. The eight phases of the SDLC. Analysts, requirements and design. Data flow diagrams. Software quality. And the five development models, each suited to a different kind of project.")
        self.outro("That was the software process model. Next and last, recent trends in technology: AI, cloud, blockchain and more. See you there.")
