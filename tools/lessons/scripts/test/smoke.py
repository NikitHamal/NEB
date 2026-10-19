from manim import *
from kit import Lesson, T, M, th

class Lesson(Lesson):
    SUBJECT="phy"; GRADE=12; UNIT=1; TITLE="Rotational Dynamics"; SUBTITLE="The physics of spin"
    SECTIONS=["Angular kinematics","Moment of inertia"]
    def lesson(self):
        g,nb=self.title_card()
        with self.say("Welcome. Today we learn why spinning things behave the way they do."): pass
        self.end_title(g,nb)
        self.section(0)
        eq=M(r"\omega = \frac{d\theta}{dt}", size=72)
        with self.say("Angular velocity is the rate of change of angle."):
            self.play(Write(eq))
        self.quiz("Which has more moment of inertia?", ["A ring","A disc","Same","Depends"],0,
                  "Pause and think.","A ring: all its mass sits at the rim.", think=2)
        self.recap(["Omega is d theta by d t","Rings resist spin more"],"That is it.")
        self.outro("See you next time.")
