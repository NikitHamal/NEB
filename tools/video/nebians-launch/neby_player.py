"""The real Neby for the Dashain film: the product's geometry engine, animated by rig.py."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "neby"))
from rig import NebyRig, Performance  # noqa: E402

PERF = Performance(
    keys=[(0.0, "intro-neby-closed", 0, "smooth"), (0.6, "intro-neby-peek", 0.35, "spring"),
          (1.2, "intro-neby-focus", 0.40, "spring"), (1.9, "intro-neby-signature", 0.45, "smooth"),
          (2.6, "idle-front", 0.40, "smooth"),
          (3.0, "anticipation", 0.25, "spring"), (3.4, "delight", 0.30, "spring"), (4.4, "joy", 0.40, "spring"),
          (5.6, "soft-smile", 0.50, "smooth"),
          (7.2, "focus", 0.40, "smooth"), (7.8, "scan-left", 0.50, "smooth"), (8.7, "scan-right", 0.60, "smooth"),
          (9.6, "intro-scan", 0.50, "smooth"),
          (10.6, "joy", 0.30, "spring"), (11.4, "delight", 0.40, "smooth"), (12.4, "joy", 0.40, "smooth"),
          (13.6, "talk-a", 0.35, "smooth"), (14.2, "talk-b", 0.30, "smooth"), (14.8, "talk-c", 0.30, "smooth"),
          (15.4, "soft-smile", 0.40, "smooth"),
          (16.1, "cheer", 0.25, "spring"), (16.8, "success", 0.40, "spring"), (17.5, "joy", 0.40, "smooth"),
          (18.3, "wink", 0.28, "spring"), (19.0, "soft-smile", 0.50, "smooth")],
    blinks=[2.9, 5.2, 6.6, 10.1, 12.9, 15.0, 17.2, 19.45],
    looks=[(0.0, 0, 0, 0.1), (3.2, -0.6, 0.2, 0.5), (7.2, -0.7, 0.45, 0.5), (10.6, 0.7, 0.0, 0.5),
           (13.6, 0.0, 0.0, 0.4), (16.1, 0.0, -0.1, 0.4), (17.2, 0.5, 0.0, 0.6)])


class Neby:
    def __init__(self, duration=None, fps=None):
        self.rig = NebyRig()

    def draw(self, c, t, cx, cy, size, alpha=1.0, rot=0.0, shadow=True, sx=1.0, sy=1.0):
        self.rig.draw(c, PERF, t, cx, cy, size, alpha=alpha, rot=rot, sx=sx, sy=sy, shadow=shadow)
