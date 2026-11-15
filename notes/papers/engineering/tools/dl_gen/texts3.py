from texts2 import *

KN = {"T": "T", "D": "D", "JK": "JK", "SR": "SR"}
KNAME = {"T": "T flip-flop", "D": "D flip-flop", "JK": "JK flip-flop", "SR": "SR flip-flop"}
EXC = {
    "T": ("| Q | Q⁺ | T |\n|---|---|---|\n| 0 | 0 | 0 |\n| 0 | 1 | 1 |\n| 1 | 0 | 1 |\n| 1 | 1 | 0 |\n", "$T = Q \\oplus Q^{+}$"),
    "D": ("| Q | Q⁺ | D |\n|---|---|---|\n| 0 | 0 | 0 |\n| 0 | 1 | 1 |\n| 1 | 0 | 0 |\n| 1 | 1 | 1 |\n", "$D = Q^{+}$"),
    "JK": ("| Q | Q⁺ | J | K |\n|---|---|---|---|\n| 0 | 0 | 0 | X |\n| 0 | 1 | 1 | X |\n| 1 | 0 | X | 1 |\n| 1 | 1 | X | 0 |\n", "$J,K$ as tabulated"),
    "SR": ("| Q | Q⁺ | S | R |\n|---|---|---|---|\n| 0 | 0 | 0 | X |\n| 0 | 1 | 1 | 0 |\n| 1 | 0 | 0 | 1 |\n| 1 | 1 | X | 0 |\n", "$S,R$ as tabulated"),
}

def nff(n):
    k = 1
    while 2 ** k < n: k += 1
    return k

def counter_text(title, nq, kind, trans, extra=0, extra_names=(), unused=None, seq_for_timing=None, timing_cap="", per_row=3, kmcs=0.55):
    d = design(nq, kind, trans, extra=extra, xnames=tuple(extra_names) or ("X",))
    s = f"**Design of {title}.**\n\n"
    s += f"*Step 1 - number of flip-flops.* $2^{{{nq-1}}} < N \\le 2^{{{nq}}}$ needs $n={nq}$ flip-flops ({KNAME[kind]}s), all clocked together (synchronous). The states are $" + "".join(d["qnames"]) .replace("Q", "Q") + "$.\n\n"
    s += f"*Step 2 - excitation table of the {KNAME[kind]}.*\n\n" + EXC[kind][0] + "\n"
    s += "*Step 3 - state / excitation table* (for each present state the next state, and the flip-flop inputs needed from the excitation table; X = don't care):\n\n"
    s += excitation_table(d, kind, nq, extra_names=list(extra_names) if extra else ())
    if unused:
        s += f"\nThe unused states ({unused}) never occur, so their next-state and input entries are don't-cares (X) in the K-maps.\n"
    s += "\n*Step 4 - K-map simplification of every flip-flop input.*\n\n"
    maps = maps_for(d, kind, nq)
    s += kmap_figure("K-maps for the flip-flop inputs (1 = needed, X = don't care); on the maps A, B, C, D stand for the present-state bits in the order of the table.", maps, "".join(["A", "B", "C", "D"]) if False else "".join(n[-1] for n in d["names"]) if False else "ABCD", per_row=per_row, cs=kmcs).replace("kmap(", "kmap(")
    s += "\nThe loops give\n\n" + pin_equations_block(d, kind, nq) + "\n"
    s += "*Step 5 - logic diagram.*\n\n" + circuit_fig(f"Logic diagram of {title}.", d, kind, nq, extra=(list(extra_names) if extra else ())) + "\n"
    if seq_for_timing:
        s += timing_fig(timing_cap, seq_for_timing, d["qnames"])
    return s, d

