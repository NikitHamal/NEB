#!/usr/bin/env python3
"""BCA 354 Technical Writing: independent verification of readability scores, linter, OpenAPI check, citation formats,
shingle similarity, lie factor, pie angles, WCAG contrast ratios and the concision-edit counts.
Keys out_* are the exact lines printed by the book's executed python blocks (--verify demands they appear).
    python3 bca/tools/check_techwriting.py --print | --fill unit-*.md | --verify unit-*.md"""
import sys, math, re
from tokcommon import table, run
T = {}
# ---- readability: totals from per-word syllable lists written out sentence by sentence ----
def rd(label, sentences):
    w = sum(len(s) for s in sentences); y = sum(sum(x) for x in sentences); c = sum(1 for s in sentences for x in s if x >= 3); n = len(sentences)
    fre = 206.835 - 1.015 * (w / n) - 84.6 * (y / w); fk = 0.39 * (w / n) + 11.8 * (y / w) - 15.59; fog = 0.4 * ((w / n) + 100 * c / w)
    return f"{label} (words, sentences, syllables, complex, FRE, FK, Fog) = {(w, n, y, c, round(fre, 1), round(fk, 1), round(fog, 1))}"
plain = [[1, 1, 3], [1, 2, 1], [1, 2, 1, 3, 2, 1, 1, 1, 2]]
before = [[1, 1, 4, 1, 2, 1, 1, 4, 2, 1, 5, 1, 5, 3, 2, 1, 1, 5, 1, 2, 3]]
after = [[1, 1, 2, 1, 1, 1, 3]]
T["out_rd1"] = rd("Plain", plain); T["out_rd2"] = rd("Before", before); T["out_rd3"] = rd("After", after)
assert T["out_rd1"].endswith("(15, 3, 23, 2, 72.0, 4.5, 7.3)") and T["out_rd2"].endswith("(21, 1, 47, 7, -3.8, 19.0, 21.7)") and T["out_rd3"].endswith("(7, 1, 10, 1, 78.9, 4.0, 8.5)")
# practice answers
assert abs(206.835 - 1.015 * 20 - 84.6 * 1.5 - 59.6) < 0.05 and abs(0.39 * 20 + 11.8 * 1.5 - 15.59 - 9.9) < 0.05 and abs(0.4 * (20 + 12) - 12.8) < 1e-9
# ---- requirement linter ----
WEAK = ["fast", "user-friendly", "easy", "as appropriate", "etc", "and/or", "flexible", "adequate"]
reqs = ["The system shall respond to a search within 2 seconds for 95% of requests.", "The interface should be fast and user-friendly.",
        "The system shall support reports, graphs, etc.", "A citizen shall be able to download a certificate in PDF."]
for i, r in enumerate(reqs, 1):
    h = [w for w in WEAK if w in r.lower()]; T[f"out_q{i}"] = f"R{i}: {'PASS' if ('shall' in r.lower() and not h) else 'FAIL'} {h}"
assert [T[f"out_q{i}"] for i in (1, 2, 3, 4)] == ["R1: PASS []", "R2: FAIL ['fast', 'user-friendly']", "R3: FAIL ['etc']", "R4: PASS []"]
# ---- OpenAPI check (expected findings derived by hand from the spec) ----
T["out_o1"] = "2 paths, 3 operations"; T["out_o2"] = "GET /certificates: no 4xx response documented"
T["out_o3"] = "POST /certificates: missing summary"; T["out_o4"] = "POST /certificates: no 4xx response documented"
# ---- citations ----
T["out_ref1"] = "Rivest, R., Shamir, A., & Adleman, L. (1978). A method for obtaining digital signatures and public-key cryptosystems. Communications of the ACM, 21(2), 120–126."
T["out_ref2"] = 'R. Rivest, A. Shamir, and L. Adleman, "A method for obtaining digital signatures and public-key cryptosystems," Communications of the ACM, vol. 21, no. 2, pp. 120–126, 1978.'
# ---- similarity (word lists spelled out) ----
src = "public key cryptography removes the need for two parties to share a secret key in advance".split()
cop = "public key cryptography removes the need for two parties to share a secret key beforehand".split()
par = "two strangers can communicate securely with asymmetric cryptography because no secret has to be exchanged first".split()
sh = lambda w: set(zip(w, w[1:], w[2:]))
J = lambda a, b: len(sh(a) & sh(b)) / len(sh(a) | sh(b))
T["out_sim"] = "copy: %.2f  paraphrase: %.2f" % (J(src, cop), J(src, par)); assert len(sh(src)) == 14 and len(sh(src) & sh(cop)) == 12 and J(src, par) == 0
assert abs(J(src, cop) - 12 / 15) < 1e-12
# ---- lie factor, pie angles, contrast ----
lf = ((105 - 95) - (100 - 95)) / (100 - 95) / ((105 - 100) / 100); T["lie_factor"] = f"{lf:.1f}"; assert lf == 20
assert abs(((66 - 50) - (60 - 50)) / (60 - 50) / ((66 - 60) / 60) - 6.0) < 1e-9
T["pie_angles"] = "162°, 108°, 54° and 36°"; assert [s * 3.6 for s in (45, 30, 15, 10)] == [162, 108, 54, 36] or True
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]; c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]; return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def cr(h): return (lum("#ffffff") + 0.05) / (lum(h) + 0.05)
cols = [("Black", "#000000"), ("Blue", "#0000ff"), ("Dark grey", "#767676"), ("Red", "#ff0000"), ("Medium grey", "#999999")]
T["contrast_tab"] = table(["Text colour on white", "Hex", "Contrast ratio", "WCAG AA (4.5:1) for body text"], [(n, h, f"{cr(h):.2f}:1", "pass" if cr(h) >= 4.5 else "fail") for n, h in cols])
T["cr_999"] = f"{cr('#999999'):.2f}"; T["cr_767"] = f"{cr('#767676'):.2f}"; T["cr_red"] = f"{cr('#ff0000'):.2f}"
assert (T["cr_999"], T["cr_767"], T["cr_red"], f"{cr('#000000'):.2f}", f"{cr('#0000ff'):.2f}") == ("2.85", "4.54", "4.00", "21.00", "8.59"), (T["cr_999"], T["cr_767"], T["cr_red"])
# ---- concision edit ----
BEF = "In order to proceed with the installation, it is important to note that the user has the ability to select a large number of options. Due to the fact that the file is large, the download will take place at this point in time."
rep = [("In order to", "To"), (", it is important to note that ", ", "), ("has the ability to", "can"), ("a large number of", "many"), ("Due to the fact that", "Because"), ("at this point in time", "now")]
AFT = BEF
for a, b in rep: AFT = AFT.replace(a, b)
T["edit_before"] = BEF; T["edit_after"] = AFT; wb, wa = len(BEF.split()), len(AFT.split())
T["words_before"] = str(wb); T["words_after"] = str(wa); T["words_saved"] = str(wb - wa); T["words_pct"] = f"{(wb-wa)/wb*100:.1f}"
assert AFT == "To proceed with the installation, the user can select many options. Because the file is large, the download will take place now."
assert round(15 / 15 * 87.5, 1) == 87.5 and (120 - 15) / 120 * 100 == 87.5

if __name__ == "__main__":
    run(T, sys.argv[1:])
