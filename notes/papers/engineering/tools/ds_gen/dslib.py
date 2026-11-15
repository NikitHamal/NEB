import itertools, re
from collections import deque

def edmonds_karp(cap, flow0, s, t):
    """cap, flow0: dict (u,v)->int.  Returns (flow dict, list of (path, bottleneck), total, mincut S-set)"""
    f = dict(flow0); nodes = {u for e in cap for u in e}
    paths = []
    def res(u, v):
        return cap.get((u, v), 0) - f.get((u, v), 0) + f.get((v, u), 0)
    while True:
        par = {s: None}; q = deque([s])
        while q and t not in par:
            u = q.popleft()
            for v in sorted(nodes):
                if v not in par and res(u, v) > 0:
                    par[v] = u; q.append(v)
        if t not in par:
            break
        path = []; v = t
        while par[v] is not None: path.append(v); v = par[v]
        path.append(s); path.reverse()
        b = min(res(path[i], path[i + 1]) for i in range(len(path) - 1))
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            back = min(b, f.get((v, u), 0)); f[(v, u)] = f.get((v, u), 0) - back
            f[(u, v)] = f.get((u, v), 0) + (b - back)
        paths.append((path, b))
    S = set(par)
    total = sum(f.get((s, v), 0) for v in nodes)
    return f, paths, total, S

def prim(vertices, edges, start):
    inT = {start}; out = []
    while len(inT) < len(vertices):
        cand = [(w, u, v) for (u, v, w) in edges if (u in inT) != (v in inT)]
        w, u, v = min(cand, key=lambda x: (x[0], x[1], x[2]))
        out.append((u, v, w, sorted(inT))); inT.add(u if v in inT else v)
    return out

def subset_construct(delta, start, finals, alphabet):
    S0 = frozenset([start]); seen = {S0: None}; order = [S0]; table = {}
    i = 0
    while i < len(order):
        S = order[i]; i += 1
        for a in alphabet:
            T = frozenset(x for q in S for x in delta.get((q, a), ()))
            table[(S, a)] = T
            if T not in seen: seen[T] = None; order.append(T)
    return order, table

def name(S):
    return "∅" if not S else "{" + ",".join(sorted(S)) + "}"

def insertion_passes(a):
    a = a[:]; out = [("initial", a[:])]
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0 and a[j] > key: a[j + 1] = a[j]; j -= 1
        a[j + 1] = key; out.append(("pass %d (insert %d)" % (i, key), a[:]))
    return out

def bsearch(a, k):
    lo, hi = 1, len(a); steps = []
    while lo <= hi:
        mid = (lo + hi) // 2; steps.append((lo, hi, mid, a[mid - 1]))
        if a[mid - 1] == k: return mid, steps
        if a[mid - 1] < k: lo = mid + 1
        else: hi = mid - 1
    return None, steps

def check_regex():
    rx = re.compile(r'^(a|ba|bba)*(b|bb)?$')
    for n in range(0, 13):
        for s in map(''.join, itertools.product('ab', repeat=n)):
            assert bool(rx.match(s)) == ('bbb' not in s), s
    return True
