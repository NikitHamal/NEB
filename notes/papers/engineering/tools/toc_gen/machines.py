"""All machines used in the Theory of Computation papers, each verified exhaustively against its language.
Run `python3 machines.py` to re-check everything."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from toclib import *

B = "_"


def T(rows):
    """rows: 'q sym -> q2 wr mv' strings -> delta dict"""
    d = {}
    for r in rows:
        l, rt = r.split("->"); q, s = l.split(); q2, wr, mv = rt.split(); d[(q, s)] = (q2, wr, mv)
    return d


# ---------------------------------------------------------------- TM : a^n b^n c^n (n >= 0)
TM_ABC = T([
    "q0 a -> q1 X R", "q0 Y -> q4 Y R", "q0 _ -> qf _ S",
    "q1 a -> q1 a R", "q1 Y -> q1 Y R", "q1 b -> q2 Y R",
    "q2 b -> q2 b R", "q2 Z -> q2 Z R", "q2 c -> q3 Z L",
    "q3 a -> q3 a L", "q3 b -> q3 b L", "q3 Y -> q3 Y L", "q3 Z -> q3 Z L", "q3 X -> q0 X R",
    "q4 Y -> q4 Y R", "q4 Z -> q4 Z R", "q4 _ -> qf _ S",
])
# ---------------------------------------------------------------- TM : a^n b^n c^n d^n (n >= 0)
TM_ABCD = T([
    "q0 a -> q1 X R", "q0 Y -> q5 Y R", "q0 _ -> qf _ S",
    "q1 a -> q1 a R", "q1 Y -> q1 Y R", "q1 b -> q2 Y R",
    "q2 b -> q2 b R", "q2 Z -> q2 Z R", "q2 c -> q3 Z R",
    "q3 c -> q3 c R", "q3 W -> q3 W R", "q3 d -> q4 W L",
    "q4 a -> q4 a L", "q4 b -> q4 b L", "q4 c -> q4 c L", "q4 Y -> q4 Y L", "q4 Z -> q4 Z L", "q4 W -> q4 W L", "q4 X -> q0 X R",
    "q5 Y -> q5 Y R", "q5 Z -> q5 Z R", "q5 W -> q5 W R", "q5 _ -> qf _ S",
])
# ---------------------------------------------------------------- TM : odd binary number
TM_ODD = T(["q0 0 -> q0 0 R", "q0 1 -> q0 1 R", "q0 _ -> q1 _ L", "q1 1 -> qf 1 S"])
# ---------------------------------------------------------------- TM : bit complement
TM_COMP = T(["q0 0 -> q0 1 R", "q0 1 -> q0 0 R", "q0 _ -> qf _ S"])
# ---------------------------------------------------------------- TM : a^n c b^n (n >= 0)
TM_ACB = T([
    "q0 a -> q1 X R", "q0 c -> q4 c R",
    "q1 a -> q1 a R", "q1 c -> q1 c R", "q1 Y -> q1 Y R", "q1 b -> q2 Y L",
    "q2 a -> q2 a L", "q2 c -> q2 c L", "q2 Y -> q2 Y L", "q2 X -> q0 X R",
    "q4 Y -> q4 Y R", "q4 _ -> qf _ S",
])
# ---------------------------------------------------------------- TM : unary doubling 1^n -> 1^2n
TM_DBL = T([
    "q0 X -> q0 X R", "q0 1 -> q1 X R", "q0 Y -> q6 1 R", "q0 _ -> qh _ S",
    "q1 1 -> q1 1 R", "q1 Y -> q1 Y R", "q1 _ -> q2 Y R",
    "q2 _ -> q3 Y L",
    "q3 Y -> q3 Y L", "q3 1 -> q3 1 L", "q3 X -> q0 X R",
    "q6 Y -> q6 1 R", "q6 _ -> q7 _ L",
    "q7 1 -> q7 1 L", "q7 X -> q8 _ L",
    "q8 X -> q8 _ L", "q8 _ -> q9 _ R",
    "q9 _ -> q9 _ R", "q9 1 -> qh 1 S",
])
# ---------------------------------------------------------------- TM : reverse w over {a,b} (swap outer pair, storage in states)
TM_REV = T([
    "sL a -> sL a L", "sL b -> sL b L", "sL A -> sL A L", "sL B -> sL B L", "sL # -> sL # L", "sL _ -> s0 _ R",
    "s0 A -> s0 A R", "s0 B -> s0 B R", "s0 a -> Ra # R", "s0 b -> Rb # R", "s0 _ -> cr _ S",
    "Ra a -> Ra a R", "Ra b -> Ra b R", "Ra A -> Ra2 A L", "Ra B -> Ra2 B L", "Ra _ -> Ra2 _ L",
    "Rb a -> Rb a R", "Rb b -> Rb b R", "Rb A -> Rb2 A L", "Rb B -> Rb2 B L", "Rb _ -> Rb2 _ L",
    "Ra2 # -> cr A R", "Rb2 # -> cr B R",
    "Ra2 a -> Ly_a A L", "Ra2 b -> Ly_b A L", "Rb2 a -> Ly_a B L", "Rb2 b -> Ly_b B L",
    "Ly_a a -> Ly_a a L", "Ly_a b -> Ly_a b L", "Ly_a # -> sL A L",
    "Ly_b a -> Ly_b a L", "Ly_b b -> Ly_b b L", "Ly_b # -> sL B L",
    "cr A -> cr A R", "cr B -> cr B R", "cr a -> cr a R", "cr b -> cr b R", "cr _ -> cl _ L",
    "cl A -> cl a L", "cl B -> cl b L", "cl _ -> qf _ S",
])

# ---------------------------------------------------------------- PDAs
# L = { a^n b a^n : n >= 0 } (accept by final state)
PDA_ANBAN = [("q0", "a", "Z", "q0", "aZ"), ("q0", "a", "a", "q0", "aa"),
             ("q0", "b", "Z", "q1", "Z"), ("q0", "b", "a", "q1", "a"),
             ("q1", "a", "a", "q1", ""), ("q1", "", "Z", "q2", "Z")]
# L = { a^m b^n : m >= n > 0 } (accept by final state)
PDA_MGEN = [("q0", "a", "Z", "q0", "aZ"), ("q0", "a", "a", "q0", "aa"),
            ("q0", "b", "a", "q1", ""), ("q1", "b", "a", "q1", ""),
            ("q1", "", "a", "q2", "a"), ("q1", "", "Z", "q2", "Z")]


def verify():
    ok = True

    def chk(name, delta, acc, pred, alphabet, n):
        nonlocal ok
        bad = []
        for s in strings(alphabet, n):
            a, _ = tm_run(delta, "q0" if ("q0", "_") in delta or any(k[0] == "q0" for k in delta) else "sL", {acc}, s)
            if a != pred(s): bad.append(s)
        print(("OK  " if not bad else "FAIL"), name, bad[:5]); ok &= not bad

    def anbncn(s): m = re.fullmatch(r"(a*)(b*)(c*)", s); return bool(m) and len(m[1]) == len(m[2]) == len(m[3])
    def anbncndn(s): m = re.fullmatch(r"(a*)(b*)(c*)(d*)", s); return bool(m) and len(m[1]) == len(m[2]) == len(m[3]) == len(m[4])
    chk("a^n b^n c^n", TM_ABC, "qf", anbncn, "abc", 9)
    chk("a^n b^n c^n d^n", TM_ABCD, "qf", anbncndn, "abcd", 8)
    chk("odd binary", TM_ODD, "qf", lambda s: s != "" and s[-1] == "1", "01", 10)
    chk("a^n c b^n", TM_ACB, "qf", lambda s: bool(re.fullmatch(r"a*cb*", s)) and s.count("a") == s.count("b"), "abc", 9)
    for s in strings("01", 9):
        a, c = tm_run(TM_COMP, "q0", {"qf"}, s); assert a and tm_output(c) == "".join("1" if x == "0" else "0" for x in s)
    print("OK   complement")
    for n in range(0, 9):
        a, c = tm_run(TM_DBL, "q0", {"qh"}, "1" * n); assert a and tm_output(c) == "1" * (2 * n), (n, c[-1])
    print("OK   doubling")
    for s in strings("ab", 8):
        a, c = tm_run(TM_REV, "sL", {"qf"}, s) if s else tm_run(TM_REV, "s0", {"qf"}, "")
        assert a and tm_output(c) == s[::-1], (s, tm_output(c))
    print("OK   reverse")
    for s in strings("ab", 11):
        exp = bool(re.fullmatch(r"a*ba*", s)) and s.index("b") == len(s) - 1 - s.index("b")
        a, _ = pda_run(PDA_ANBAN, "q0", {"q2"}, s); assert a == exp, s
        exp2 = bool(re.fullmatch(r"a+b+", s)) and s.count("a") >= s.count("b")
        a2, _ = pda_run(PDA_MGEN, "q0", {"q2"}, s); assert a2 == exp2, s
    print("OK   PDAs")
    return ok


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
