import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _cs as C  # noqa: E402


def stack_grid():
    """Who manages what: on-premises, IaaS, PaaS, SaaS (customer = amber, provider = sky)."""
    rows = ["Application", "Data", "Runtime", "Operating system", "Virtualisation", "Servers", "Storage", "Networking"]
    cols = [("On-premises", set(range(8))), ("IaaS", {0, 1, 2, 3}), ("PaaS", {0, 1}), ("SaaS", {1})]
    g = VGroup()
    labels = VGroup(*[T(r, size=22, color=th.INK).move_to([-3.2, 1.75 - 0.5 * i, 0], aligned_edge=RIGHT) for i, r in enumerate(rows)])
    heads = VGroup()
    cells = VGroup()
    for j, (nm, cust) in enumerate(cols):
        x = -1.6 + 2.15 * j
        heads.add(T(nm, size=24, color=th.INK, weight="BOLD").move_to([x, 2.35, 0]))
        col = VGroup()
        for i in range(8):
            c_ = th.AMBER if i in cust else th.SKY
            col.add(Rectangle(width=2.0, height=0.44, stroke_width=0, fill_color=c_, fill_opacity=0.55).move_to([x, 1.75 - 0.5 * i, 0]))
        cells.add(col)
    for l_ in labels:
        l_.align_to(np.array([-2.75, 0, 0]), RIGHT)
    g.add(labels, heads, cells)
    g.cells = cells
    return g


