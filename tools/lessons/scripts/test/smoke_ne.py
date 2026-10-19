from manim import *
from kit import Lesson, T, M, th, para

class Lesson(Lesson):
    SUBJECT="nep"; GRADE=12; UNIT=1; TITLE="शिक्षा र राष्ट्र"; LANG="ne"
    SECTIONS=["कविको परिचय","कविताको सार"]
    def lesson(self):
        g,nb=self.title_card()
        with self.say("नमस्ते! आजको पाठमा हामी कविताको भाव बुझ्नेछौं।"): pass
        self.end_title(g,nb)
        self.section(0)
        p=para("क्षत्रिय, द्वन्द्व, श्रद्धा, प्रकृति र संस्कृति जस्ता संयुक्त अक्षर ठीकसँग देखिनुपर्छ।", width=10)
        with self.say("संयुक्त अक्षरहरू जाँच्दैछौं।"):
            self.play(FadeIn(p))
        self.outro("फेरि भेटौँला।")
