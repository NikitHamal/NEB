from manim import ManimColor

BG = "#0B0E1A"
BG2 = "#121730"
PANEL = "#171C36"
PANEL_EDGE = "#2A3160"
INK = "#F3F5FF"
BODY = "#C9CEE8"
MUTED = "#8189B0"
FAINT = "#3A4170"

ACCENT = "#7C74FF"
BRAND = "#4A42D6"
TEAL = "#2EC4B6"
AMBER = "#FFB547"
CORAL = "#FF6B6B"
MINT = "#7BE495"
SKY = "#4CC9F0"
PINK = "#F472B6"
LIME = "#C5F05C"

PALETTE = [ACCENT, TEAL, AMBER, CORAL, SKY, MINT, PINK, LIME]

SUBJECT_COLORS = {
    "phy": SKY,
    "chem": MINT,
    "bio": LIME,
    "math": ACCENT,
    "omath": PINK,
    "cs": TEAL,
    "eng": AMBER,
    "nep": CORAL,
    "soc": AMBER,
    "health": MINT,
    "sci": SKY,
    "acc": TEAL,
    "eco": PINK,
    "qbank": ACCENT,
    "qbankc": ACCENT,
}

LATIN_DISPLAY = "Poppins"
LATIN_BODY = "Inter"
DEVA = "Mukta"
MONO = "JetBrains Mono"


def c(hex_):
    return ManimColor(hex_)