def detector_text(pattern, kind):
    trans = detector(pattern)
    L = len(pattern)
    d = design(2, kind, trans, extra=1, xnames=("X",))
    # state diagram
    labs = {}
    for (k, b), (ns, z) in trans.items():
        labs.setdefault((k, ns), []).append(f"{b}/{z}")
    edges = [(k, ns, ", ".join(v)) for (k, ns), v in labs.items()]
    names = [f"S{i}" for i in range(L)]
    code = "statediag(ax,%r,%r)\n" % (names, edges)
    meaning = []
    for i in range(L):
        meaning.append(f"$S_{i}$: " + ("no part of the pattern seen yet (reset state)" if i == 0 else f"the last {i} input bit{'s' if i>1 else ''} {pattern[:i]} seen"))
    s = f"**Design of the sequence detector for {pattern} (Mealy machine, overlapping sequences allowed, {KNAME[kind]}s).** One input $X$ (serial data), one output $Z$; $Z=1$ for the clock period in which the last bit of **{pattern}** arrives.\n\n"
    s += "*Step 1 - state diagram.* States remember how much of the pattern has been matched:\n\n" + "\n".join("- " + m for m in meaning) + "\n\n"
    s += "Edge labels are $X/Z$. After a complete match the machine falls back to the longest prefix of the pattern that is also a suffix of what was received (overlap).\n\n"
    W = (L - 1) * 2.2 + 3.4
    s += figblock(f"State diagram (Mealy) of the {pattern} detector; labels are X/Z.", code, w=5.9, h=3.0, xlim="(-1.0,%s)" % round(W - 1.0, 2), ylim="(-2.4,1.7)", ) + "\n"
    s += "*Step 2 - state table.*\n\n"
    rows = []
    for k in range(L):
        rows.append([f"S{k}", *[f"S{trans[(k,b)][0]} / {trans[(k,b)][1]}" for b in (0, 1)]])
    s += tbl(["Present state", "X = 0: next / Z", "X = 1: next / Z"], rows)
    s += "\n*Step 3 - state assignment.* Three states need $n = 2$ flip-flops: $S_0=00$, $S_1=01$, $S_2=10$ ($Q_1Q_0$). The code 11 is unused (don't care).\n\n"
    s += f"*Step 4 - excitation table of the {KNAME[kind]}.*\n\n" + EXC[kind][0] + "\n"
    s += "*Step 5 - state/excitation table* with $Q_1Q_0$ the present state and $X$ the input:\n\n"
    s += excitation_table(d, kind, 2, extra_names=["X"], show_z=True)
    s += "\n*Step 6 - K-maps* (variables $Q_1, Q_0, X$; the unused state 11 gives X entries):\n\n"
    s += kmap_figure("K-maps for the flip-flop inputs and the output Z (variables Q1 Q0 X; A = Q1, B = Q0, C = X).", maps_for(d, kind, 2), "ABC", per_row=3 if True else 2, cs=0.6)
    s += "\n" + pin_equations_block(d, kind, 2) + "\n"
    s += "*Step 7 - logic diagram.*\n\n" + circuit_fig(f"Logic diagram of the {pattern} sequence detector ({KNAME[kind]}s).", d, kind, 2, extra=["X"]) + "\n"
    # verification
    stream = "0110110011" if pattern == "011" else {"110": "1101100110", "010": "0101010011", "101": "1010110101"}.get(pattern, "0110110011")
    st = 0; srow = []; z_out = []
    for ch in stream:
        ns, z = trans[(st, int(ch))]; srow.append((st, int(ch), ns, z)); z_out.append(z); st = ns
    s += f"*Check with a test stream* $X = {stream}$ (applied left to right): the states visited are " + ", ".join(f"S{a}" for a, _, _, _ in srow) + f" and the output is $Z = {''.join(map(str, z_out))}$, with a 1 exactly when the last three bits are {pattern} (including overlaps).\n\n"
    # timing
    n = len(stream)
    xs = [int(c) for c in stream]
    states = [0] + [srow[i][2] for i in range(n)]
    nq = 2
    code = f"clock(ax,0,{nq*0.95+0.3+2*0.95},{n})\n"
    ytop = nq * 0.95 + 0.3 + 2 * 0.95
    code += "guides(ax,%r,%s,-0.1)\n" % (list(range(n)), ytop + 0.7)
    # X changes shortly after each edge (data set up for the next edge); Z is Mealy: depends on X and present state
    tx = [(0.0, xs[0])]
    for k in range(1, n):
        if xs[k] != xs[k - 1]: tx.append((round(k - 0.45, 3), xs[k]))
    code += "wave(ax,%s,%r,%s,'X')\n" % (3 * 0.95 + 0.1 + 0.95 * 0 + (nq) * 0.95 * 0 + 0.0 + 0.0 + 0.95 * 0, tx, n) if False else ""
    yX = nq * 0.95 + 0.1 + 0.95; yZ = nq * 0.95 + 0.1
    code += "wave(ax,%s,%r,%s,'X')\n" % (yX + 0.0, tx, n)
    # Z: during period k (between edge k-1... ) Mealy output = f(state before edge k, X_k): changes with X (mid-period) -> show value in [k-0.45,k+0.55)
    zs = z_out
    tz = [(0.0, zs[0])]
    for k in range(1, n):
        if zs[k] != zs[k - 1]: tz.append((round(k - 0.45, 3), zs[k]))
    code += "wave(ax,%s,%r,%s,'Z',color='#d9534f')\n" % (yZ + 0.0, tz, n)
    for f in range(nq):
        bit = nq - 1 - f
        lv = (states[0] >> bit) & 1
        tr = [(0.0, lv)]
        for k in range(1, n + 1):
            nb = (states[k] >> bit) & 1
            if nb != lv: tr.append((round(k - 1 + 0.05, 3), nb)); lv = nb
        code += "wave(ax,%s,%r,%s,%r)\n" % ((nq - 1 - f) * 0.95 + 0.1, tr, n, "Q%d" % bit)
    W = n + 2.6; H = ytop + 1.1
    s += figblock(f"Timing diagram of the {pattern} detector for X = {stream}: Z goes high in the period in which the last bit of {pattern} is applied (Mealy output, depends on X and the present state).", code, w=5.9, h=round(max(1.8, 5.9 * H / W), 2), xlim="(-1.9,%s)" % (n + 0.7), ylim="(-0.3,%s)" % round(ytop + 0.9, 2))
    return s, d
