import os
import sys

from manim import *
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Lesson, M, T, para, th  # noqa: E402
import _cs as C  # noqa: E402


def pc(label, color=th.SKY, w=1.1, h=0.6, size=20):
    return C.node(label, color, w=w, h=h, size=size)


class Lesson(Lesson):
    SUBJECT = "cs"
    GRADE = 12
    UNIT = 2
    TITLE = "Data Communication and Networking"
    SUBTITLE = "How computers talk to each other"
    SECTIONS = ["The communication system", "Signals, modes and media", "Impairments", "Networks, architectures and devices", "Topologies", "The OSI model", "IP addressing"]
    NEXT = "Unit 3 · Web Technology II"

    def lesson(self):
        self.parts(self.cold_open, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.ending)

    # ------------------------------------------------------------------ cold open
    def cold_open(self):
        you = pc("your phone", th.SKY, w=2.0, h=0.9, size=26).move_to([-5.6, 0, 0])
        hops = [pc(t_, th.MUTED, w=2.1, h=0.75, size=24).move_to(p_) for t_, p_ in [("Wi-Fi router", [-3.3, 1.5, 0]), ("ISP", [-1.1, -0.9, 0]), ("fibre backbone", [1.1, 1.5, 0]), ("data centre", [3.3, -0.9, 0])]]
        srv = pc("video server", th.MINT, w=2.2, h=0.9, size=26).move_to([5.5, 0.4, 0])
        chain = [you] + hops + [srv]
        links = VGroup(*[Line(a.get_center(), b.get_center(), color=th.FAINT, stroke_width=2).set_z_index(-1) for a, b in zip(chain, chain[1:])])
        cap = T("one tap → thousands of packets, a dozen devices, under a second", size=26, color=th.AMBER).move_to([0, -2.6, 0])
        with self.say("You tap play on a video. In under a second, your request leaves your phone, crosses your Wi Fi router, your internet provider, a fibre backbone and a data centre, and thousands of packets of video come streaming back."):
            self.play(FadeIn(you), *[FadeIn(h_) for h_ in hops], FadeIn(srv), Create(links))
            p = C.packet(th.AMBER).move_to(you.get_center())
            self.add(p)
            for nxt in chain[1:]:
                self.play(p.animate.move_to(nxt.get_center()), run_time=0.35)
            back = [C.packet(th.MINT).move_to(srv.get_center()) for _ in range(5)]
            self.play(LaggedStart(*[AnimationGroup(*[Succession(*[b.animate(run_time=0.25).move_to(n.get_center()) for n in reversed(chain[:-1])])]) for b in back], lag_ratio=0.15), run_time=2.5)
            self.remove(p, *back)
            self.play(FadeIn(cap))
        with self.say("Every step follows agreed rules. This unit explains the media, the devices, the layers and the addresses that make it work."):
            nb = C.neby_in(self, "surprised", height=1.3)
        C.neby_out(self, nb)
        self.play(FadeOut(VGroup(you, *hops, srv, links, cap)))
        tc, nb = self.title_card()
        with self.say("Welcome to Class 12 Computer Science, Unit 2: Data Communication and Networking."):
            pass
        self.end_title(tc, nb)
        self.roadmap("Seven parts. The communication system. Signals, transmission modes and media. Transmission impairments. Network types, architectures and devices. Topologies. The OSI reference model. And IP addressing and subnetting.")

    # ------------------------------------------------------------------ part 1
    def p1(self):
        self.section(0)
        h = C.head(self, "Five elements of data communication")
        snd = pc("sender", th.SKY, w=1.8, h=0.9, size=26).move_to([-4.6, 0.4, 0])
        rcv = pc("receiver", th.MINT, w=1.8, h=0.9, size=26).move_to([4.6, 0.4, 0])
        med = Line(snd.get_right(), rcv.get_left(), color=th.MUTED, stroke_width=6)
        msg = VGroup(RoundedRectangle(corner_radius=0.08, width=1.2, height=0.6, stroke_width=0, fill_color=th.AMBER, fill_opacity=1), T("message", size=22, color=th.BG, weight="BOLD")).move_to(snd.get_center())
        labs = VGroup(T("medium", size=28, color=th.MUTED).next_to(med, DOWN, buff=0.2), T("protocol: the agreed rules", size=26, color=th.PINK).move_to([0, 2.0, 0]))
        nt = para("Without a shared protocol, two connected devices still cannot understand each other — like two people with no common language on a working telephone.", width=11, size=28, color=th.BODY).move_to([0, -2.2, 0])
        with self.say("Every communication needs five things: a message, a sender, a receiver, a medium for it to travel through, and a protocol, the agreed set of rules. Without a shared protocol, a perfect connection is useless, like two people with no common language on a working phone line."):
            self.play(FadeIn(h), FadeIn(snd), FadeIn(rcv), Create(med), FadeIn(labs[0]))
            self.play(FadeIn(msg))
            self.play(msg.animate.next_to(rcv, LEFT, buff=0.15), run_time=1.5)
            self.play(FadeIn(labs[1]), FadeIn(nt))
        self.play(FadeOut(VGroup(h, snd, rcv, med, msg, labs, nt)))
        h = C.head(self, "The block diagram")
        names = [("source", th.SKY), ("transmitter", th.PINK), ("transmission\nsystem", th.MUTED), ("receiver", th.PINK), ("destination", th.MINT)]
        blocks = VGroup(*[pc(n_, c_, w=2.0, h=1.0, size=22) for n_, c_ in names]).arrange(RIGHT, buff=0.45).move_to([0, 1.0, 0])
        arrs = VGroup(*[Arrow(blocks[k].get_right(), blocks[k + 1].get_left(), buff=0.05, color=th.MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.3) for k in range(4)])
        noise = VGroup(Arrow(blocks[2].get_bottom() + DOWN * 1.0, blocks[2].get_bottom(), buff=0.05, color=th.CORAL, stroke_width=3), T("noise", size=26, color=th.CORAL).next_to(blocks[2].get_bottom() + DOWN * 1.0, DOWN, buff=0.05))
        ax = Axes(x_range=[0, 8, 1], y_range=[-1.6, 1.6, 1], x_length=10.0, y_length=1.4, tips=False, axis_config={"stroke_opacity": 0}).move_to([0, -2.3, 0])
        clean = ax.plot(lambda x: np.sin(2 * x), x_range=[0, 8], color=th.SKY, stroke_width=3)
        rng = np.random.default_rng(2)
        nz = rng.normal(0, 0.25, 400)
        noisy = ax.plot(lambda x: np.sin(2 * x) + nz[min(399, int(x / 8 * 399))], x_range=[0, 8, 0.02], color=th.CORAL, stroke_width=2)
        with self.say("Examiners ask for this diagram. The source produces the data; the transmitter turns it into a signal the medium can carry; the transmission system carries it, and unavoidably adds noise; the receiver turns the signal back into data; and the destination uses it."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(b_) for b_ in blocks], lag_ratio=0.15), LaggedStart(*[GrowArrow(a_) for a_ in arrs], lag_ratio=0.15))
            self.play(GrowArrow(noise[0]), FadeIn(noise[1]))
            self.play(Create(clean))
            self.play(Transform(clean, noisy))
        self.play(FadeOut(VGroup(h, blocks, arrs, noise, clean)))

    # ------------------------------------------------------------------ part 2
    def p2(self):
        self.section(1)
        h = C.head(self, "Analogue and digital signals")
        ax1 = Axes(x_range=[0, 8, 1], y_range=[-1.3, 1.3, 1], x_length=5.4, y_length=2.2, tips=False, axis_config={"color": th.MUTED}).move_to([-3.3, 0.6, 0])
        ax2 = Axes(x_range=[0, 8, 1], y_range=[-0.3, 1.3, 1], x_length=5.4, y_length=2.2, tips=False, axis_config={"color": th.MUTED}).move_to([3.3, 0.6, 0])
        an = ax1.plot(lambda x: np.sin(1.6 * x), x_range=[0, 8], color=th.SKY, stroke_width=4)
        bits = [1, 0, 1, 1, 0, 0, 1, 0]
        pts = []
        for k, b in enumerate(bits):
            pts += [ax2.c2p(k, b), ax2.c2p(k + 1, b)]
        dg = VMobject(stroke_color=th.MINT, stroke_width=4).set_points_as_corners(pts)
        bl = VGroup(*[T(str(b), size=24, color=th.MINT).move_to(ax2.c2p(k + 0.5, 1.2)) for k, b in enumerate(bits)])
        labs = VGroup(T("analogue: continuous", size=28, color=th.SKY).next_to(ax1, DOWN, buff=0.2), T("digital: discrete 0s and 1s", size=28, color=th.MINT).next_to(ax2, DOWN, buff=0.2))
        tm = VGroup(T("bandwidth: range of frequencies (Hz) or max bit rate (bps)", size=26), T("bit rate = baud rate × bits per signal change", size=26, color=th.AMBER)).arrange(DOWN, buff=0.2).move_to([0, -2.4, 0])
        with self.say("A signal represents data physically. An analogue signal varies continuously, like a voice. A digital signal jumps between levels for nought and one. Noise on an analogue signal piles up for good, while a digital signal can be regenerated perfectly."):
            self.play(FadeIn(h), Create(ax1), Create(ax2), Create(an), Create(dg), FadeIn(bl), FadeIn(labs))
        with self.say("Bandwidth is how much a channel can carry. Bit rate counts bits per second; baud rate counts signal changes per second. If each change carries several bits, the bit rate is the baud rate times the bits per change."):
            self.play(FadeIn(tm))
        self.play(FadeOut(VGroup(h, ax1, ax2, an, dg, bl, labs, tm)))
        h = C.head(self, "Simplex, half duplex, full duplex")
        rows = VGroup()
        specs = [("simplex", "one way only: TV broadcast, keyboard → CPU", [1]), ("half duplex", "both ways, one at a time: walkie-talkie", [1, -1]), ("full duplex", "both ways at once: telephone, switched Ethernet", [0])]
        for k, (nm, ex, mode) in enumerate(specs):
            y = 1.4 - k * 1.6
            a, b = pc("A", th.SKY, w=0.9).move_to([-5.6, y, 0]), pc("B", th.MINT, w=0.9).move_to([-1.6, y, 0])
            rows.add(VGroup(a, b, Line(a.get_right(), b.get_left(), color=th.FAINT), T(nm, size=28, color=th.AMBER, weight="BOLD").move_to([1.4, y + 0.28, 0]), para(ex, width=5.2, size=24, color=th.BODY).move_to([3.4, y - 0.32, 0])))
        for r in rows:
            r[4].align_to(r[3], LEFT)
        with self.say("Transmission modes. Simplex goes one way only, like television. Half duplex goes both ways, but one at a time, like a walkie talkie: say over. Full duplex goes both ways at once, like a phone call."):
            self.play(FadeIn(h), FadeIn(rows))
            a, b = rows[0][0], rows[0][1]
            p1 = C.packet(th.AMBER).move_to(a.get_center())
            self.play(p1.animate.move_to(b.get_center()), run_time=0.9)
            a, b = rows[1][0], rows[1][1]
            p2 = C.packet(th.AMBER).move_to(a.get_center())
            self.play(p2.animate.move_to(b.get_center()), run_time=0.8)
            self.play(p2.animate.move_to(a.get_center()), run_time=0.8)
            a, b = rows[2][0], rows[2][1]
            p3, p4 = C.packet(th.AMBER).move_to(a.get_center() + UP * 0.12), C.packet(th.MINT).move_to(b.get_center() + DOWN * 0.12)
            self.play(p3.animate.move_to(b.get_center() + UP * 0.12), p4.animate.move_to(a.get_center() + DOWN * 0.12), run_time=1.0)
        self.play(FadeOut(VGroup(h, rows, p1, p2, p3, p4)))
        h = C.head(self, "Guided media")
        tp = VGroup(*[ParametricFunction(lambda t, s=s: np.array([t, 0.18 * np.sin(4 * t + s), 0]), t_range=[-2.2, 2.2], color=c_, stroke_width=5) for s, c_ in ((0, th.AMBER), (PI, th.SKY))]).move_to([-3.6, 1.6, 0])
        coax = VGroup(*[Circle(radius=r, stroke_color=c_, stroke_width=4, fill_color=c_, fill_opacity=0.25 if r < 0.2 else 0.0) for r, c_ in ((0.12, th.AMBER), (0.32, th.FAINT), (0.42, th.MUTED), (0.52, th.INK))]).move_to([-3.6, -0.4, 0])
        core = Rectangle(width=4.4, height=0.5, stroke_width=0, fill_color=th.SKY, fill_opacity=0.25).move_to([-3.6, -2.2, 0])
        clad = Rectangle(width=4.4, height=0.9, stroke_color=th.SKY, stroke_width=2).move_to([-3.6, -2.2, 0])
        zz = VMobject(stroke_color=th.AMBER, stroke_width=3).set_points_as_corners([[-5.8 + 0.55 * k, -2.2 + (0.22 if k % 2 else -0.22), 0] for k in range(9)])
        labs = VGroup(*[para(t_, width=6.0, size=26, color=th.INK).move_to([3.4, y_, 0]) for t_, y_ in [("twisted pair: twisting cancels crosstalk; Cat 6 up to 10 Gbps, 100 m", 1.6), ("coaxial: core, insulator, braided shield; cable TV", -0.4), ("optical fibre: light by total internal reflection; Tbps, km, immune to EMI", -2.2)]])
        with self.say("Guided media carry the signal along a cable. Twisted pair, the cheapest, twists its wires so that interference cancels out: most school networks use it. Coaxial cable has a central core and a braided shield, used for cable television. Optical fibre carries light, trapped in the glass core by total internal reflection: enormous bandwidth, long distances, and immune to electrical interference."):
            self.play(FadeIn(h), Create(tp), FadeIn(labs[0]))
            self.play(FadeIn(coax), FadeIn(labs[1]))
            self.play(FadeIn(core), Create(clad), Create(zz), FadeIn(labs[2]))
        self.play(FadeOut(VGroup(h, tp, coax, core, clad, zz, labs)))
        rows = [["unguided medium", "range / feature", "example"], ["radio wave", "omnidirectional, passes walls", "FM radio"], ["microwave", "line of sight, ~50 km per hop", "Wi-Fi (2.4, 5, 6 GHz), towers"], ["infrared", "a few metres, blocked by walls", "TV remote"], ["satellite", "global, ~250 ms delay", "remote areas, TV"]]
        tb = C.table(rows, [3.2, 4.6, 4.2], row_h=0.62, size=28, colors=[th.MINT, th.INK, th.MUTED]).move_to([0, 0.3, 0])
        with self.say("Unguided media send signals through free space. Radio waves spread in all directions and pass through walls. Microwaves need line of sight; Wi Fi uses them. Infrared works only within a room. Satellites cover the globe, but with a delay of about a quarter of a second each way. Wireless is quick to install and mobile, but less secure: anyone in range can listen.") as v:
            C.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 3
    def p3(self):
        self.section(2)
        h = C.head(self, "Transmission impairments")
        ax = Axes(x_range=[0, 10, 1], y_range=[-1.6, 1.6, 1], x_length=7.6, y_length=1.2, tips=False, axis_config={"stroke_opacity": 0})
        rows = VGroup()
        specs = [("attenuation", lambda x: np.exp(-0.25 * x) * np.sin(3 * x), "strength fades with distance → repeater/amplifier"), ("distortion", lambda x: 0.75 * np.sin(3 * x) + 0.4 * np.sin(10 * x), "shape changes: frequencies travel at different speeds"),
                 ("noise", None, "unwanted energy added: thermal, crosstalk, impulse")]
        rng = np.random.default_rng(5)
        nz = rng.normal(0, 0.18, 600)
        for k, (nm, fn, ex) in enumerate(specs):
            y = 1.5 - k * 1.9
            a_ = ax.copy().move_to([2.6, y, 0])
            if fn is None:
                fn = lambda x: 0.8 * np.sin(3 * x) + nz[min(599, int(x / 10 * 599))]
            rows.add(VGroup(a_.plot(lambda x: 0.8 * np.sin(3 * x), x_range=[0, 10, 0.02], color=th.FAINT, stroke_width=2), a_.plot(fn, x_range=[0, 10, 0.02], color=th.CORAL, stroke_width=3),
                            T(nm, size=28, color=th.AMBER, weight="BOLD").move_to([-4.6, y + 0.5, 0]), para(ex, width=3.6, size=19, color=th.BODY).move_to([-4.6, y - 0.25, 0])))
        with self.say("A signal never arrives exactly as it was sent. Attenuation: it weakens with distance, so repeaters regenerate it. Distortion: its shape changes, because different frequencies travel at different speeds. And noise: unwanted energy added on the way, from heat in the wires, from neighbouring wires, which is crosstalk, or from sudden spikes like lightning."):
            self.play(FadeIn(h))
            for r in rows:
                self.play(Create(r[0]), Create(r[1]), FadeIn(r[2]), FadeIn(r[3]), run_time=1.2)
        self.play(FadeOut(VGroup(h, rows)))
        rows = [["impairment", "what happens", "cure"], ["crosstalk", "a neighbouring wire leaks in", "twisting, shielding, fibre"], ["echo", "signal reflected back to the sender", "echo cancellers"], ["jitter", "packets arrive unevenly spaced", "jitter buffer, QoS"],
                ["bandwidth limit", "fast signals rounded off", "a wider medium (fibre)"]]
        tb = C.table(rows, [3.0, 5.0, 4.0], row_h=0.64, size=28, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.3, 0])
        with self.say("More impairments. Crosstalk: you faintly hear another call. Echo: you hear yourself, delayed. Jitter: packets arriving unevenly, which ruins a video call. And bandwidth itself is a limit: a channel simply cannot carry changes faster than its bandwidth.") as v:
            C.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 4
    def p4(self):
        self.section(3)
        h = C.head(self, "LAN, MAN, WAN")
        circ = VGroup(*[Circle(radius=r, stroke_color=c_, stroke_width=3, fill_color=c_, fill_opacity=0.08) for r, c_ in ((0.8, th.MINT), (1.6, th.SKY), (2.4, th.AMBER))]).move_to([-4.2, -0.5, 0])
        cl = VGroup(T("LAN", size=28, color=th.MINT, weight="BOLD").move_to(circ[0]), T("MAN", size=28, color=th.SKY, weight="BOLD").move_to(circ.get_center() + UP * 1.2), T("WAN", size=28, color=th.AMBER, weight="BOLD").move_to(circ.get_center() + UP * 2.0))
        txt = VGroup(T("LAN: a lab, a building, a campus; fastest; private", size=28, color=th.MINT), T("MAN: a city, e.g. an ISP across Kathmandu", size=28, color=th.SKY), T("WAN: a country or the world; the Internet", size=28, color=th.AMBER), T("PAN: a few metres (Bluetooth earphones)", size=26, color=th.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        txt.scale_to_fit_width(min(txt.width, 6.6)).move_to([3.0, -0.2, 0])
        with self.say("Networks are named by the area they cover. A local area network covers a room, a building or a campus: fast and private. A metropolitan network covers a city. A wide area network spans a country or the world, the Internet being the biggest. And a personal area network covers just a few metres."):
            self.play(FadeIn(h), LaggedStart(*[GrowFromCenter(c_) for c_ in circ], lag_ratio=0.3), FadeIn(cl))
            self.play(LaggedStart(*[FadeIn(t_, shift=LEFT * 0.2) for t_ in txt], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, circ, cl, txt)))
        h = C.head(self, "Client–server vs peer-to-peer")
        srv = pc("server", th.AMBER, w=1.6, h=0.9, size=24).move_to([-3.6, 0.8, 0])
        cls = VGroup(*[pc("client", th.SKY, w=1.2, h=0.55, size=20).move_to(srv.get_center() + 2.0 * np.array([np.cos(a), np.sin(a), 0]) + DOWN * 0.4) for a in np.linspace(PI * 1.1, PI * 1.9, 4)])
        cs_l = VGroup(*[Line(c_.get_center(), srv.get_center(), color=th.FAINT).set_z_index(-1) for c_ in cls])
        prs = VGroup(*[pc("peer", th.MINT, w=1.1, h=0.55, size=20).move_to([3.6 + 1.6 * np.cos(a), 0.4 + 1.4 * np.sin(a), 0]) for a in np.linspace(0, TAU, 5)[:-1] + 0.4])
        p_l = VGroup(*[Line(prs[a].get_center(), prs[b].get_center(), color=th.FAINT).set_z_index(-1) for a in range(4) for b in range(a + 1, 4)])
        labs = VGroup(para("central control, strong security, scales; but the server is a single point of failure", width=5.4, size=25, color=th.AMBER).move_to([-3.6, -2.4, 0]),
                      para("cheap, no server, every node both gives and takes; weak security, ~10 machines", width=5.4, size=25, color=th.MINT).move_to([3.6, -2.4, 0]))
        with self.say("Two architectures. In client server, a dedicated server provides services and clients request them: one place for accounts, security and backups, but if the server dies, everyone stops. In peer to peer, every computer is both client and server: cheap and simple for a small office, but security depends on every user."):
            self.play(FadeIn(h), FadeIn(srv), FadeIn(cls), Create(cs_l))
            self.play(FadeIn(labs[0]))
            self.play(FadeIn(prs), Create(p_l))
            self.play(FadeIn(labs[1]))
        self.play(FadeOut(VGroup(h, srv, cls, cs_l, prs, p_l, labs)))
        h = C.head(self, "Hub vs switch")
        hub = pc("HUB", th.CORAL, w=1.4, h=0.8, size=24).move_to([-3.4, 0.2, 0])
        sw = pc("SWITCH", th.MINT, w=1.6, h=0.8, size=24).move_to([3.4, 0.2, 0])

        def ring(c_, col):
            return VGroup(*[pc(n_, col, w=0.9, h=0.5, size=18).move_to(c_.get_center() + 2.0 * np.array([np.cos(a), np.sin(a), 0])) for n_, a in zip("ABCD", [PI * 0.75, PI * 0.25, -PI * 0.25, -PI * 0.75])])

        hs, ss = ring(hub, th.SKY), ring(sw, th.SKY)
        hl = VGroup(*[Line(x.get_center(), hub.get_center(), color=th.FAINT).set_z_index(-1) for x in hs])
        sl = VGroup(*[Line(x.get_center(), sw.get_center(), color=th.FAINT).set_z_index(-1) for x in ss])
        labs = VGroup(para("copies every frame to every port (layer 1)", width=5.0, size=24, color=th.CORAL).next_to(hub, DOWN, buff=1.9), para("learns MAC addresses, sends only to D (layer 2)", width=5.0, size=24, color=th.MINT).next_to(sw, DOWN, buff=1.9))
        with self.say("Network devices. A hub is a dumb repeater: a frame from A to D is copied to every port, wasting bandwidth and causing collisions. A switch learns which MAC address sits on which port and sends the frame only to D."):
            self.play(FadeIn(h), FadeIn(hub), FadeIn(hs), Create(hl), FadeIn(sw), FadeIn(ss), Create(sl))
            p = C.packet(th.AMBER, label="→D").move_to(hs[0].get_center())
            self.play(p.animate.move_to(hub.get_center()), run_time=0.6)
            cps = [p.copy() for _ in range(3)]
            self.play(*[c_.animate.move_to(x.get_center()) for c_, x in zip(cps, hs[1:])], FadeOut(p), run_time=0.8)
            self.play(FadeIn(labs[0]))
            q = C.packet(th.AMBER, label="→D").move_to(ss[0].get_center())
            self.play(q.animate.move_to(sw.get_center()), run_time=0.6)
            self.play(q.animate.move_to(ss[3].get_center()), run_time=0.6)
            self.play(FadeIn(labs[1]))
        self.play(FadeOut(VGroup(h, hub, sw, hs, ss, hl, sl, labs, q, *cps)))
        rows = [["device", "layer", "job"], ["NIC", "1–2", "connects a computer; holds the MAC address"], ["modem", "1", "modulates digital ↔ analogue"], ["repeater / hub", "1", "regenerates / copies to all ports"], ["bridge / switch", "2", "forwards by MAC address"], ["router", "3", "joins networks, routes by IP address"], ["gateway", "all", "translates between different protocols"]]
        tb = C.table(rows, [3.0, 1.2, 7.4], row_h=0.58, size=28, colors=[th.AMBER, th.SKY, th.INK]).move_to([0, 0.2, 0])
        with self.say("The full list, with each device's layer. A network card connects a computer. A modem converts between digital and analogue. Repeaters and hubs work on raw signals. Bridges and switches forward by MAC address. Routers join different networks and choose paths by IP address. And a gateway translates between different protocols.") as v:
            C.reveal_table(self, tb, v.dur * 0.85)
        self.play(FadeOut(tb))

    # ------------------------------------------------------------------ part 5
    def p5(self):
        self.section(4)
        h = C.head(self, "Topologies")

        def mk(kind, c):
            c = np.array(c, dtype=float)
            g = VGroup()
            if kind == "bus":
                g.add(Line(c + LEFT * 1.6, c + RIGHT * 1.6, color=th.AMBER, stroke_width=5))
                for k in range(4):
                    x = -1.2 + 0.8 * k
                    n_ = Dot(c + np.array([x, 0.6 * (1 if k % 2 else -1), 0]), radius=0.14, color=th.SKY)
                    g.add(Line(n_.get_center(), c + np.array([x, 0, 0]), color=th.FAINT), n_)
            elif kind == "star":
                hub = Square(side_length=0.4, stroke_color=th.AMBER, fill_color=th.AMBER, fill_opacity=0.6).move_to(c)
                g.add(hub)
                for a in np.linspace(0, TAU, 6)[:-1]:
                    n_ = Dot(c + 1.1 * np.array([np.cos(a), np.sin(a), 0]), radius=0.14, color=th.SKY)
                    g.add(Line(n_.get_center(), c, color=th.FAINT).set_z_index(-1), n_)
            elif kind == "ring":
                pts = [c + 1.0 * np.array([np.cos(a), np.sin(a), 0]) for a in np.linspace(0, TAU, 7)[:-1]]
                g.add(Polygon(*pts, stroke_color=th.AMBER, stroke_width=3), *[Dot(p_, radius=0.14, color=th.SKY) for p_ in pts])
            elif kind == "mesh":
                pts = [c + 1.0 * np.array([np.cos(a), np.sin(a), 0]) for a in np.linspace(PI / 2, PI / 2 + TAU, 6)[:-1]]
                g.add(*[Line(pts[a], pts[b], color=th.FAINT, stroke_width=2) for a in range(5) for b in range(a + 1, 5)], *[Dot(p_, radius=0.14, color=th.SKY) for p_ in pts])
            elif kind == "tree":
                root = Dot(c + UP * 0.9, radius=0.16, color=th.AMBER)
                mids = [Dot(c + np.array([x, 0, 0]), radius=0.14, color=th.AMBER) for x in (-0.8, 0.8)]
                leaves = [Dot(c + np.array([x, -0.9, 0]), radius=0.12, color=th.SKY) for x in (-1.2, -0.4, 0.4, 1.2)]
                g.add(*[Line(root.get_center(), m.get_center(), color=th.FAINT) for m in mids], *[Line(mids[k // 2].get_center(), l_.get_center(), color=th.FAINT) for k, l_ in enumerate(leaves)], root, *mids, *leaves)
            return g

        kinds = [("bus", "one backbone: cheapest; one break kills all"), ("star", "central switch: a cable fault hits one node; the switch is a single point of failure"), ("ring", "token passes round: equal access; one break stops the ring"),
                 ("mesh", "every pair linked: most reliable, n(n − 1)/2 links"), ("tree", "a hierarchy of stars: scales; a branch failure cuts its subtree")]
        cells = VGroup()
        for k, (kd, d_) in enumerate(kinds):
            c = [-4.6 + 4.6 * (k % 3), 1.6 - 3.0 * (k // 3), 0]
            shp = mk(kd, c).scale(0.72, about_point=np.array(c, dtype=float))
            cells.add(VGroup(shp, T(kd, size=28, color=th.AMBER, weight="BOLD").move_to(np.array(c) + DOWN * 1.0), para(d_, width=4.0, size=19, color=th.BODY).next_to(np.array(c) + DOWN * 1.2, DOWN, buff=0.05)))
        with self.say("A topology is the shape of a network. Bus: every computer taps one backbone cable; cheap, but one break stops everything. Star: everything connects to a central switch; a cable fault affects one computer, but the switch is a single point of failure. Ring: data passes round in one direction; equal access, but one break stops the ring. Mesh: every pair is linked; the most reliable and the most expensive. Tree: stars arranged in a hierarchy.") as v:
            self.play(FadeIn(h))
            for c_ in cells:
                self.play(FadeIn(c_, shift=UP * 0.15), run_time=0.6)
                self.hold(max(0, v.dur / 5 - 0.6))
        self.play(FadeOut(VGroup(h, cells)))
        C.worked(self, "A full mesh joins 8 computers. How many cables, how many ports per computer, and how many cables would a star need?",
                 [r"\text{mesh: } \frac{n(n - 1)}{2} = \frac{8 \times 7}{2} = 28 \text{ cables},\quad n - 1 = 7 \text{ ports each}", r"\text{star: } 8 \text{ cables} + \text{an 8-port switch}", r"28 \div 8 = 3.5 \text{ times the cable — mesh is kept for backbones}"],
                 ["The cost of a mesh.", "Every pair needs a link: eight times seven over two, twenty eight cables, and seven ports on each computer.", "A star needs just one cable per computer.", "Three and a half times the cable, and the gap grows with n. That is why mesh is used only where reliability is worth it."])

    # ------------------------------------------------------------------ part 6
    def p6(self):
        self.section(5)
        h = C.head(self, "OSI: seven layers, each adds its header")
        names = ["7 Application", "6 Presentation", "5 Session", "4 Transport", "3 Network", "2 Data link", "1 Physical"]
        pdus = ["data", "data", "data", "segment", "packet", "frame", "bits"]
        cols = [th.SKY, th.SKY, th.SKY, th.MINT, th.AMBER, th.PINK, th.CORAL]
        stack = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.08, width=3.4, height=0.55, stroke_color=c_, stroke_width=2, fill_color=th.PANEL, fill_opacity=1), T(n_, size=24, color=c_)).move_to([-4.6, 2.0 - 0.66 * k, 0]) for k, (n_, c_) in enumerate(zip(names, cols))])
        for g in stack:
            g[1].move_to(g[0])
        pdu = VGroup(*[T(p_, size=22, color=th.MUTED).next_to(stack[k], RIGHT, buff=0.15) for k, p_ in enumerate(pdus)])
        with self.say("The OSI reference model, published by ISO in nineteen eighty four, splits communication into seven layers, each with one job, so any layer can change without disturbing the rest. Application, presentation, session, transport, network, data link and physical. All People Seem To Need Data Processing."):
            self.play(FadeIn(h), LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in stack], lag_ratio=0.12), FadeIn(pdu))
        data = VGroup(RoundedRectangle(corner_radius=0.05, width=1.6, height=0.45, stroke_width=0, fill_color=th.SKY, fill_opacity=0.9), T("data", size=22, color=th.BG, weight="BOLD")).move_to([2.6, 2.0, 0])
        hdrs = [("TCP hdr", th.MINT, 3), ("IP hdr", th.AMBER, 4), ("Eth hdr", th.PINK, 5)]
        cap = para("encapsulation: each layer wraps the data with its own header", width=6.0, size=24, color=th.INK).move_to([3.4, -3.0, 0])
        with self.say("As data goes down the stack at the sender, each layer wraps it in its own header. Transport adds port numbers to make a segment. Network adds IP addresses to make a packet. Data link adds MAC addresses and a checksum to make a frame. The physical layer sends it as bits. At the receiver, each layer strips its header off on the way up. This wrapping is called encapsulation."):
            self.play(FadeIn(data))
            cur = data
            for nm, col, lv in hdrs:
                hb = VGroup(RoundedRectangle(corner_radius=0.05, width=1.2, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.9), T(nm, size=18, color=th.BG, weight="BOLD"))
                hb[1].move_to(hb[0])
                tgt_y = 2.0 - 0.66 * lv
                self.play(cur.animate.move_to([cur.get_center()[0], tgt_y, 0]), run_time=0.5)
                hb.next_to(cur, LEFT, buff=0.02)
                self.play(FadeIn(hb, shift=RIGHT * 0.3), run_time=0.5)
                cur = VGroup(hb, cur)
            bits = T("1 0 1 1 0 0 1 0 1 1 …", size=26, color=th.CORAL).move_to([2.6, 2.0 - 0.66 * 6, 0])
            self.play(FadeIn(bits))
            self.play(FadeIn(cap))
        self.play(FadeOut(VGroup(h, stack, pdu, cur, bits, cap)))
        rows = [["layer", "job", "protocols / devices"], ["7 application", "network services to programs", "HTTP, FTP, SMTP, DNS"], ["6 presentation", "format, encryption, compression", "TLS, JPEG, ASCII"], ["5 session", "open, manage, close sessions", "RPC, NetBIOS"],
                ["4 transport", "end-to-end delivery, ports", "TCP (reliable), UDP (fast)"], ["3 network", "IP addressing, routing", "IP, ICMP — router"], ["2 data link", "framing, MAC, CRC error check", "Ethernet — switch"], ["1 physical", "bits on the wire", "RJ-45, fibre — hub"]]
        tb = C.table(rows, [3.0, 5.0, 4.0], row_h=0.5, size=26, colors=[th.AMBER, th.INK, th.MINT]).move_to([0, 0.4, 0])
        nt = T("TCP/IP, the model the Internet actually uses, has 4 layers: application, transport, internet, network access.", size=24, color=th.MUTED).move_to([0, -2.8, 0])
        with self.say("Each layer's job and protocols. The Internet itself runs on the simpler TCP IP model, with four layers: the top three OSI layers are merged into one application layer.") as v:
            C.reveal_table(self, tb, v.dur * 0.75)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))

    # ------------------------------------------------------------------ part 7
    def p7(self):
        self.section(6)
        h = C.head(self, "An IPv4 address: 32 bits, four octets")
        octs = ["192", "168", "10", "37"]
        bins = [format(int(o), "08b") for o in octs]
        top = VGroup(*[T(o, size=40, color=th.INK, weight="BOLD") for o in octs])
        dots = VGroup(*[T(".", size=40, color=th.MUTED) for _ in range(3)])
        row = VGroup(top[0], dots[0], top[1], dots[1], top[2], dots[2], top[3]).arrange(RIGHT, buff=0.25).move_to([0, 1.8, 0])
        brow = VGroup(*[T(b, size=26, color=th.SKY, font=C.MONO) for b in bins]).arrange(RIGHT, buff=0.5).move_to([0, 0.7, 0])
        mask = VGroup(*[T(b, size=26, color=th.AMBER, font=C.MONO) for b in ["11111111"] * 3 + ["00000000"]]).arrange(RIGHT, buff=0.5).move_to([0, -0.2, 0])
        ml = T("mask 255.255.255.0 (/24): 1s mark the network part", size=28, color=th.AMBER).move_to([0, -0.9, 0])
        net = SurroundingRectangle(VGroup(*brow[:3]), color=th.MINT, buff=0.1)
        hst = SurroundingRectangle(brow[3], color=th.PINK, buff=0.1)
        res = VGroup(T("network address 192.168.10.0", size=28, color=th.MINT), T("broadcast address 192.168.10.255", size=28, color=th.PINK), T("usable hosts 2⁸ − 2 = 254", size=28, color=th.INK)).arrange(DOWN, buff=0.2).move_to([0, -2.3, 0])
        with self.say("An IPv4 address is thirty two bits, written as four numbers from nought to two five five: dotted decimal. One nine two dot one six eight dot ten dot thirty seven. In binary, each number is eight bits, an octet."):
            self.play(FadeIn(h), FadeIn(row))
            self.play(LaggedStart(*[TransformFromCopy(t_, b_) for t_, b_ in zip(top, brow)], lag_ratio=0.2))
        with self.say("The subnet mask says which bits name the network and which name the host. Two five five dot two five five dot two five five dot nought: the first twenty four bits are network. Set the host bits to nought for the network address, to all ones for the broadcast address. That leaves two to the eight minus two, two hundred and fifty four usable hosts."):
            self.play(FadeIn(mask), FadeIn(ml))
            self.play(Create(net), Create(hst))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3))
        self.play(FadeOut(VGroup(h, row, brow, mask, ml, net, hst, res)))
        rows = [["class", "first octet", "default mask", "hosts / network"], ["A", "1 – 126", "/8", "16 777 214"], ["B", "128 – 191", "/16", "65 534"], ["C", "192 – 223", "/24", "254"], ["D", "224 – 239", "—", "multicast"], ["E", "240 – 255", "—", "reserved"]]
        tb = C.table(rows, [1.6, 3.0, 3.0, 3.4], row_h=0.6, size=28, colors=[th.AMBER, th.INK, th.SKY, th.MINT]).move_to([0, 0.5, 0])
        nt = para("127.x.x.x is loopback (this computer). Private ranges 10/8, 172.16/12 and 192.168/16 are reused inside organisations; NAT lets them share one public address.", width=11.5, size=26, color=th.MUTED).move_to([0, -2.3, 0])
        with self.say("Addresses were once grouped into classes by their first octet. Class A, for huge networks, up to one two six. Class B, one two eight to one nine one. Class C, one nine two to two two three, with two hundred and fifty four hosts each. D is for multicast and E is reserved. One two seven is loopback, meaning this computer, and three private ranges are reused inside every school and home, sharing one public address through NAT.") as v:
            C.reveal_table(self, tb, v.dur * 0.65)
            self.play(FadeIn(nt))
        self.play(FadeOut(VGroup(tb, nt)))
        h = C.head(self, "Subnetting 192.168.1.0/24 into 4")
        bar = VGroup()
        for k in range(4):
            r = Rectangle(width=2.8, height=0.8, stroke_color=th.BG, stroke_width=2, fill_color=[th.SKY, th.MINT, th.AMBER, th.PINK][k], fill_opacity=0.5).move_to([-4.2 + 2.8 * k, 1.2, 0])
            bar.add(VGroup(r, T(f".{64 * k} – .{64 * k + 63}", size=24, color=th.INK).move_to(r)))
        st = VGroup(M(r"2^b \ge 4 \Rightarrow b = 2:\ /24 + 2 = /26 = 255.255.255.192", size=32), M(r"2^6 = 64 \text{ addresses per subnet},\ 64 - 2 = 62 \text{ usable}", size=32),
                    T("subnet 2: network .64, hosts .65 – .126, broadcast .127", size=28, color=th.MINT)).arrange(DOWN, buff=0.35).move_to([0, -1.0, 0])
        with self.say("Subnetting splits one network into several. To make four subnets, borrow two host bits, since two squared is four. The prefix becomes slash twenty six, mask two five five dot two five five dot two five five dot one nine two. Each subnet has sixty four addresses, sixty two usable, starting at nought, sixty four, one twenty eight and one ninety two. The second runs from sixty four, the network, to one twenty seven, the broadcast."):
            self.play(FadeIn(h))
            self.play(LaggedStart(*[GrowFromEdge(b_, LEFT) for b_ in bar], lag_ratio=0.25))
            for s_ in st:
                self.play(Write(s_) if isinstance(s_, MathTex) else FadeIn(s_), run_time=0.9)
        self.play(FadeOut(VGroup(h, bar, st)))
        c = self.callout("careful", "MAC address: physical, permanent, 48-bit, used by switches within one LAN. IP address: logical, changes when you move network, 32-bit (IPv4), used by routers.", width=11, size=26)
        with self.say("And keep two addresses apart. The MAC address is burned into the network card and never changes; switches use it inside one network. The IP address is logical and changes when you move to a new network; routers use it to cross networks."):
            self.play(FadeIn(c, shift=UP * 0.2))
        self.play(FadeOut(c))
        self.quiz("A device that forwards frames only to the port where the destination MAC address lives is a",
                  ["hub", "repeater", "switch", "modem"], 2,
                  "Pause and think.",
                  "A switch. A hub copies every frame to every port.")
        self.quiz("How many usable host addresses does a /26 subnet have?",
                  ["64", "62", "254", "126"], 1,
                  "One more.",
                  "Sixty two: six host bits give sixty four addresses, minus the network and broadcast addresses.")

    # ------------------------------------------------------------------ ending
    def ending(self):
        self.recap([
            "Five elements: message, sender, receiver, medium, protocol. Simplex, half, full duplex.",
            "Guided: twisted pair, coax, fibre. Unguided: radio, microwave, infrared, satellite.",
            "Impairments: attenuation, distortion, noise, crosstalk, echo, jitter.",
            "Hub copies to all; switch by MAC (L2); router by IP (L3). Bus, star, ring, mesh n(n−1)/2, tree.",
            "OSI 7 layers with encapsulation; IPv4 32 bits; hosts = 2ⁿ − 2; /26 → 4 subnets of 62.",
        ], "Quick recap. The five elements and three transmission modes. Guided and unguided media. The impairments. Hubs, switches and routers, and the topologies. The seven OSI layers, wrapping data in headers. And IP addresses, masks and subnetting.")
        self.outro("That was data communication and networking. Next, web technology: building pages with HTML, CSS, JavaScript and PHP. See you there.")
