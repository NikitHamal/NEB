"""Fill {{PDA:KEY:w}}, {{TM:KEY:w}}, {{TMTAB:KEY}}, {{ENC:KEY}} placeholders in tplX.md and write the paper md.
Usage: python3 gen_toc.py <tpl.md> <out.md>"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from toclib import *
import machines as M

TMS = {"ABC": (M.TM_ABC, "q0", {"qf"}), "ABCD": (M.TM_ABCD, "q0", {"qf"}), "ODD": (M.TM_ODD, "q0", {"qf"}),
       "COMP": (M.TM_COMP, "q0", {"qf"}), "ACB": (M.TM_ACB, "q0", {"qf"}), "DBL": (M.TM_DBL, "q0", {"qh"}),
       "REV": (M.TM_REV, "sL", {"qf"}), "FL": (M.TM_FL, "q0", {"qf"})}
PDAS = {"ANBAN": (M.PDA_ANBAN, {"q2"}), "MGEN": (M.PDA_MGEN, {"q2"})}


def encode(delta, states, syms, accept):
    si = {q: i + 1 for i, q in enumerate(states)}
    yi = {s: i + 1 for i, s in enumerate(syms)}
    blocks = []
    for (q, s), (q2, w, mv) in delta.items():
        blocks.append("0" * si[q] + "1" + "0" * yi[s] + "1" + "0" * si[q2] + "1" + "0" * yi[w] + "1" + "0" * (1 if mv == "L" else 2))
    return "11".join(blocks), blocks


def sub(m):
    kind, args = m.group(1), m.group(2).split(":")
    if kind == "TM":
        d, st, acc = TMS[args[0]]; w = args[1] if len(args) > 1 else ""
        a, c = tm_run(d, st, acc, w); out = "%d moves; the machine %s." % (len(c) - 1, "accepts" if a else "halts without accepting")
        return trace_md(c, per=3, maxlines=60) + "\n\n" + out if False else trace_md(c, per=3, maxlines=60)
    if kind == "PDA":
        d, fin = PDAS[args[0]]; w = args[1]; a, p = pda_run(d, "q0", fin, w); assert a
        return pda_trace_md(w, p, per=3)
    if kind == "TT":
        rows = ["| $P$ | $Q$ | $R$ | $P\\to Q$ | $Q\\to R$ | $(P\\to Q)\\land(Q\\to R)$ | $P\\to R$ | whole formula |", "|---|---|---|---|---|---|---|---|"]
        imp = lambda a, b: (not a) or b; T_ = lambda x: "T" if x else "F"
        for P in (True, False):
            for Q in (True, False):
                for R in (True, False):
                    a, b = imp(P, Q), imp(Q, R); c = a and b; d = imp(P, R); e = imp(c, d); assert e
                    rows.append("| %s | %s | %s | %s | %s | %s | %s | **%s** |" % tuple(T_(x) for x in (P, Q, R, a, b, c, d, e)))
        return "\n".join(rows)
    if kind == "TMTAB":
        return tm_table(TMS[args[0]][0])
    if kind == "ENC":
        d = TMS["COMP"][0]; states = ["q0", "qf"]; syms = ["0", "1", "_"]
        code, blocks = encode(d, states, syms, {"qf"})
        names = {"q0": "q1 (start)", "qf": "q2 (accepting)"}
        rows = ["| Move | $i,j,k,l,m$ | Code |", "|---|---|---|"]
        for (q, s), (q2, w, mv) in d.items():
            si = {"q0": 1, "qf": 2}; yi = {"0": 1, "1": 2, "_": 3}
            rows.append("| $\\delta(%s,%s)=(%s,%s,%s)$ | %d,%d,%d,%d,%d | `%s` |" % (
                "q_%d" % si[q], "X_%d" % yi[s], "q_%d" % si[q2], "X_%d" % yi[w], mv, si[q], yi[s], si[q2], yi[w], 1 if mv == "L" else 2,
                "0" * si[q] + "1" + "0" * yi[s] + "1" + "0" * si[q2] + "1" + "0" * yi[w] + "1" + "0" * (1 if mv == "L" else 2)))
        return ("$(q_0 \\to q_1,\\ q_f \\to q_2,\\ 0=X_1,\\ 1=X_2,\\ B=X_3)$ has the three moves\n\n" + "\n".join(rows) +
                "\n\nso its code is the three blocks joined by $11$:\n\n`%s`\n\n(the whole string is %d symbols long). $U$ reads this string from tape 1, together with the input from tape 2." % (code, len(code)))
    raise KeyError(kind)


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    s = re.sub(r"\{\{(TMTAB|TM|PDA|ENC|TT):?([^}]*)\}\}", sub, s)
    open(sys.argv[2], "w").write(s)
    print("wrote", sys.argv[2], len(s))
