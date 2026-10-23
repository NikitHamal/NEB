import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _cs as C  # noqa: E402

STU = [[1, "Anisha Shrestha", "Science", "Kathmandu"], [2, "Bikash Tamang", "Science", "Lalitpur"], [3, "Chandra Gurung", "Management", "Kaski"], [4, "Deepa Yadav", "Science", "Dhanusha"], [5, "Eliza Rai", "Management", "Morang"]]
ENR = [[1, "CS401", 78], [1, "MA402", 65], [1, "PH404", 71], [2, "CS401", 52], [2, "MA402", 48], [3, "CS401", 85], [3, "EN403", 66], [4, "CS401", 91], [4, "MA402", 74], [4, "PH404", 59], [5, "EN403", 45]]


def row_hl(tb, i, color=th.AMBER):
    return SurroundingRectangle(tb[i], color=color, buff=0.03, stroke_width=3)


class Lesson(Lesson):
    SUBJECT = "cs"
    GRADE = 12
    UNIT = 1
    TITLE = "Database Management System"
    SUBTITLE = "Storing data once, and asking it anything"
    SECTIONS = ["Data, databases and the DBMS", "Fields, records and keys", "SQL: DDL and DML", "Joins and grouping", "Database models", "Normalisation: 1NF, 2NF, 3NF", "Distributed databases and security"]
    NEXT = "Unit 2 · Data Communication and Networking"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        f1 = C.dbtable("office.xlsx", ["roll", "name", "district"], [[1, "Anisha Shrestha", "Kathmandu"], [2, "Bikash Tamang", "Lalitpur"]], widths=[1.0, 3.2, 2.2], size=26, row_h=0.5, name_color=th.SKY).move_to([-3.4, 1.0, 0])
        f2 = C.dbtable("exam.xlsx", ["roll", "name", "district"], [[1, "Anisha Shrestha", "Kathmandu"], [2, "Bikash Tamang", "Lalitpur"]], widths=[1.0, 3.2, 2.2], size=26, row_h=0.5, name_color=th.PINK).move_to([3.4, 1.0, 0])
        with self.say("A school keeps its records in two spreadsheets: one in the office, one in the exam section. Both list Anisha, from Kathmandu."):
            self.play(FadeIn(f1), FadeIn(f2))
        new = T("Bhaktapur", size=26, color=th.MINT).move_to(f1.tb[1][3])
        old = f1.tb[1][3]
        q = VGroup(T("Where does Anisha live?", size=30, color=th.INK), T("two copies → two answers", size=28, color=th.CORAL, weight="BOLD")).arrange(DOWN, buff=0.25).move_to([0, -1.6, 0])
        with self.say("She moves to Bhaktapur. The office updates its copy. Nobody tells the exam section. Now the school has two different answers to one question, and no way to know which is right. That is what goes wrong when the same data is stored in many places."):
            self.play(FadeOut(old, shift=UP * 0.2), FadeIn(new, shift=UP * 0.2))
            f1.add(new)
            self.play(Indicate(f2.tb[1][3], color=th.CORAL))
            self.play(FadeIn(q))
        with self.say("A database management system stores each fact once, shares it with everyone, and answers any question you can ask. This unit shows you how."):
            nb = C.neby_in(self, "think", height=1.3)
        C.neby_out(self, nb)
        self.play(FadeOut(VGroup(f1, f2, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Computer Science, Unit 1: Database Management System."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Seven parts. Data, databases and the DBMS. Fields, records and keys. SQL for defining and changing data. Joins and grouping. The database models. Normalisation. And distributed databases and security.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = C.head(self, "From data to information")
        raw = VGroup(*[T(s_, size=28, color=th.MUTED) for s_ in ["Anisha Shrestha", "78", "CS401", "2007-04-12"]]).arrange(DOWN, buff=0.35).move_to([-4.2, 0.0, 0])
        arr = Arrow([-2.4, 0, 0], [-0.6, 0, 0], color=th.AMBER, stroke_width=6)
        pl = T("processing", size=26, color=th.AMBER).next_to(arr, UP, buff=0.1)
        info = para("“Anisha scored 78 in Computer Science, the second highest in her class.”", width=5.4, size=28, color=th.MINT).move_to([3.0, 0.0, 0])
        lab = VGroup(T("data: raw facts", size=28, color=th.MUTED).next_to(raw, DOWN, buff=0.4), T("information: processed, useful", size=28, color=th.MINT).next_to(info, DOWN, buff=0.4))
        with self.say("Data are raw facts: a name, a number, a date. On their own they mean nothing. Processed into a sentence that helps someone decide, they become information."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(r_) for r_ in raw], lag_ratio=0.2))
            self.play(GrowArrow(arr), FadeIn(pl))
            self.play(FadeIn(info), FadeIn(lab))
        self.play(FadeOut(VGroup(h, raw, arr, pl, info, lab)))
        rows = [["component", "what it is"], ["hardware", "servers, disks, network links"], ["software", "the DBMS, the OS, application programs"], ["data", "stored data + metadata (the data dictionary)"], ["users", "end users, programmers, the DBA"], ["procedures", "rules for backup, recovery, access"]]
        tb = C.table(rows, [3.0, 7.8], row_h=0.62, size=26, colors=[th.AMBER, th.INK]).move_to([0, 0.4, 0])
        defs = para("Database: an organised collection of related data shared by many users. DBMS: the software that defines, stores, retrieves and controls it — MySQL, Oracle, PostgreSQL, SQLite, MS Access.", width=11.5, size=28, color=th.BODY).move_to([0, -2.6, 0])
        with self.say("A database is an organised collection of related data, shared by many users and programs. The DBMS is the software that manages it, such as MySQL or Oracle. And a database system is the whole arrangement: hardware, software, the data itself, the users, including the database administrator, and the procedures they follow.") as v:
            C.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(defs))
        self.play(FadeOut(VGroup(tb, defs)))
        h = C.head(self, "Three levels: why programs survive a reorganised disk")
        lv = VGroup()
        specs = [("External level", "each user's own view", th.SKY), ("Conceptual level", "all entities, attributes, relationships, constraints", th.MINT), ("Internal level", "files, indexes, blocks on disk", th.AMBER)]
        for k, (a, b, c_) in enumerate(specs):
            box = RoundedRectangle(corner_radius=0.15, width=8.2, height=1.2, stroke_color=c_, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
            lv.add(VGroup(box, VGroup(T(a, size=30, color=c_, weight="BOLD"), T(b, size=28, color=th.BODY)).arrange(DOWN, buff=0.08).move_to(box)))
        lv.arrange(DOWN, buff=0.55).move_to([-2.4, -0.4, 0])
        ar = VGroup(*[DoubleArrow(lv[k].get_bottom(), lv[k + 1].get_top(), buff=0.05, color=th.MUTED, stroke_width=3, tip_length=0.15) for k in range(2)])
        ind = VGroup(VGroup(T("logical data independence", size=26, color=th.MINT, weight="BOLD"), para("add a table or column without changing users' views", width=4.4, size=26, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, 0.6, 0]),
                     VGroup(T("physical data independence", size=26, color=th.AMBER, weight="BOLD"), para("add an index or move to a new disk without changing the schema", width=4.4, size=26, color=th.BODY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, -1.3, 0]))
        with self.say("The ANSI SPARC architecture splits a database into three levels. At the top, each user sees their own external view. In the middle, the conceptual level describes everything: all the entities and how they relate. At the bottom, the internal level is how it actually sits on disk."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(l_, shift=DOWN * 0.2) for l_ in lv], lag_ratio=0.3))
            self.play(Create(ar))
        with self.say("Because the levels are separate, you can change one without breaking the others. Add a new column, and existing views still work: logical data independence. Add an index or move to a faster disk, and the schema does not change: physical data independence."):
            self.play(FadeIn(ind[0], shift=LEFT * 0.2))
            self.play(FadeIn(ind[1], shift=LEFT * 0.2))
        self.play(FadeOut(VGroup(h, lv, ar, ind)))
        rows = [["", "file system", "DBMS"], ["redundancy", "same data in many files", "stored once, shared"], ["consistency", "copies drift apart", "one copy, one truth"], ["new question", "write a new program", "write a query"], ["integrity", "rules buried in programs", "constraints in the schema"],
                ["concurrency", "two users can clash", "locking and transactions"], ["security", "whole-file only", "per table, per column"], ["cost", "cheap, simple", "costly, needs a DBA"]]
        tb = C.table(rows, [2.6, 4.4, 4.4], row_h=0.56, size=28, colors=[th.AMBER, th.CORAL, th.MINT]).move_to([0, 0.0, 0])
        with self.say("Compare the old file system with a DBMS. Files repeat data and drift apart; a DBMS stores it once. Files need a new program for every new question; a DBMS answers any query. It enforces rules, handles many users at once, and controls who sees what. The price: cost, complexity, and a trained administrator.") as v:
            C.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = C.head(self, "A table: fields and records")
        t = C.dbtable("students", ["roll", "name", "faculty", "district"], STU, widths=[1.1, 3.4, 2.6, 2.6], size=28, row_h=0.6, pk=("roll",)).move_to([-1.4, 0.0, 0])
        col = SurroundingRectangle(VGroup(*[t.tb[i][3] for i in range(len(t.tb))]), color=th.SKY, buff=0.06)
        row = SurroundingRectangle(t.tb[3], color=th.MINT, buff=0.04)
        cl = T("field (column, attribute)", size=26, color=th.SKY).next_to(col, DOWN, buff=0.2)
        rl = T("record (row, tuple)", size=26, color=th.MINT)
        with self.say("Data in a relational database lives in tables. A field is one column: one property, with one data type, like faculty. A record is one row: everything about one student."):
            self.play(FadeIn(h), FadeIn(t))
            self.play(Create(col), FadeIn(cl))
            self.play(Create(row), FadeIn(cl.copy().set_opacity(0)))
            rl.next_to(row, RIGHT, buff=0.25)
            self.play(FadeIn(rl))
        self.play(FadeOut(VGroup(h, t, col, row, cl, rl)))
        h = C.head(self, "The family of keys")
        tb = C.dbtable("STUDENT", ["Roll", "Symbol_No", "Email", "Name", "Faculty"], [[1, "7801", "anisha@…", "Anisha", "Science"], [2, "7802", "bikash@…", "Bikash", "Science"], [3, "7803", "chandra@…", "Chandra", "Mgmt"]],
                        widths=[1.2, 2.3, 2.8, 2.0, 2.0], size=26, row_h=0.52).move_to([0, 1.3, 0])
        cand = VGroup(*[SurroundingRectangle(VGroup(*[tb.tb[i][c] for i in range(4)]), color=th.AMBER, buff=0.04) for c in (1, 2, 3)])
        keys = VGroup(T("candidate keys: {Roll}, {Symbol_No}, {Email} — each unique and minimal", size=28, color=th.AMBER), T("primary key: {Roll}  (chosen; never NULL, never repeated)", size=28, color=th.MINT),
                      T("alternate keys: {Symbol_No}, {Email}  (candidates not chosen)", size=28, color=th.SKY), T("super key: {Roll, Name}  (unique, but not minimal)", size=28, color=th.MUTED),
                      T("foreign key: a column whose values must exist as a primary key elsewhere", size=28, color=th.PINK)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -1.7, 0])
        keys.scale_to_fit_width(min(keys.width, 12.6))
        with self.say("Keys identify rows. Here no two students share a roll number, a symbol number or an email. Each of these alone is unique, and cannot be made smaller: they are the candidate keys."):
            self.play(FadeIn(h), FadeIn(tb))
            self.play(Create(cand))
            self.play(FadeIn(keys[0]))
        with self.say("The designer picks one as the primary key: roll, short and stable. It can never be empty or repeated. The others become alternate keys. Add any extra column, like roll with name, and it is still unique but not minimal: a super key. And a foreign key is a column whose values must already exist as a primary key in another table: that is what links tables."):
            self.play(FadeOut(cand[1:]), cand[0].animate.set_color(th.MINT), FadeIn(keys[1]))
            self.play(FadeIn(keys[2]))
            self.play(FadeIn(keys[3]))
            self.play(FadeIn(keys[4]))
        self.play(FadeOut(VGroup(h, tb, cand, keys)))
        c = self.callout("careful", "A primary key is not 'the first column' or 'the column called ID'. It is a declared constraint: unique and NOT NULL. A composite key (roll, code) is ONE key of two columns, not two primary keys.", width=11, size=25)
        with self.say("A common mistake: the primary key is not simply the first column. It is a rule the DBMS enforces: unique and never null. And a key made of two columns together is still one primary key."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = C.head(self, "DDL defines structure; DML works with the data")
        ddl = C.code(["CREATE TABLE students (", "  roll     INTEGER PRIMARY KEY,", "  name     VARCHAR(40) NOT NULL,", "  faculty  VARCHAR(20),", "  district VARCHAR(20)", ");"], size=28, title="DDL").to_edge(LEFT, buff=0.5).shift(UP * 0.3)
        lst = VGroup(T("DDL: CREATE, ALTER, DROP, TRUNCATE", size=26, color=th.SKY), T("DML: SELECT, INSERT, UPDATE, DELETE", size=26, color=th.AMBER),
                     para("DROP removes the table itself; TRUNCATE removes every row but keeps the table; DELETE removes chosen rows.", width=4.6, size=25, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        lst.scale_to_fit_width(min(lst.width, 5.2)).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        with self.say("SQL has two halves. The data definition language builds the structure: CREATE a table, with each column's type and constraints. Roll is the primary key; name may not be empty."):
            self.play(FadeIn(h))
            C.type_code(self, ddl, per_line=0.4)
        with self.say("DDL also has ALTER, DROP and TRUNCATE. The data manipulation language works with the rows: SELECT, INSERT, UPDATE and DELETE. Do not mix up DROP, which deletes the whole table, with DELETE, which removes chosen rows."):
            self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.2) for l_ in lst], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, ddl, lst)))
        h = C.head(self, "SELECT … WHERE: filter the rows")
        t = C.dbtable("students", ["roll", "name", "faculty", "district"], STU, widths=[1.0, 2.9, 2.2, 2.2], size=28, row_h=0.5, pk=("roll",)).move_to([-2.9, -1.1, 0])
        q = C.code(["SELECT roll, name, district", "FROM students", "WHERE faculty = 'Science'", "ORDER BY name;"], size=28).move_to([3.7, 1.4, 0])
        with self.say("Retrieving data. Select the roll, name and district from students, where the faculty is Science, ordered by name. Watch what the query does to the table."):
            self.play(FadeIn(h), FadeIn(t))
            C.type_code(self, q, per_line=0.35)
        keep = [i for i, r in enumerate(STU, start=1) if r[2] == "Science"]
        drop = [i for i in range(1, 6) if i not in keep]
        with self.say("WHERE keeps only the rows that pass the test: the two Management students drop out. SELECT keeps only the columns named, so faculty goes too. Three rows remain, already in alphabetical order."):
            self.play(*[t.tb[i].animate.set_opacity(0.15) for i in drop], *[Create(row_hl(t.tb, i, th.MINT)) for i in keep])
            self.play(*[t.tb[i][3].animate.set_opacity(0.15) for i in range(len(t.tb))])
        self.play(FadeOut(VGroup(h, t, q)), *[FadeOut(m) for m in self.mobjects if isinstance(m, SurroundingRectangle)])
        ex = VGroup(C.code(["SELECT name, district FROM students", "WHERE district IN ('Kathmandu', 'Kaski');"], size=28), C.code(["SELECT DISTINCT faculty FROM students;"], size=28),
                    C.code(["SELECT MAX(marks), MIN(marks), AVG(marks)", "FROM enrolment;     -- 91, 45, 66.73"], size=28), C.code(["INSERT INTO students VALUES (6, 'Firoj Ansari', 'Science', 'Parsa');"], size=26),
                    C.code(["UPDATE enrolment SET marks = marks + 5 WHERE code = 'EN403';"], size=26), C.code(["DELETE FROM enrolment WHERE marks < 50;"], size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ex.scale_to_fit_height(min(ex.height, 5.6)).move_to([0, -0.3, 0])
        hd = T("More DML", size=30, weight="BOLD").to_edge(UP, buff=0.75)
        with self.say("More queries. IN tests against a list. DISTINCT removes repeated values. The aggregate functions, count, sum, average, max and min, collapse many rows into one value. INSERT adds a row, UPDATE changes values, and DELETE removes rows, each with a WHERE clause to pick which ones.") as v:
            self.play(FadeIn(hd))
            C.reveal_list(self, ex, v.dur * 0.85, shift=UP * 0.1)
        self.play(FadeOut(VGroup(hd, ex)))
        c = self.callout("careful", "UPDATE or DELETE without WHERE changes EVERY row: DELETE FROM enrolment; empties the table. Always write the WHERE clause first.", width=11, size=26)
        with self.say("The most dangerous line in SQL: an UPDATE or DELETE with no WHERE clause. It hits every single row."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = C.head(self, "JOIN: match foreign key to primary key")
        s = C.dbtable("students", ["roll", "name"], [[r[0], r[1]] for r in STU[:4]], widths=[0.9, 2.8], size=26, pk=("roll",)).move_to([-4.6, 0.6, 0])
        e = C.dbtable("enrolment", ["roll", "code", "marks"], ENR[:8], widths=[0.9, 1.4, 1.1], size=24, row_h=0.38, fk=("roll", "code")).move_to([0.2, 0.3, 0])
        cmap = {"CS401": "Computer Science", "MA402": "Mathematics", "PH404": "Physics", "EN403": "English"}
        c = C.dbtable("courses", ["code", "title"], [[k, v] for k, v in list(cmap.items())], widths=[1.3, 2.8], size=26, pk=("code",)).move_to([4.7, 0.6, 0])
        links = VGroup()
        for i, r in enumerate(ENR[:8], start=1):
            si = r[0]
            links.add(Line(s.tb[si].get_right(), e.tb[i].get_left(), color=th.SKY, stroke_width=1.8, stroke_opacity=0.7))
            ci = list(cmap).index(r[1]) + 1
            links.add(Line(e.tb[i].get_right(), c.tb[ci].get_left(), color=th.PINK, stroke_width=1.8, stroke_opacity=0.7))
        with self.say("Real questions need several tables. Each enrolment row holds a roll number and a course code: foreign keys. A JOIN matches each one to the primary key it points at: rolls to students, codes to courses."):
            self.play(FadeIn(h), FadeIn(s), FadeIn(e), FadeIn(c))
            self.play(LaggedStart(*[Create(l_) for l_ in links], lag_ratio=0.05), run_time=2.5)
        q = C.code(["SELECT s.name, c.title, e.marks", "FROM students s", "JOIN enrolment e ON s.roll = e.roll", "JOIN courses c ON c.code = e.code;"], size=26).to_edge(DOWN, buff=0.35)
        with self.say("In SQL: join students to enrolment on roll, and enrolment to courses on code. Every enrolment row now carries a name and a course title."):
            C.type_code(self, q, per_line=0.4)
        self.play(FadeOut(VGroup(h, s, e, c, links, q)))
        h = C.head(self, "GROUP BY: rows into groups, groups into one line")
        e = C.dbtable("enrolment", ["roll", "code", "marks"], ENR, widths=[0.9, 1.4, 1.1], size=24, row_h=0.36).move_to([-4.0, -0.2, 0])
        cols = {"CS401": th.SKY, "MA402": th.AMBER, "PH404": th.MINT, "EN403": th.PINK}
        res = C.table([["title", "students", "avg"], ["Computer Science", "4", "76.5"], ["Physics", "2", "65.0"], ["Mathematics", "3", "62.3"], ["English", "2", "55.5"]], [3.0, 1.6, 1.3], row_h=0.5, size=26, colors=[th.INK, th.INK, th.AMBER]).move_to([3.3, -0.3, 0])
        for k, colr in zip(range(1, 5), [th.SKY, th.MINT, th.AMBER, th.PINK]):
            res[k][1].set_color(colr)
        q = C.code(["SELECT c.title, COUNT(e.roll), AVG(e.marks)", "FROM courses c JOIN enrolment e ON c.code = e.code", "GROUP BY c.title ORDER BY AVG(e.marks) DESC;"], size=22, max_width=7.6).move_to([2.6, 1.8, 0])
        with self.say("GROUP BY sorts rows into groups with the same value, here the same course, and an aggregate turns each group into one line. Colour the enrolments by course."):
            self.play(FadeIn(h), FadeIn(e), FadeIn(q))
            self.play(*[e.tb[i][0].animate.set_fill(cols[r[1]], opacity=0.35) for i, r in enumerate(ENR, start=1)])
        with self.say("Four Computer Science rows average seventy six and a half. Physics, Mathematics and English follow. Nepali does not appear at all: with an inner join, a course with nobody enrolled has no rows to group. A LEFT JOIN would keep it with a count of zero."):
            C.reveal_table(self, res, 3.0)
        hv = C.code(["... GROUP BY s.roll", "HAVING COUNT(*) >= 3;   -- groups, not rows"], size=24, max_width=6.4).move_to([3.3, -2.4, 0])
        with self.say("To filter groups rather than rows, use HAVING. WHERE removes rows before grouping; HAVING removes groups after. So students with three or more subjects is HAVING count at least three."):
            C.type_code(self, hv, per_line=0.4)
        self.play(FadeOut(VGroup(h, e, res, q, hv)))
        err = C.terminal(["mysql> INSERT INTO enrolment VALUES (99, 'CS401', 60);", "ERROR 1452: Cannot add or update a child row:", "a foreign key constraint fails"], size=24).move_to([0, 0.8, 0])
        nt = para("There is no student 99, so the DBMS refuses. Likewise it refuses to delete CS401 while enrolments still point at it. That refusal is referential integrity.", width=11, size=28, color=th.BODY).move_to([0, -1.4, 0])
        with self.say("And the DBMS defends its rules. Try to enrol a student number ninety nine, who does not exist: refused, a foreign key constraint fails. Try to delete a course that students are enrolled in: refused again. That is referential integrity."):
            self.play(FadeIn(err))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(err, nt)))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = C.head(self, "Three ways to organise data")

        def nd(t_, p_, col=th.SKY, w=1.6):
            return C.node(t_, col, w=w, h=0.6, size=22).move_to(p_)

        hier = VGroup(nd("SCHOOL", [-4.6, 1.4, 0], th.AMBER), nd("Science", [-5.6, 0.2, 0]), nd("Management", [-3.6, 0.2, 0], w=1.8), nd("Anisha", [-6.1, -1.0, 0], th.MINT, 1.2), nd("Bikash", [-4.9, -1.0, 0], th.MINT, 1.2), nd("Chandra", [-3.6, -1.0, 0], th.MINT, 1.3))
        he = VGroup(*[Line(hier[a][0].get_bottom(), hier[b][0].get_top(), color=th.MUTED) for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]])
        net = VGroup(nd("CS401", [-0.6, 1.0, 0], th.AMBER, 1.3), nd("MA402", [1.4, 1.0, 0], th.AMBER, 1.3), nd("Anisha", [-1.1, -0.6, 0], th.MINT, 1.2), nd("Bikash", [0.4, -0.6, 0], th.MINT, 1.2), nd("Deepa", [1.9, -0.6, 0], th.MINT, 1.2))
        ne = VGroup(*[Line(net[a][0].get_bottom(), net[b][0].get_top(), color=th.MUTED) for a, b in [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]])
        rel = VGroup(C.dbtable("students", ["roll", "name"], [[1, "Anisha"], [2, "Bikash"]], widths=[0.8, 1.6], size=22, row_h=0.34, pk=("roll",)), C.dbtable("enrolment", ["roll", "code"], [[1, "CS401"], [2, "MA402"]], widths=[0.8, 1.3], size=22, row_h=0.34, fk=("roll", "code"))).arrange(DOWN, buff=0.3).move_to([4.9, 0.2, 0])
        labs = VGroup(T("hierarchical: a tree", size=28, color=th.AMBER).move_to([-4.6, -2.0, 0]), T("network: a graph", size=28, color=th.AMBER).move_to([0.4, -2.0, 0]), T("relational: tables", size=28, color=th.AMBER).move_to([4.9, -2.0, 0]))
        subs = VGroup(T("one parent each (IBM IMS)", size=22, color=th.MUTED).next_to(labs[0], DOWN, buff=0.1), T("many parents (CODASYL)", size=22, color=th.MUTED).next_to(labs[1], DOWN, buff=0.1), T("matching keys (Codd, 1970)", size=22, color=th.MUTED).next_to(labs[2], DOWN, buff=0.1))
        allm = VGroup(hier, he, net, ne, rel, labs, subs)
        allm.move_to([0, -0.3, 0])
        with self.say("Three database models. The hierarchical model is an upside down tree: every record has exactly one parent, so it handles one to many, but not many to many."):
            self.play(FadeIn(h), FadeIn(hier), Create(he), FadeIn(labs[0]), FadeIn(subs[0]))
        with self.say("The network model allows many parents, a graph. Now a student can belong to several courses and a course to several students."):
            self.play(FadeIn(net), Create(ne), FadeIn(labs[1]), FadeIn(subs[1]))
        with self.say("The relational model, proposed by Codd in nineteen seventy, uses no pointers at all. Relationships are matching values in tables, and you simply state what you want in SQL. Almost every database today is relational."):
            self.play(FadeIn(rel), FadeIn(labs[2]), FadeIn(subs[2]))
        self.play(FadeOut(VGroup(h, hier, he, net, ne, rel, labs, subs)))
        h = C.head(self, "E-R diagram: entities, attributes, relationships")
        st = VGroup(Rectangle(width=2.0, height=0.8, stroke_color=th.SKY, stroke_width=3), T("STUDENT", size=28, color=th.SKY, weight="BOLD")).move_to([-4.0, 0, 0])
        co = VGroup(Rectangle(width=2.0, height=0.8, stroke_color=th.SKY, stroke_width=3), T("COURSE", size=28, color=th.SKY, weight="BOLD")).move_to([4.0, 0, 0])
        rl = VGroup(Square(side_length=1.2, stroke_color=th.AMBER, stroke_width=3).rotate(PI / 4), T("ENROLS", size=24, color=th.AMBER, weight="BOLD")).move_to([0, 0, 0])
        lines = VGroup(Line(st.get_right(), rl[0].get_left(), color=th.MUTED), Line(rl[0].get_right(), co.get_left(), color=th.MUTED))
        card = VGroup(T("M", size=26, color=th.CORAL).next_to(lines[0], UP, buff=0.05), T("N", size=26, color=th.CORAL).next_to(lines[1], UP, buff=0.05))

        def attr(t_, p_, key=False, anchor=None):
            e_ = Ellipse(width=2.0, height=0.75, stroke_color=th.MINT, stroke_width=2).move_to(p_)
            tx = T(t_, size=22, color=th.MINT).move_to(p_)
            if key:
                tx.add(Underline(tx, color=th.MINT, buff=0.02))
            return VGroup(Line(e_.get_center(), anchor, color=th.FAINT, stroke_width=2), e_, tx)

        at = VGroup(attr("Roll", [-5.3, 1.5, 0], True, st.get_center()), attr("Name", [-3.0, 1.6, 0], anchor=st.get_center()), attr("Faculty", [-4.2, -1.5, 0], anchor=st.get_center()),
                    attr("Code", [3.0, 1.6, 0], True, co.get_center()), attr("Title", [5.3, 1.5, 0], anchor=co.get_center()), attr("Marks", [0, -1.6, 0], anchor=rl.get_center()))
        for a_ in at:
            a_[0].set_z_index(-1)
        with self.say("Before building tables, designers draw an entity relationship diagram. Rectangles are entities, the things we store data about. Ovals are their attributes, with the key underlined. The diamond is a relationship: a student enrols in courses."):
            self.play(FadeIn(h), FadeIn(st), FadeIn(co), FadeIn(rl), Create(lines))
            self.play(LaggedStart(*[FadeIn(a_) for a_ in at], lag_ratio=0.15))
        with self.say("Its cardinality is many to many: a student takes many courses and a course has many students. In tables, a many to many relationship always becomes its own link table, here enrolment, which also holds the marks."):
            self.play(FadeIn(card))
        self.play(FadeOut(VGroup(h, st, co, rl, lines, card, at)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = C.head(self, "Unnormalised: a repeating group")
        unf = C.table([["roll", "name", "faculty", "head", "courses"], ["1", "Anisha", "Science", "R. Sharma", "CS401 78, MA402 65"], ["3", "Chandra", "Mgmt", "S. Karki", "CS401 85, EN403 66"], ["4", "Deepa", "Science", "R. Sharma", "CS401 91, MA402 74"]],
                      [0.8, 1.6, 1.5, 1.8, 4.0], row_h=0.55, size=26).move_to([0, 1.2, 0])
        hl = SurroundingRectangle(VGroup(*[unf[i][5] for i in range(1, 4)]), color=th.CORAL, buff=0.05)
        nt = para("Normalisation splits a badly designed table into smaller ones so that each fact is stored once — without losing anything: a join brings the original back.", width=11, size=28, color=th.BODY).move_to([0, -1.4, 0])
        with self.say("Here is one table holding a school's whole result record. The courses column crams several values into one cell, a repeating group. You cannot even ask who scored above eighty in CS four oh one. Normalisation fixes designs like this, step by step, without losing any information."):
            self.play(FadeIn(h), FadeIn(unf))
            self.play(Create(hl))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, unf, hl, nt)))
        h = C.head(self, "1NF: one value per cell; key (roll, code)")
        one = C.table([["roll", "name", "faculty", "head", "code", "marks"], ["1", "Anisha", "Science", "R. Sharma", "CS401", "78"], ["1", "Anisha", "Science", "R. Sharma", "MA402", "65"], ["3", "Chandra", "Mgmt", "S. Karki", "CS401", "85"],
                       ["3", "Chandra", "Mgmt", "S. Karki", "EN403", "66"], ["4", "Deepa", "Science", "R. Sharma", "CS401", "91"], ["4", "Deepa", "Science", "R. Sharma", "MA402", "74"]], [0.8, 1.5, 1.4, 1.7, 1.3, 1.1], row_h=0.46, size=25).move_to([-2.4, 0.4, 0])
        for i in range(len(one)):
            for j in (1, 5):
                one[i][j].set_color(th.AMBER)
        fds = VGroup(T("(roll, code) → marks   full", size=26, color=th.MINT), T("roll → name, faculty   PARTIAL", size=26, color=th.CORAL), T("faculty → head   TRANSITIVE", size=26, color=th.PINK)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fds.scale_to_fit_width(min(fds.width, 4.6)).move_to([4.5, 1.2, 0])
        anom = para("Anisha stored twice (update anomaly); a course with no students can't be added (insert); deleting Chandra's English loses the course (delete).", width=4.6, size=22, color=th.MUTED).move_to([4.5, -1.5, 0])
        with self.say("First normal form: every cell holds one value. Give each student and course its own row. Now neither roll nor code alone identifies a row, but together they do: the key is roll and code."):
            self.play(FadeIn(h), FadeIn(one))
        with self.say("Write down what determines what. Marks depend on the whole key. But name and faculty depend on roll alone, only part of the key: a partial dependency. And the faculty head depends on faculty, a non-key column: a transitive dependency. These cause anomalies: data repeated, and things you cannot insert or delete cleanly."):
            for f_ in fds:
                self.play(FadeIn(f_, shift=LEFT * 0.2), run_time=0.6)
            self.play(FadeIn(anom))
        self.play(FadeOut(VGroup(h, one, fds, anom)))
        h = C.head(self, "2NF removes partial dependencies; 3NF removes transitive ones")
        big = C.node("RESULT (roll, name, faculty, head, code, title, marks)", th.CORAL, w=11.0, h=0.8, size=28).move_to([0, 2.0, 0])
        s2 = C.node("STUDENT\n(roll, name, faculty, head)", th.SKY, w=5.0, h=1.05, size=24).move_to([-4.0, 0.45, 0])
        c2 = C.node("COURSE\n(code, title)", th.MINT, w=3.0, h=1.05, size=24).move_to([0.3, 0.5, 0])
        e2 = C.node("ENROLMENT\n(roll, code, marks)", th.AMBER, w=4.2, h=1.05, size=24).move_to([4.5, 0.5, 0])
        s3 = C.node("STUDENT\n(roll, name, faculty)", th.SKY, w=4.4, h=1.05, size=24).move_to([-4.4, -1.6, 0])
        f3 = C.node("FACULTY\n(faculty, head)", th.PINK, w=3.6, h=1.05, size=24).move_to([-0.3, -1.6, 0])
        arr2 = VGroup(*[Arrow(big.get_bottom(), x.get_top() + UP * 0.02, buff=0.08, color=th.MUTED, stroke_width=3) for x in (s2, c2, e2)])
        arr3 = VGroup(*[Arrow(s2.get_bottom(), x.get_top(), buff=0.08, color=th.MUTED, stroke_width=3) for x in (s3, f3)])
        l2 = T("2NF: split off each partial dependency with its own key", size=22, color=th.MUTED).move_to([0, -0.45, 0])
        l3 = T("3NF: split off faculty → head", size=24, color=th.INK).move_to([4.2, -1.6, 0])
        fin = T("four tables, each fact once; joining them gives back every original row (lossless)", size=26, color=th.MINT).move_to([0, -2.6, 0])
        with self.say("Second normal form: remove partial dependencies. Things that depend on roll alone move to a student table; things that depend on code alone move to a course table; what depends on the whole key stays in enrolment."):
            self.play(FadeIn(h), FadeIn(big))
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arr2], lag_ratio=0.2), FadeIn(s2), FadeIn(c2), FadeIn(e2))
            self.play(FadeIn(l2))
        with self.say("Third normal form: remove transitive dependencies. The faculty head depends on faculty, not directly on the student, so it gets its own faculty table. Now Science's head is stored once. Four tables, every fact in one place, and joining them on their keys gives back every original row exactly: the decomposition is lossless."):
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arr3], lag_ratio=0.2), FadeIn(s3), FadeIn(f3), FadeIn(l3))
            self.play(FadeIn(fin))
        self.play(FadeOut(VGroup(h, big, s2, c2, e2, s3, f3, arr2, arr3, l2, l3, fin)))
        rows = [["normal form", "condition", "removes"], ["1NF", "every value atomic", "repeating groups"], ["2NF", "1NF + no partial dependency", "part-key redundancy"], ["3NF", "2NF + no transitive dependency", "non-key → non-key redundancy"]]
        tb = C.table(rows, [2.4, 4.8, 4.6], row_h=0.66, size=25, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.6, 0])
        nt = para("2NF only matters when the key is composite: a single-column key is already in 2NF. Always keep the foreign keys so the tables can be re-joined.", width=11.5, size=27, color=th.CORAL).move_to([0, -1.8, 0])
        with self.say("In summary: first normal form, atomic values. Second, no partial dependencies. Third, no transitive dependencies. Second normal form only matters when the key has more than one column. And keep the foreign keys, or the tables cannot be joined back together.") as v:
            C.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        h = C.head(self, "Centralised vs distributed")
        cen = C.node("Central DB\nKathmandu", th.AMBER, w=2.2, h=1.0, size=24).move_to([-4.2, 0.2, 0])
        cl = VGroup(*[C.node(t_, th.SKY, w=1.5, h=0.55, size=20).move_to(p_) for t_, p_ in [("Pokhara", [-6.0, 1.9, 0]), ("Biratnagar", [-2.4, 1.9, 0]), ("Butwal", [-6.0, -1.5, 0]), ("Dhangadhi", [-2.4, -1.5, 0])]])
        cln = VGroup(*[Line(c_.get_center(), cen.get_center(), color=th.FAINT, stroke_width=2).set_z_index(-1) for c_ in cl])
        sites = VGroup(*[C.node(t_, th.MINT, w=1.7, h=0.75, size=21).move_to(p_) for t_, p_ in [("KTM DB", [2.4, 1.6, 0]), ("PKR DB", [5.6, 1.6, 0]), ("BRT DB", [2.4, -1.2, 0]), ("BTL DB", [5.6, -1.2, 0])]])
        sln = VGroup(*[Line(sites[a].get_center(), sites[b].get_center(), color=th.FAINT, stroke_width=2).set_z_index(-1) for a, b in [(0, 1), (0, 2), (1, 3), (2, 3), (0, 3)]])
        labs = VGroup(T("centralised: one site, easy control, single point of failure", size=24, color=th.AMBER).move_to([-4.2, -2.5, 0]), T("distributed: fragmented/replicated, fast locally, harder to keep in step", size=24, color=th.MINT).move_to([4.0, -2.5, 0]))
        for l_, x_ in zip(labs, (-3.5, 3.5)):
            l_.scale_to_fit_width(min(l_.width, 6.4)).set_x(x_)
        with self.say("Where does the database live? In a centralised system, all of it sits at one site, and every branch reaches across the network. Easy to control and keep consistent, but every request travels, and if the server fails, everything stops."):
            self.play(FadeIn(h), FadeIn(cen), FadeIn(cl), Create(cln))
            pk = [C.packet(th.AMBER).move_to(c_.get_center()) for c_ in cl]
            self.play(*[p_.animate.move_to(cen.get_center()) for p_ in pk], run_time=1.0)
            self.remove(*pk)
            self.play(FadeIn(labs[0]))
        with self.say("In a distributed database, the data is split or copied across several sites, each with its own DBMS, yet it behaves as one database. Local questions are answered locally and the system survives one site failing, but keeping the copies in step is hard."):
            self.play(FadeIn(sites), Create(sln))
            self.play(FadeIn(labs[1]))
        self.play(FadeOut(VGroup(h, cen, cl, cln, sites, sln, labs)))
        sec = VGroup(T("Database security", size=30, weight="BOLD"), C.bullets(["Authentication: passwords, OTP — who are you?", "Authorisation: GRANT and REVOKE privileges per table, even per column", "Views hide columns a user must not see", "Encryption of stored and transmitted data",
                                                                               "Backup, log-based recovery and audit trails", "Defend against SQL injection: never paste user input into a query"], width=11.5, size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.6, 0])
        g = C.code(["GRANT SELECT ON students TO clerk;", "REVOKE DELETE ON enrolment FROM clerk;"], size=26).move_to([0, -2.9, 0])
        with self.say("Finally, security. Authenticate users, then authorise them: GRANT and REVOKE give each user exactly the privileges they need. Views hide sensitive columns. Encrypt data, keep backups and logs, and never paste a user's input straight into a query, which is how SQL injection attacks work.") as v:
            self.play(FadeIn(sec[0]))
            C.reveal_list(self, sec[1], v.dur * 0.7)
            self.play(FadeIn(g))
        self.play(FadeOut(VGroup(sec, g)))
        self.quiz("A candidate key that is NOT chosen as the primary key is called",
                  ["a foreign key", "an alternate key", "a super key", "a composite key"], 1,
                  "Pause and think.",
                  "An alternate key. A foreign key points to another table's primary key.")
        self.quiz("To keep only groups whose average marks are at least 60, use",
                  ["WHERE AVG(marks) >= 60", "HAVING AVG(marks) >= 60", "ORDER BY AVG(marks)", "DISTINCT AVG(marks)"], 1,
                  "One more.",
                  "HAVING: it filters groups after GROUP BY. WHERE cannot use an aggregate.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "DBMS: stores each fact once, shares it, enforces rules; three levels give data independence.",
            "Keys: candidate (minimal unique), primary (chosen, NOT NULL), alternate, super, foreign.",
            "DDL: CREATE, ALTER, DROP, TRUNCATE.  DML: SELECT, INSERT, UPDATE, DELETE.",
            "JOIN foreign key = primary key; GROUP BY + aggregates; WHERE filters rows, HAVING groups.",
            "Models: tree, graph, tables. Normalise: 1NF atomic, 2NF no partial, 3NF no transitive.",
        ], "Quick recap. A DBMS stores each fact once and enforces the rules, with three levels for data independence. The family of keys. DDL builds structure and DML works with rows. Joins match foreign keys to primary keys, and GROUP BY with HAVING summarises. Three models, and normalisation to third normal form.")
        self.outro("That was database management systems. Next, data communication and networking: how computers talk to each other. See you there.")