class Lesson(Lesson):
    SUBJECT = "cs"
    GRADE = 12
    UNIT = 7
    TITLE = "Recent Trends in Technology"
    SUBTITLE = "AI, cloud, big data, VR, e-services, mobile and IoT"
    SECTIONS = ["AI and robotics", "Cloud computing", "Big data", "Virtual reality", "e-commerce, e-medicine, e-governance", "Mobile computing and IoT"]
    NEXT = "Class 12 Computer Science, complete"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        chain = VGroup(*[C.node(t_, c_, w=2.3, h=1.05, size=22) for t_, c_ in [("soil sensor", th.MINT), ("gateway", th.SKY), ("cloud", th.SKY), ("AI model", th.PINK), ("farmer's app", th.AMBER)]]).arrange(RIGHT, buff=0.45).move_to([0, 0.9, 0])
        ar = VGroup(*[Arrow(chain[k].get_right(), chain[k + 1].get_left(), buff=0.04, color=th.MUTED, stroke_width=4, max_tip_length_to_length_ratio=0.3) for k in range(4)])
        dot = Dot(color=th.AMBER, radius=0.1).move_to(chain[0])
        tags = VGroup(*[T(t_, size=22, color=th.MUTED).next_to(chain[k], DOWN, buff=0.25) for k, t_ in enumerate(["IoT", "mobile", "cloud", "AI", "e-service"])])
        q = T("A field in Jhapa is dry. Ten seconds later, a pump switches on.", size=28, color=th.INK).move_to([0, -1.8, 0])
        with self.say("A soil sensor in a field in Jhapa notices the ground is dry. Its reading hops over the mobile network to a server in a data centre, a trained model decides the crop needs water, and the farmer's phone switches the pump on. Ten seconds, no human in the loop."):
            self.play(LaggedStart(*[FadeIn(c_) for c_ in chain], lag_ratio=0.15), LaggedStart(*[GrowArrow(a_) for a_ in ar], lag_ratio=0.15))
            self.play(FadeIn(dot))
            for k in range(1, 5):
                self.play(dot.animate.move_to(chain[k]), run_time=0.5)
            self.play(Indicate(chain[4], color=th.AMBER), FadeIn(q))
        with self.say("That one moment uses almost every topic in this unit: the internet of things, mobile computing, cloud computing and artificial intelligence."):
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tags], lag_ratio=0.2))
            nb = C.neby_in(self, "surprised", height=1.3)
        C.neby_out(self, nb)
        self.play(FadeOut(VGroup(chain, ar, dot, tags, q)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Computer Science, Unit 7: Recent Trends in Technology. Numbers in this unit date fast, so whenever you quote one in the exam, quote its year too."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Six parts. Artificial intelligence and robotics. Cloud computing. Big data. Virtual reality. e-commerce, e-medicine and e-governance. And mobile computing with the internet of things.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = C.head(self, "AI is the field; the newest systems sit deep inside it")
        specs = [("Artificial intelligence (1956)", "search, planning, expert systems, robotics", th.SKY, 7.2, 5.0), ("Machine learning (1980s)", "learns patterns from data: spam filters", th.MINT, 6.2, 3.8),
                 ("Deep learning (2012)", "neural networks: faces, speech", th.AMBER, 5.2, 2.6), ("Generative AI (2017)", "LLMs: new text, code, images", th.CORAL, 4.2, 1.4)]
        boxes = VGroup()
        for k, (nm, eg, c_, w, hh) in enumerate(specs):
            r = RoundedRectangle(corner_radius=0.15, width=w, height=hh, stroke_color=c_, stroke_width=3, fill_color=c_, fill_opacity=0.07).move_to([-3.0, -0.75 + 0.0 * k - (5.0 - hh) / 2 * 0.0, 0])
            r.align_to(np.array([0, -3.1, 0]), DOWN)
            lab = VGroup(T(nm, size=22, color=c_, weight="BOLD"), T(eg, size=22, color=th.MUTED)).arrange(DOWN, buff=0.06).move_to(r.get_top() + DOWN * 0.42)
            if k == 3:
                lab.move_to(r)
            boxes.add(VGroup(r, lab))
        for b_ in boxes:
            b_[1].scale_to_fit_width(min(b_[1].width, b_[0].width - 0.3))
        miles = VGroup(*[VGroup(T(y_, size=24, color=th.AMBER, weight="BOLD"), T(e_, size=24, color=th.INK)).arrange(RIGHT, buff=0.3) for y_, e_ in [("1956", "Dartmouth: the term AI"), ("1997", "Deep Blue beats Kasparov"), ("2016", "AlphaGo beats Lee Sedol"), ("2017", "the transformer"), ("2022", "ChatGPT")]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, -0.4, 0])
        with self.say("Artificial intelligence is building machines that do jobs which would need human intelligence: learning, reasoning, understanding language, recognising patterns. Inside it sits machine learning, which learns patterns from data instead of following hand written rules. Inside that, deep learning, with many layered neural networks. And inside that, the newest layer: generative AI, the large language models behind ChatGPT, which create new text, code and pictures."):
            self.play(FadeIn(h))
            for b_ in boxes:
                self.play(FadeIn(b_), run_time=0.6)
        with self.say("A few dates worth knowing. The term was coined at Dartmouth in nineteen fifty six. Deep Blue beat Kasparov at chess in ninety seven, AlphaGo won at Go in twenty sixteen, the transformer was published in twenty seventeen, and ChatGPT arrived in November twenty twenty two."):
            self.play(LaggedStart(*[FadeIn(m_, shift=RIGHT * 0.2) for m_ in miles], lag_ratio=0.35))
        self.play(FadeOut(VGroup(h, boxes, miles)))
        h = C.head(self, "Narrow, general, super")
        cards = VGroup()
        for t_, d_, c_ in [("Narrow AI (ANI)", "good at ONE task. Every real system today: Google Translate, face unlock, ChatGPT", th.MINT), ("General AI (AGI)", "human-level across all tasks. Does not exist yet", th.AMBER), ("Super AI", "beyond human ability. Hypothetical", th.CORAL)]:
            box = RoundedRectangle(corner_radius=0.15, width=3.9, height=3.2, stroke_color=c_, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
            cards.add(VGroup(box, VGroup(T(t_, size=26, color=c_, weight="BOLD"), para(d_, width=3.4, size=24, color=th.BODY)).arrange(DOWN, buff=0.3).move_to(box)))
        cards.arrange(RIGHT, buff=0.35).move_to([0, 0.1, 0])
        br = T("branches: machine learning, NLP, computer vision, expert systems, speech, robotics", size=24, color=th.MUTED).move_to([0, -2.4, 0])
        br.scale_to_fit_width(min(br.width, 12.4))
        with self.say("By capability, AI is narrow, general or super. Narrow AI does one task well, and every system in use today is narrow, however clever it looks. General AI, human level at everything, does not yet exist; super AI is hypothetical."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cards], lag_ratio=0.35))
            self.play(FadeIn(br))
        self.play(FadeOut(VGroup(h, cards, br)))
        h = C.head(self, "A robot senses, decides and acts")
        blocks = VGroup(*[C.node(t_, c_, w=2.75, h=1.4, size=24) for t_, c_ in [("Sensors\ncamera, touch", th.SKY), ("Controller\nprogram / AI", th.AMBER), ("Actuators\nmotors", th.SKY), ("End effector\ngripper, wheels", th.SKY)]]).arrange(RIGHT, buff=0.4).move_to([0, 1.0, 0])
        ar = VGroup(*[Arrow(blocks[k].get_right(), blocks[k + 1].get_left(), buff=0.04, color=th.MUTED, stroke_width=4, max_tip_length_to_length_ratio=0.3) for k in range(3)])
        fb = VGroup(Line(blocks[3].get_bottom(), blocks[3].get_bottom() + DOWN * 0.7, color=th.CORAL, stroke_width=4), Line(blocks[3].get_bottom() + DOWN * 0.7, blocks[0].get_bottom() + DOWN * 0.7, color=th.CORAL, stroke_width=4),
                    Arrow(blocks[0].get_bottom() + DOWN * 0.7, blocks[0].get_bottom(), buff=0, color=th.CORAL, stroke_width=4, max_tip_length_to_length_ratio=0.4))
        fbl = T("feedback: the sensors see the effect of the action", size=24, color=th.CORAL).next_to(fb[1], DOWN, buff=0.15)
        nt = T("robot: Čapek's play R.U.R., 1920  ·  first industrial robot Unimate, 1961", size=22, color=th.MUTED).move_to([0, -2.7, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("Robotics designs, builds and programs robots: machines that sense their surroundings, process what they sense, and act on the physical world. Sensors feed the controller; the controller's program decides; actuators, the motors, move the end effector, the gripper or wheels. And the sensors then see the result, closing the feedback loop."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(b_) for b_ in blocks], lag_ratio=0.25), LaggedStart(*[GrowArrow(a_) for a_ in ar], lag_ratio=0.25))
            self.play(Create(fb), FadeIn(fbl))
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, blocks, ar, fb, fbl, nt)))
        rows = [["robot type", "where", "example"], ["industrial arm", "welding, painting, assembly", "car factories"], ["mobile / AGV", "moving goods", "warehouse robots"], ["humanoid / service", "reception, hospitality", "a robot waiter in Kathmandu (2018)"],
                ["medical", "minimally invasive surgery", "da Vinci system"], ["drone (UAV)", "survey, mapping, farming", "mapping after the 2015 earthquake"], ["exploration", "where humans can't go", "Mars rovers"]]
        tb = C.table(rows, [3.4, 4.0, 5.0], row_h=0.58, size=24, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.5, 0])
        pc = VGroup(T("+ tireless, fast, safe in danger, consistent", size=24, color=th.MINT), T("− costly, jobs lost, no common sense, biased data → biased results", size=24, color=th.CORAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        pc.scale_to_fit_width(min(pc.width, 12.2)).move_to([0, -2.65, 0])
        with self.say("Robots by type: industrial arms, mobile warehouse robots, service robots like the robot waiter a Kathmandu startup built, surgical robots, drones that mapped the damage after the twenty fifteen earthquake, and explorers like the Mars rovers. AI and robots work without tiring, fast and safely in danger. But they cost a lot, displace jobs, lack common sense, and a model trained on biased data gives biased answers.") as v:
            C.reveal_table(self, tb, v.dur * 0.6)
            self.play(FadeIn(pc))
        self.play(FadeOut(VGroup(tb, pc)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = C.head(self, "Cloud computing: rent it, don't buy it")
        df = para("Computing services — servers, storage, databases, software — delivered over the internet on demand, paying only for what you use. The provider owns the hardware.", width=11.6, size=26, color=th.INK).move_to([0, 1.6, 0])
        ch = C.bullets(["on-demand self-service", "broad network access", "resource pooling (many tenants share one machine)", "rapid elasticity: grow or shrink in minutes", "measured service: pay per use"], width=8.0, size=24).move_to([-1.6, -1.1, 0])
        vz = para("underneath: virtualisation — one physical server split into many virtual machines", width=3.8, size=24, color=th.AMBER).move_to([4.6, -1.1, 0])
        with self.say("Cloud computing delivers computing services over the internet, on demand, and you pay only for what you use. The provider owns and maintains the hardware; you rent capacity. The official NIST definition lists five characteristics: self service on demand, access over the network, pooled resources shared by many customers, elasticity, and metered pay per use. The trick underneath is virtualisation."):
            self.play(FadeIn(h), FadeIn(df))
            C.reveal_list(self, ch, 4.0)
            self.play(FadeIn(vz))
        self.play(FadeOut(VGroup(h, df, ch, vz)))
        h = C.head(self, "IaaS, PaaS, SaaS: who manages what")
        g = stack_grid().move_to([0.4, -0.35, 0])
        key = VGroup(VGroup(Square(0.3, stroke_width=0, fill_color=th.AMBER, fill_opacity=0.6), T("you manage", size=22, color=th.INK)).arrange(RIGHT, buff=0.15), VGroup(Square(0.3, stroke_width=0, fill_color=th.SKY, fill_opacity=0.6), T("provider manages", size=22, color=th.INK)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.6).move_to([0.4, -3.1, 0])
        with self.say("The three service models differ in how much of the stack you still manage. On your own premises, you manage everything, down to the network cables. Infrastructure as a service rents you virtual machines: you still install the operating system and software. Platform as a service gives a ready platform: you bring only your application and data. Software as a service, like Gmail, gives finished software: you manage nothing but your own data."):
            self.play(FadeIn(h), FadeIn(g[0]), FadeIn(key))
            for j in range(4):
                self.play(FadeIn(g[1][j]), LaggedStart(*[FadeIn(c_) for c_ in g.cells[j]], lag_ratio=0.06), run_time=0.9)
        self.play(FadeOut(VGroup(h, g, key)))
        rows = [["model", "you rent", "examples"], ["IaaS", "virtual machines, storage, network", "AWS EC2, Azure VMs"], ["PaaS", "a platform to deploy code on", "Google App Engine, Heroku"], ["SaaS", "finished software in a browser", "Gmail, Google Docs, Zoom"]]
        tb = C.table(rows, [2.0, 5.6, 4.8], row_h=0.66, size=24, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 1.4, 0])
        deps = VGroup(*[VGroup(T(t_, size=26, color=c_, weight="BOLD"), T(d_, size=22, color=th.BODY)).arrange(DOWN, buff=0.1) for t_, d_, c_ in [("public", "open to anyone", th.SKY), ("private", "one organisation", th.MINT), ("community", "shared by a group", th.AMBER), ("hybrid", "a mix of these", th.PINK)]]).arrange(RIGHT, buff=0.9).move_to([0, -1.5, 0])
        dl = T("deployment models", size=24, color=th.MUTED).next_to(deps, UP, buff=0.3)
        with self.say("Examples to quote. Infrastructure: Amazon EC2. Platform: Google App Engine. Software: Gmail and Google Docs. And by who may use it, a cloud is public, private to one organisation, shared by a community, or a hybrid.") as v:
            C.reveal_table(self, tb, v.dur * 0.5)
            self.play(FadeIn(dl), LaggedStart(*[FadeIn(d_) for d_ in deps], lag_ratio=0.25))
        self.play(FadeOut(VGroup(tb, deps, dl)))
        C.worked(self, "A college server costs Rs 4,50,000 (life 5 years), draws 300 W all the time at Rs 11 per unit, plus Rs 2,000 a month of admin time. A cloud server costs Rs 9,000 a month. Compare.",
                 [r"\text{hardware: } \tfrac{4{,}50{,}000}{60} = \text{Rs } 7{,}500 \text{ a month}", r"\text{power: } 0.3 \times 24 \times 30 = 216 \text{ kWh} \times 11 = \text{Rs } 2{,}376", r"\text{own server} = 7{,}500 + 2{,}376 + 2{,}000 = \text{Rs } 11{,}876",
                  r"\text{cloud saves } 11{,}876 - 9{,}000 = \text{Rs } 2{,}876 \text{ a month} \approx \text{Rs } 34{,}512 \text{ a year}"],
                 ["Cloud or your own server?", "Spread the hardware over sixty months: seven thousand five hundred a month.", "Three hundred watts all month is two hundred and sixteen units: two thousand three hundred and seventy six rupees.", "With the admin's time, eleven thousand eight hundred and seventy six a month.",
                  "So the cloud saves about two thousand nine hundred a month, thirty four and a half thousand a year, before counting the UPS and load shedding."])
        h = C.head(self, "The price of the cloud")
        cons = C.bullets(["useless without a reliable internet link", "a bill that never ends", "your data may sit under another country's law", "vendor lock-in: moving away is expensive", "the provider's outage is your outage"], width=11, size=26, color=th.CORAL).move_to([0, 0.3, 0])
        ms = T("2025 market: AWS ~30 %, Azure ~22 %, Google Cloud ~12 %", size=24, color=th.MUTED).move_to([0, -2.6, 0])
        with self.say("The costs: no internet, no service. The bill never ends. Your data may physically sit in another country, under its laws. Vendor lock in makes leaving expensive. And when the provider goes down, so do you. As of twenty twenty five, Amazon held about thirty per cent of the market, Microsoft twenty two and Google twelve."):
            self.play(FadeIn(h))
            C.reveal_list(self, cons, 5.0)
            self.play(FadeIn(ms))
        self.play(FadeOut(VGroup(h, cons, ms)))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        rows = [["V", "meaning", "example"], ["volume", "sheer quantity: terabytes to zettabytes", "a telecom's call records"], ["velocity", "speed at which data arrives", "Fonepay transactions, sensors"], ["variety", "structured + semi- + unstructured", "tables, JSON, photos, voice"],
                ["veracity", "how much is noisy or wrong", "typed addresses, GPS drift"], ["value", "the useful insight", "where to add buses"]]
        tb = C.table(rows, [2.4, 5.6, 4.6], row_h=0.62, size=24, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.9, 0])
        df = para("Big data: data so large, fast or varied that ordinary database tools cannot capture, store and analyse it in acceptable time.", width=11.6, size=24, color=th.SKY).move_to([0, -2.4, 0])
        with self.say("Big data is data so large, so fast, or so varied that ordinary database tools cannot handle it in time. The standard answer is the five Vs. Volume, the sheer quantity. Velocity, the speed it arrives. Variety, tables mixed with logs, photos and voice. Veracity, how much of it is wrong. And value, the insight you can extract.") as v:
            C.reveal_table(self, tb, v.dur * 0.7)
            self.play(FadeIn(df))
        self.play(FadeOut(VGroup(tb, df)))
        h = C.head(self, "Data created worldwide, in zettabytes")
        yrs = ["2015", "2018", "2020", "2022", "2025", "2028*"]
        vol = [15.5, 33, 64.2, 101, 181, 394]
        ax = Axes(x_range=[-0.5, 5.5, 1], y_range=[0, 400, 100], x_length=8.4, y_length=4.6, tips=False, axis_config={"color": th.MUTED, "stroke_width": 2}).move_to([-1.5, -0.4, 0])
        bars = VGroup(*[Rectangle(width=0.9, height=ax.c2p(0, v_)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=th.AMBER if k == 5 else th.SKY, fill_opacity=0.8).move_to(ax.c2p(k, 0), aligned_edge=DOWN) for k, v_ in enumerate(vol)])
        xl = VGroup(*[T(y_, size=22, color=th.MUTED).next_to(ax.c2p(k, 0), DOWN, buff=0.2) for k, y_ in enumerate(yrs)])
        vl = VGroup(*[T(f"{v_:g}", size=22, color=th.INK).next_to(b_, UP, buff=0.08) for v_, b_ in zip(vol, bars)])
        zb = VGroup(T("1 ZB = 10²¹ bytes", size=24, color=th.AMBER), T("* forecast", size=22, color=th.MUTED), T("tools: Hadoop, Spark, NoSQL", size=24, color=th.MINT)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        zb.scale_to_fit_width(min(zb.width, 3.5)).move_to([4.95, 0.6, 0])
        with self.say("How big? Estimates put the data created in twenty twenty five at around a hundred and eighty zettabytes, nearly three times twenty twenty, roughly doubling every two to three years. One zettabyte is ten to the twenty one bytes. No single server copes, so big data runs on distributed tools: Hadoop, Spark, and NoSQL databases such as MongoDB."):
            self.play(FadeIn(h), Create(ax), FadeIn(xl))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.2), LaggedStart(*[FadeIn(v_) for v_ in vl], lag_ratio=0.2), run_time=2.5)
            self.play(FadeIn(zb))
        self.play(FadeOut(VGroup(h, ax, bars, xl, vl, zb)))
        C.worked(self, "A flood-warning network has 2,000 sensors; each sends an 80-byte reading every 5 seconds. Data per day and per year? Which Vs are present?",
                 [r"\text{readings per sensor per day} = \tfrac{86\,400}{5} = 17\,280", r"2\,000 \times 17\,280 \times 80 = 2.76 \times 10^{9} \text{ B} \approx 2.76 \text{ GB a day}", r"\times 365 \approx 1.01 \times 10^{12} \text{ B} \approx 1 \text{ TB a year}",
                  r"\text{velocity: } 400 \text{ readings every second} \Rightarrow \text{big data}"],
                 ["Is it big data?", "Seventeen thousand two hundred and eighty readings per sensor per day.", "Times two thousand sensors, times eighty bytes: about two point seven six gigabytes a day.", "About one terabyte a year. Volume alone, an ordinary database could store.",
                  "But four hundred readings arrive every second, and a flood warning computed tomorrow is useless. Velocity, plus variety and veracity, make it a genuine big data problem."])

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = C.head(self, "Virtual reality: a loop that must run in under 20 ms")
        c0 = np.array([-3.2, -0.4, 0])
        nodes = VGroup(*[C.node(t_, c_, w=2.6, h=1.05, size=24).move_to(c0 + p_) for t_, c_, p_ in [("user\nhead, hands", th.INK, UP * 1.95), ("tracking\nsensors", th.SKY, RIGHT * 2.2), ("graphics\nengine", th.AMBER, DOWN * 1.95), ("headset\ndisplay", th.MINT, LEFT * 2.2)]])
        ar = VGroup(*[CurvedArrow(nodes[k].get_center() + (nodes[(k + 1) % 4].get_center() - nodes[k].get_center()) * 0.38, nodes[(k + 1) % 4].get_center() - (nodes[(k + 1) % 4].get_center() - nodes[k].get_center()) * 0.38, angle=-PI / 3, color=th.MUTED, stroke_width=3) for k in range(4)])
        ms = T("< 20 ms", size=28, color=th.CORAL, weight="BOLD").move_to(c0)
        txt = para("A computer-generated 3-D world that replaces what you see and hear, giving a sense of presence. Two images, one per eye, redrawn about 90 times a second; if they lag the head, you feel sick.", width=4.8, size=24, color=th.BODY).move_to([3.9, 0.3, 0])
        with self.say("Virtual reality is a computer generated three dimensional world that replaces what you see and hear, so you feel present inside it. It is a loop. Sensors track your head and hands; the engine draws two images, one per eye, for depth; the headset displays them; you move again. The loop must close in under about twenty milliseconds, ninety times a second, or the user feels sick."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(n_) for n_ in nodes], lag_ratio=0.2))
            self.play(LaggedStart(*[Create(a_) for a_ in ar], lag_ratio=0.25), FadeIn(ms))
            self.play(FadeIn(txt))
        self.play(FadeOut(VGroup(h, nodes, ar, ms, txt)))
        h = C.head(self, "From the real world to fully virtual")
        line = Arrow([-6.0, 1.2, 0], [6.0, 1.2, 0], buff=0, color=th.MUTED, stroke_width=4)
        marks = VGroup(*[VGroup(Dot([x, 1.2, 0], color=c_, radius=0.12), T(t_, size=28, color=c_, weight="BOLD").move_to([x, 1.75, 0]), para(d_, width=2.7, size=22, color=th.BODY).move_to([x, 0.15, 0])) for x, t_, d_, c_ in [(-4.8, "Real", "no computer content", th.INK), (-1.6, "AR", "adds objects to the real view (Pokémon GO)", th.SKY), (1.6, "MR", "virtual objects anchored to real ones", th.AMBER), (4.8, "VR", "replaces the world (Meta Quest, Vision Pro)", th.MINT)]])
        ty = T("VR: non-immersive (screen)  ·  semi-immersive (big projection)  ·  fully immersive (headset)", size=24, color=th.MUTED).move_to([0, -2.0, 0])
        ty.scale_to_fit_width(min(ty.width, 12.4))
        with self.say("Place the technologies on a line. The plain real world. Augmented reality adds computer objects to your real view, like Pokémon Go. Mixed reality anchors virtual objects to real ones. Virtual reality replaces the world altogether. VR itself is non immersive on an ordinary screen, semi immersive on a big projection, or fully immersive in a tracked headset."):
            self.play(FadeIn(h), GrowArrow(line))
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.3))
            self.play(FadeIn(ty))
        self.play(FadeOut(VGroup(h, line, marks, ty)))
        rows = [["field", "use of VR"], ["education", "virtual labs and field trips"], ["medicine", "surgical training, phobia therapy, rehab"], ["engineering", "walk through a building before it is built"], ["aviation, military", "simulators: failure is cheap"], ["heritage, tourism", "a virtual walk through Kathmandu Durbar Square"]]
        tb = C.table(rows, [3.6, 8.4], row_h=0.6, size=24, colors=[th.AMBER, th.INK]).move_to([0, 0.7, 0])
        pc = T("− costly hardware, motion sickness, eye strain, costly content", size=24, color=th.CORAL).move_to([0, -2.4, 0])
        with self.say("Applications: virtual labs, surgical training and therapy, walking through a building before it exists, flight simulators where crashing is free, and heritage tours. The drawbacks: expensive hardware, motion sickness, eye strain, and content that is costly to make.") as v:
            C.reveal_table(self, tb, v.dur * 0.65)
            self.play(FadeIn(pc))
        self.play(FadeOut(VGroup(tb, pc)))
        C.worked(self, "A headset shows 2160 × 2160 pixels per eye, 24-bit colour, 90 frames per second. What is the uncompressed data rate?",
                 [r"\text{bits per frame} = 2 \times 2160 \times 2160 \times 24 = 2.24 \times 10^{8}", r"\text{rate} = 2.24 \times 10^{8} \times 90 = 2.02 \times 10^{10} \text{ bit/s}", r"\approx 20 \text{ Gbit/s: so render in the headset, or compress hard}"],
                 ["Why VR needs so much bandwidth.", "Two eyes, two thousand one hundred and sixty squared pixels each, twenty four bits per pixel: two point two four times ten to the eight bits per frame.", "Ninety frames a second: about twenty gigabits per second.", "No home network carries that, so the picture is drawn inside the headset or heavily compressed."])

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = C.head(self, "e-commerce models: who sells to whom")
        cells = VGroup()
        for t_, d_, e_, c_ in [("B2B", "business → business", "a wholesaler supplying shops online", th.SKY), ("B2C", "business → consumer", "an online shop like Daraz", th.MINT), ("C2C", "consumer → consumer", "selling a used bicycle on Hamrobazar", th.AMBER), ("C2B", "consumer → business", "a freelancer selling photos to a company", th.PINK)]:
            box = RoundedRectangle(corner_radius=0.15, width=5.6, height=2.0, stroke_color=c_, stroke_width=3, fill_color=th.PANEL, fill_opacity=1)
            cells.add(VGroup(box, VGroup(VGroup(T(t_, size=32, color=c_, weight="BOLD"), T(d_, size=24, color=th.INK)).arrange(RIGHT, buff=0.35), para(e_, width=5.0, size=22, color=th.MUTED)).arrange(DOWN, buff=0.2).move_to(box)))
        cells.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.3)).move_to([0, 0.15, 0])
        pay = VGroup(T("payments: eSewa, Khalti, IME Pay, connectIPS, Fonepay QR", size=24, color=th.MUTED), T("law: Electronic Transactions Act 2063 (2008)", size=24, color=th.MUTED)).arrange(DOWN, buff=0.12)
        cells.shift(UP * 0.2)
        pay.move_to([0, -2.75, 0])
        with self.say("e-commerce is buying and selling, and moving the money, over electronic networks. Its models are named by who sits at each end. Business to business: a wholesaler supplying shops. Business to consumer: an online shop like Daraz. Consumer to consumer: selling your old bicycle on Hamrobazar. Consumer to business: a freelancer selling photos to a company. In Nepal the money moves through wallets and QR payments, under the Electronic Transactions Act of twenty sixty three."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cells], lag_ratio=0.3))
            self.play(FadeIn(pay))
        self.play(FadeOut(VGroup(h, cells, pay)))
        h = C.head(self, "e-medicine: the specialist travels, the patient doesn't")
        hp = C.node("health post\nHumla", th.MINT, w=3.0, h=1.3, size=26).move_to([-4.4, 0.8, 0])
        hs = C.node("specialist\nKathmandu", th.SKY, w=3.0, h=1.3, size=26).move_to([4.4, 0.8, 0])
        links = VGroup(*[Arrow(hp.get_right() + UP * 0.3 * (1 - 2 * k), hs.get_left() + UP * 0.3 * (1 - 2 * k), buff=0.1, color=c_, stroke_width=4) for k, c_ in enumerate([th.AMBER, th.MINT])])
        links[1].rotate(PI)
        ll = VGroup(T("X-ray, ECG, video call", size=24, color=th.AMBER).next_to(links[0], UP, buff=0.1), T("diagnosis, advice", size=24, color=th.MINT).next_to(links[1], DOWN, buff=0.1))
        lim = para("limits: no physical examination, needs bandwidth and power, patient privacy, and who is responsible for a remote diagnosis?", width=10.5, size=26, color=th.CORAL).move_to([0, -1.6, 0])
        with self.say("e-medicine, or telemedicine, delivers health care at a distance: video consultation, X rays and ECGs sent to a specialist, wearable monitors, electronic records. For Nepal the argument is geography: a Kathmandu specialist can advise a health post in Humla in minutes instead of a two day journey. Its limits: no physical examination, it needs bandwidth and power, and patient privacy and responsibility are hard questions."):
            self.play(FadeIn(h), FadeIn(hp), FadeIn(hs))
            self.play(GrowArrow(links[0]), FadeIn(ll[0]))
            self.play(GrowArrow(links[1]), FadeIn(ll[1]))
            self.play(FadeIn(lim))
        self.play(FadeOut(VGroup(h, hp, hs, links, ll, lim)))
        rows = [["type", "between", "Nepali example"], ["G2C", "government → citizen", "online passport form, Nagarik App"], ["G2B", "government → business", "company registration, VAT filing"], ["G2G", "office ↔ office", "national ID database shared by ministries"], ["G2E", "government → employee", "payroll, transfers, records"]]
        tb = C.table(rows, [1.8, 4.2, 6.4], row_h=0.66, size=24, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.8, 0])
        nt = VGroup(T("Digital Nepal Framework (2019)", size=24, color=th.MUTED), T("+ transparency, fewer office visits     − digital divide, cyber-security", size=24, color=th.INK)).arrange(DOWN, buff=0.12).move_to([0, -2.45, 0])
        with self.say("e-governance is government using ICT to serve citizens, businesses and its own offices. Four types: government to citizen, like the Nagarik App; government to business, like online VAT filing; government to government, like a shared national ID database; and government to employee. It brings transparency and fewer queues, but faces the digital divide and cyber security risks.") as v:
            C.reveal_table(self, tb, v.dur * 0.65)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = C.head(self, "Mobile generations (log scale)")
        gens = [("1G", "1980s", 0.0024, "2.4 kbps voice"), ("2G", "1991", 0.064, "64 kbps SMS"), ("3G", "2001", 2.0, "2 Mbps internet"), ("4G", "2009", 100.0, "100 Mbps video"), ("5G", "2019", 10000.0, "10 Gbps")]
        base = -2.3
        bars = VGroup()
        for k, (g_, y_, r_, d_) in enumerate(gens):
            hh = (np.log10(r_) + 3) * 0.55
            x = -5.6 + 1.95 * k
            b_ = Rectangle(width=1.2, height=hh, stroke_width=0, fill_color=th.CORAL if k == 4 else th.SKY, fill_opacity=0.8).move_to([x, base, 0], aligned_edge=DOWN)
            bars.add(VGroup(b_, T(f"{g_}  {y_}", size=22, color=th.INK).next_to(b_, DOWN, buff=0.15), T(d_, size=22, color=th.MUTED).next_to(b_, UP, buff=0.1)))
        mc = para("mobile computing = mobile hardware + mobile software + wireless communication, with handover between cells as you move", width=3.6, size=24, color=th.AMBER).move_to([5.0, -0.2, 0])
        with self.say("Mobile computing lets the user, the device and the connection all move. It needs mobile hardware, mobile software and wireless communication. Each network generation was ten to a hundred times faster than the last: analogue voice in the eighties, SMS on 2G, mobile internet on 3G, video on 4G, and about ten gigabits per second on 5G."):
            self.play(FadeIn(h))
            for b_ in bars:
                self.play(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[2]), run_time=0.6)
            self.play(FadeIn(mc))
        self.play(FadeOut(VGroup(h, bars, mc)))
        C.worked(self, "A 3.5 GB video is downloaded on 4G at 20 Mbit/s and on 5G at 200 Mbit/s. Find both times (1 GB = 1000 MB, 1 byte = 8 bits).",
                 [r"3.5 \times 1000 \times 8 = 28\,000 \text{ megabits}", r"\text{4G: } \tfrac{28\,000}{20} = 1\,400 \text{ s} = 23 \text{ min } 20 \text{ s}", r"\text{5G: } \tfrac{28\,000}{200} = 140 \text{ s} = 2 \text{ min } 20 \text{ s}",
                  r"\text{latency matters more: about 50 ms (4G) vs 5 ms (5G)}"],
                 ["How much faster is 5G?", "First convert to bits: twenty eight thousand megabits.", "On 4G: fourteen hundred seconds, twenty three minutes twenty.", "On 5G: one hundred and forty seconds, ten times faster.", "For live uses like remote surgery, the drop in delay from fifty to five milliseconds matters even more."])
        h = C.head(self, "Internet of Things: four layers")
        lay = VGroup(*[VGroup(C.node(t_, c_, w=3.6, h=0.9, size=24), T(e_, size=24, color=th.BODY)).arrange(RIGHT, buff=0.5) for t_, e_, c_ in [("application", "farmer's app: pump ON", th.PINK), ("processing", "cloud decides: soil too dry", th.AMBER), ("network", "gateway → Wi-Fi / LoRaWAN / 4G", th.SKY), ("perception", "soil-moisture sensor", th.MINT)]]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-0.4, 0.3, 0])
        nt = T("coined by Kevin Ashton, 1999  ·  protocols: MQTT, Zigbee, BLE, LoRaWAN  ·  weakest point: security", size=22, color=th.MUTED).move_to([0, -2.6, 0])
        nt.scale_to_fit_width(min(nt.width, 12.4))
        with self.say("The internet of things, a phrase Kevin Ashton coined in nineteen ninety nine, connects physical objects fitted with sensors and software so they exchange data and can be controlled remotely. It has four layers. Perception: the sensors. Network: the gateway and the link. Processing: the cloud that decides. Application: the app the farmer sees. Its weakest point is security: cheap devices shipped with default passwords have been hijacked into botnets."):
            self.play(FadeIn(h))
            for l_ in reversed(lay):
                self.play(FadeIn(l_, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(h, lay, nt)))
        C.worked(self, "IPv4 addresses are 32 bits, IPv6 addresses 128 bits. About 20 billion IoT devices were online in 2025. Compare with the IPv4 space.",
                 [r"\text{IPv4: } 2^{32} \approx 4.29 \times 10^{9}", r"\text{IPv6: } 2^{128} \approx 3.4 \times 10^{38}", r"\tfrac{2.0 \times 10^{10}}{4.29 \times 10^{9}} \approx 4.7 \text{ times the whole IPv4 space}"],
                 ["Why IoT needs IPv6.", "IPv4 gives about four point three billion addresses.", "IPv6 gives three point four times ten to the thirty eight.", "IoT devices alone would need four point seven times all of IPv4. With IPv6, the shortage simply disappears."])
        self.quiz("Gmail is an example of which cloud service model?",
                  ["IaaS", "PaaS", "SaaS", "on-premises"], 2,
                  "Pause and think.",
                  "Software as a service: finished software in a browser, and you manage only your data.")
        self.quiz("Which of these is NOT one of the five Vs of big data?",
                  ["volume", "velocity", "virtualisation", "veracity"], 2,
                  "One more.",
                  "Virtualisation. It is the technology under cloud computing, not a V of big data.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "AI contains machine learning, which contains deep learning, then generative AI; all real AI is narrow.",
            "Robot: sensors → controller → actuators → end effector, with feedback.",
            "Cloud: IaaS, PaaS, SaaS; public, private, community, hybrid; pay per use.",
            "Big data: volume, velocity, variety, veracity, value; Hadoop, Spark, NoSQL.",
            "VR replaces the world, AR adds to it; e-commerce B2B/B2C/C2C/C2B; e-gov G2C/G2B/G2G/G2E.",
            "IoT layers: perception, network, processing, application; needs IPv6.",
        ], "Quick recap. AI and its nested layers, and robots that sense, decide and act. Cloud service and deployment models. The five Vs of big data. Virtual and augmented reality. The e-commerce and e-governance models. And the four layers of the internet of things.")
        self.outro("And that completes Class 12 Computer Science. Well done for making it through all seven units. See you in the next subject.")
