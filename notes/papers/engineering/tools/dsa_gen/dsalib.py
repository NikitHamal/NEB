"""Algorithms + figure helpers for the Data Structure and Algorithm papers (ENCT 252)."""
import itertools, os, re, subprocess, tempfile

# ---------------------------------------------------------------- infix -> postfix
PREC = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '$': 3}
RIGHT = {'^', '$'}

def to_postfix(expr):
    st, out, rows = [], [], []
    for ch in expr.replace(' ', ''):
        note = ''
        if ch.isalnum():
            out.append(ch); note = 'operand, send to output'
        elif ch == '(':
            st.append(ch); note = 'push ('
        elif ch == ')':
            pops = []
            while st[-1] != '(':
                pops.append(st[-1]); out.append(st.pop())
            st.pop(); note = 'pop to output until (' + (': ' + ' '.join(pops) if pops else '')
        else:
            pops = []
            while st and st[-1] != '(' and (PREC[st[-1]] > PREC[ch] or (PREC[st[-1]] == PREC[ch] and ch not in RIGHT)):
                pops.append(st[-1]); out.append(st.pop())
            st.append(ch)
            note = ('pop ' + ' '.join(pops) + ' (higher or equal precedence), ' if pops else '') + 'push ' + ch
        rows.append((ch, ''.join(st), ''.join(out), note))
    pops = []
    while st:
        pops.append(st[-1]); out.append(st.pop())
    rows.append(('end', '', ''.join(out), 'pop the remaining operators: ' + ' '.join(pops)))
    return ''.join(out), rows

def postfix_md(rows):
    t = '| Symbol | Stack (bottom to top) | Postfix output | Action |\n|---|---|---|---|\n'
    for s, st, o, n in rows:
        t += '| `%s` | `%s` | `%s` | %s |\n' % (s if s != 'end' else 'end', st or ' ', o or ' ', n)
    return t

def eval_check(infix, postfix, ops_pow='$'):
    import random
    names = sorted(set(c for c in infix if c.isalpha()))
    for _ in range(5):
        v = {c: random.uniform(1.3, 4.1) for c in names}
        e = infix
        for c, x in v.items(): e = e.replace(c, str(x))
        e = e.replace('^', '**').replace('$', '**').replace('/', '/')
        a = eval(e)
        s = []
        for ch in postfix:
            if ch.isalpha(): s.append(v[ch])
            else:
                y = s.pop(); x = s.pop()
                s.append({'+': x + y, '-': x - y, '*': x * y, '/': x / y, '^': x ** y, '$': x ** y}[ch])
        assert abs(a - s[0]) < 1e-9, (infix, postfix)
    return True

# ---------------------------------------------------------------- AVL
class AN:
    def __init__(s, k): s.k, s.l, s.r, s.h = k, None, None, 1

def _h(n): return n.h if n else 0
def _upd(n): n.h = 1 + max(_h(n.l), _h(n.r))
def _bf(n): return _h(n.l) - _h(n.r)
def _rr(y):
    x = y.l; y.l = x.r; x.r = y; _upd(y); _upd(x); return x
def _rl(x):
    y = x.r; x.r = y.l; y.l = x; _upd(x); _upd(y); return y

def avl_ins(n, k, log):
    if not n: return AN(k)
    if k < n.k: n.l = avl_ins(n.l, k, log)
    else: n.r = avl_ins(n.r, k, log)
    _upd(n); b = _bf(n)
    if b > 1 and k < n.l.k:
        log.append((k, n.k, b, 'LL', 'right rotation about %d' % n.k)); return _rr(n)
    if b < -1 and k > n.r.k:
        log.append((k, n.k, b, 'RR', 'left rotation about %d' % n.k)); return _rl(n)
    if b > 1 and k > n.l.k:
        log.append((k, n.k, b, 'LR', 'left rotation about %d, then right rotation about %d' % (n.l.k, n.k)))
        n.l = _rl(n.l); return _rr(n)
    if b < -1 and k < n.r.k:
        log.append((k, n.k, b, 'RL', 'right rotation about %d, then left rotation about %d' % (n.r.k, n.k)))
        n.r = _rr(n.r); return _rl(n)
    return n

def avl_tuple(n): return None if not n else (n.k, avl_tuple(n.l), avl_tuple(n.r))
def avl_height(n): return _h(n)
def avl_check(n):
    if not n: return True
    return abs(_bf(n)) <= 1 and avl_check(n.l) and avl_check(n.r)
def inorder(n): return [] if not n else inorder(n.l) + [n.k] + inorder(n.r)

def avl_build(seq):
    root = None; snaps = []
    for k in seq:
        log = []
        root = avl_ins(root, k, log)
        assert avl_check(root)
        snaps.append((k, log, avl_tuple(root)))
    return root, snaps

# ---------------------------------------------------------------- B-tree of order 3 (max 2 keys, 3 children)
class BN:
    def __init__(s, keys=None, ch=None): s.keys, s.ch = keys or [], ch or []

def _bins(n, k, log):
    if not n.ch:
        n.keys.append(k); n.keys.sort()
    else:
        i = sum(1 for x in n.keys if k > x)
        res = _bins(n.ch[i], k, log)
        if res:
            med, l, r = res; n.keys.insert(i, med); n.ch[i:i + 1] = [l, r]
    if len(n.keys) > 2:
        log.append('node %s overflows, median %d moves up' % (n.keys, n.keys[1]))
        return n.keys[1], BN(n.keys[:1], n.ch[:2]), BN(n.keys[2:], n.ch[2:])
    return None

def b_insert(root, k, log):
    res = _bins(root, k, log)
    if res:
        med, l, r = res; return BN([med], [l, r])
    return root

def b_tuple(n): return (list(n.keys), [b_tuple(c) for c in n.ch])
def b_str(n):
    s = '[' + ' '.join(map(str, n.keys)) + ']'
    if n.ch: s += '(' + ', '.join(b_str(c) for c in n.ch) + ')'
    return s
def b_depths(n, d=0):
    if not n.ch: return {d}
    return set().union(*[b_depths(c, d + 1) for c in n.ch])
def b_flat(n):
    if not n.ch: return list(n.keys)
    out = []
    for i, k in enumerate(n.keys): out += b_flat(n.ch[i]) + [k]
    return out + b_flat(n.ch[-1])
def b_build(seq):
    root = BN(); snaps = []
    for k in seq:
        log = []; root = b_insert(root, k, log)
        assert len(b_depths(root)) == 1 and b_flat(root) == sorted(b_flat(root))
        snaps.append((k, log, b_str(root)))
    assert sorted(seq) == b_flat(root)
    return root, snaps

# ---------------------------------------------------------------- heap sort
def heapsort(a):
    a = a[:]; n = len(a); build = []; steps = []
    def sift(i, m):
        while True:
            l = 2 * i + 1; r = l + 1; g = i
            if l < m and a[l] > a[g]: g = l
            if r < m and a[r] > a[g]: g = r
            if g == i: break
            a[i], a[g] = a[g], a[i]; i = g
    for i in range(n // 2 - 1, -1, -1):
        sift(i, n); build.append((i + 1, a[:]))
    heap = a[:]
    for end in range(n - 1, 0, -1):
        mx = a[0]; a[0], a[end] = a[end], a[0]; sift(0, end); steps.append((mx, end, a[:]))
    assert a == sorted(a)
    return heap, build, steps, a

def heap_md(build, steps, n):
    t = '| Step | Array (heap part, then sorted part after the bar) |\n|---|---|\n'
    for i, arr in build: t += '| heapify node %d | %s |\n' % (i, ', '.join(map(str, arr)))
    for k, (mx, end, arr) in enumerate(steps, 1):
        h = arr[:end]; s = arr[end:]
        t += '| extract %d: swap with last, shrink, sift down | %s \\| **%s** |\n' % (mx, ', '.join(map(str, h)), ', '.join(map(str, s)))
    return t

# ---------------------------------------------------------------- quick sort (first element pivot, two pointers)
def quicksort(a):
    a = a[:]; log = []
    def qs(lo, hi):
        if lo >= hi: return
        p = a[lo]; i = lo + 1; j = hi
        while True:
            while i <= hi and a[i] <= p: i += 1
            while a[j] > p: j -= 1
            if i < j: a[i], a[j] = a[j], a[i]
            else: break
        a[lo], a[j] = a[j], a[lo]
        log.append((lo, hi, p, j, a[:]))
        qs(lo, j - 1); qs(j + 1, hi)
    qs(0, len(a) - 1)
    assert a == sorted(a)
    return a, log

def qs_md(log):
    t = '| Sub-list (positions) | Pivot | Pivot final position | Array after the partition |\n|---|---|---|---|\n'
    for lo, hi, p, j, arr in log:
        t += '| %d to %d | %d | %d | %s |\n' % (lo + 1, hi + 1, p, j + 1, ', '.join(map(str, arr)))
    return t

# ---------------------------------------------------------------- hashing
def hash_insert(keys, size, probe):
    t = [None] * size; rows = []
    for k in keys:
        h = k % size; i = 0; tried = []
        while True:
            idx = (h + probe(i)) % size; tried.append(idx)
            if t[idx] is None: t[idx] = k; break
            i += 1
            assert i < 4 * size
        rows.append((k, h, tried, idx))
    return t, rows

def hash_md(rows, form):
    t = '| Key | h(k) = k mod 10 | Probe positions tried (%s) | Stored at |\n|---|---|---|---|\n' % form
    for k, h, tried, idx in rows:
        t += '| %d | %d | %s | **%d** |\n' % (k, h, ', '.join(map(str, tried)), idx)
    return t

def table_md(t):
    s = '| Index | ' + ' | '.join(str(i) for i in range(len(t))) + ' |\n|---|' + '---|' * len(t) + '\n| Key | ' + ' | '.join('-' if x is None else str(x) for x in t) + ' |\n'
    return s

# ---------------------------------------------------------------- Floyd-Warshall / Warshall
INF = 10 ** 9
def floyd(n, edges):
    d = [[INF] * n for _ in range(n)]
    for i in range(n): d[i][i] = 0
    for u, v, w in edges: d[u - 1][v - 1] = w
    mats = [[r[:] for r in d]]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] < INF and d[k][j] < INF and d[i][k] + d[k][j] < d[i][j]: d[i][j] = d[i][k] + d[k][j]
        mats.append([r[:] for r in d])
    return mats

def mat_md(m, title):
    n = len(m)
    t = '**%s**\n\n| | 1 | 2 | 3 | 4 |\n|---|---|---|---|---|\n' % title
    for i in range(n): t += '| **%d** | ' % (i + 1) + ' | '.join('∞' if x >= INF else str(x) for x in m[i]) + ' |\n'
    return t + '\n'

def warshall(n, edges):
    r = [[0] * n for _ in range(n)]
    for u, v, w in edges: r[u - 1][v - 1] = 1
    for i in range(n): r[i][i] = r[i][i]
    for k in range(n):
        for i in range(n):
            for j in range(n): r[i][j] = r[i][j] or (r[i][k] and r[k][j])
    return r

# ---------------------------------------------------------------- Dijkstra / Kruskal / Prim
def dijkstra(edges, src, directed=False):
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w)); adj.setdefault(v, []).append((u, w)) if not directed else adj.setdefault(v, [])
    dist = {v: 10 ** 9 for v in adj}; dist[src] = 0; prev = {}; done = []; rows = []
    V = sorted(adj)
    while len(done) < len(V):
        u = min((v for v in V if v not in done), key=lambda v: (dist[v], v)); done.append(u)
        for v, w in adj[u]:
            if v not in done and dist[u] + w < dist[v]: dist[v] = dist[u] + w; prev[v] = u
        rows.append((u, list(done), {v: dist[v] for v in V if v not in done}))
    return dist, prev, rows

def dijk_md(rows, V):
    t = '| Step | Vertex made permanent | Tentative distances of the others |\n|---|---|---|\n'
    for k, (u, done, rest) in enumerate(rows, 1):
        t += '| %d | %s (d = %s) | %s |\n' % (k, u, rows[k - 1][2].get(u, ''), ', '.join('%s = %s' % (v, '∞' if x >= 10 ** 9 else x) for v, x in rest.items()))
    return t

def kruskal(edges):
    par = {}
    def find(x):
        par.setdefault(x, x)
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    out = []; rows = []; tot = 0
    for u, v, w in sorted(edges, key=lambda e: (e[2], e[0] + e[1])):
        if find(u) != find(v): par[find(u)] = find(v); out.append((u, v)); tot += w; rows.append((u, v, w, 'accept'))
        else: rows.append((u, v, w, 'reject (cycle)'))
    return out, tot, rows

def prim(V, edges, start):
    inT = {start}; out = []; tot = 0; rows = []
    while len(inT) < len(V):
        cand = [(w, u, v) for u, v, w in edges if (u in inT) != (v in inT)]
        w, u, v = min(cand)
        new = v if u in inT else u
        rows.append((sorted(inT), (u, v), w)); out.append((u, v)); tot += w; inT.add(new)
    return out, tot, rows

# ---------------------------------------------------------------- Tower of Hanoi / Fibonacci trees
def hanoi_tree(n, s, d, a, cnt):
    if n == 1:
        cnt[0] += 1; return ('move %d: disk 1\n%s->%s' % (cnt[0], s, d), 'move', [])
    left = hanoi_tree(n - 1, s, a, d, cnt)
    cnt[0] += 1; mv = ('move %d: disk %d\n%s->%s' % (cnt[0], n, s, d), 'move', [])
    right = hanoi_tree(n - 1, a, d, s, cnt)
    return ('H(%d,%s,%s,%s)' % (n, s, d, a), 'call', [left, mv, right])

def hanoi_moves(n, s, d, a, out):
    if n == 0: return
    hanoi_moves(n - 1, s, a, d, out); out.append((n, s, d)); hanoi_moves(n - 1, a, d, s, out)

def fib_tree(n):
    if n < 2: return ('F(%d)=%d' % (n, n), 'base', [])
    l, r = fib_tree(n - 1), fib_tree(n - 2)
    v = int(l[0].split('=')[1]) + int(r[0].split('=')[1])
    return ('F(%d)=%d' % (n, v), 'call', [l, r])

# ---------------------------------------------------------------- C programs
def runc(src, stdin=''):
    with tempfile.TemporaryDirectory() as d:
        c = os.path.join(d, 'p.c'); open(c, 'w').write(src)
        r = subprocess.run(['gcc', '-Wall', '-Wextra', '-o', os.path.join(d, 'p'), c], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        assert not r.stderr.strip(), r.stderr
        o = subprocess.run([os.path.join(d, 'p')], capture_output=True, text=True, input=stdin, timeout=10)
        assert o.returncode == 0
        return o.stdout

# ---------------------------------------------------------------- figure prelude + wrappers
def fig(caption, code):
    assert '"' not in caption
    return '```figure caption="%s"\n%s```\n' % (caption, code)

PRE = r'''import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
'''

GTREE = PRE + r'''def gtree(ax,T,dx=1.0,dy=1.0,w=0.9,fs=7):
    P={}; cnt=[0]
    def lay(t,d,path):
        lab,kind,ch=t
        if not ch: x=cnt[0]; cnt[0]+=1
        else:
            xs=[lay(c,d+1,path+(i,)) for i,c in enumerate(ch)]; x=(xs[0]+xs[-1])/2
        P[path]=(x*dx,-d*dy,lab,kind); return x
    lay(T,0,())
    for p,(x,y,lab,kind) in P.items():
        if p:
            px,py=P[p[:-1]][:2]; ax.plot([px,x],[py-0.2*dy,y+0.2*dy],color=INK,lw=0.9,zorder=1)
    for p,(x,y,lab,kind) in P.items():
        fc={"call":"white","base":"#eaf3ff","move":"#fff4d6"}[kind]
        box(ax,x,y,w,0.4*dy,lab,fc=fc,fs=fs)
    xs=[v[0] for v in P.values()]; ys=[v[1] for v in P.values()]
    ax.set_xlim(min(xs)-w,max(xs)+w); ax.set_ylim(min(ys)-0.5*dy,0.5*dy)
'''

def tree_fig(caption, T, w, h, dx, dy, bw, fs):
    return fig(caption, GTREE + 'T=%r\nfig,ax=plt.subplots(figsize=(%s,%s)); ax.axis("off")\ngtree(ax,T,dx=%s,dy=%s,w=%s,fs=%s)\n' % (T, w, h, dx, dy, bw, fs))

BIN = r'''def bin_draw(ax,T,r=0.34,fs=8):
    out={}; cnt=[0]
    def go(n,d,par):
        if n is None: return
        go(n[1],d+1,n[0]); out[n[0]]=(cnt[0],d,par); cnt[0]+=1; go(n[2],d+1,n[0])
    go(T,0,None)
    for k,(x,d,par) in out.items():
        if par is not None:
            px,pd=out[par][0],out[par][1]; ax.plot([px,x],[-pd,-d],color=INK,lw=1,zorder=1)
    for k,(x,d,par) in out.items():
        ax.add_patch(mp.Circle((x,-d),r,fc="white",ec=INK,lw=1.2,zorder=3)); ax.text(x,-d,str(k),ha="center",va="center",fontsize=fs,zorder=4)
    ax.set_xlim(-1,cnt[0]); ax.set_ylim(-max(v[1] for v in out.values())-0.8,0.8); ax.set_aspect("equal")
'''

def bin_fig(caption, T, w, h, fs=8):
    return fig(caption, 'import matplotlib.patches as mp\n' + BIN + 'T=%r\nfig,ax=plt.subplots(figsize=(%s,%s)); ax.axis("off")\nbin_draw(ax,T,fs=%s)\n' % (T, w, h, fs))

MT = PRE + r'''def mtree(ax,T,fs=8):
    P={}; cnt=[0.0]
    def lay(n,d,path):
        keys,ch=n; wdt=0.5*len(keys)+0.35
        if not ch: x=cnt[0]+wdt/2; cnt[0]+=wdt+0.35
        else:
            xs=[lay(c,d+1,path+(i,)) for i,c in enumerate(ch)]; x=(xs[0]+xs[-1])/2
        P[path]=(x,-d*1.4,keys,wdt); return x
    lay(T,0,())
    for p,(x,y,keys,wdt) in P.items():
        if p:
            px,py=P[p[:-1]][:2]; ax.plot([px,x],[py-0.22,y+0.22],color=INK,lw=1,zorder=1)
    for p,(x,y,keys,wdt) in P.items(): box(ax,x,y,wdt,0.44,"  ".join(map(str,keys)),fs=fs)
    xs=[v[0] for v in P.values()]; ys=[v[1] for v in P.values()]
    ax.set_xlim(min(xs)-1.2,max(xs)+1.2); ax.set_ylim(min(ys)-0.6,0.6)
'''

def mt_fig(caption, T, w, h, fs=8):
    return fig(caption, MT + 'T=%r\nfig,ax=plt.subplots(figsize=(%s,%s)); ax.axis("off")\nmtree(ax,T,fs=%s)\n' % (T, w, h, fs))

def heap_fig(caption, a, w=4.6, h=2.6):
    return fig(caption, 'A=%r\nfig,ax=plt.subplots(figsize=(%s,%s)); ax.axis("off")\nimport math\nn=len(A); L=int(math.log2(n))+1\nP={}\nfor i in range(n):\n    lv=int(math.log2(i+1)); j=i-(2**lv-1); P[i]=((j+0.5)/2**lv*8,-lv*1.1)\nfor i in range(1,n):\n    p=(i-1)//2; ax.plot([P[p][0],P[i][0]],[P[p][1],P[i][1]],color=INK,lw=1,zorder=1)\nfor i in range(n):\n    ax.add_patch(mp.Circle(P[i],0.34,fc="white",ec=INK,lw=1.2,zorder=3)); ax.text(P[i][0],P[i][1],str(A[i]),ha="center",va="center",fontsize=8,zorder=4); ax.text(P[i][0]+0.42,P[i][1]+0.34,str(i+1),fontsize=6,color="#b00020")\nax.set_xlim(-0.8,8.8); ax.set_ylim(-(L-1)*1.1-0.7,0.7); ax.set_aspect("equal")\n' % (a, w, h)).replace('A=', 'import matplotlib.patches as mp\nA=', 1)

def graph_fig(caption, edges, pos, hl=(), w=5.6, h=3.0, xl=(-0.8, 9.0), yl=(-0.8, 4.6)):
    code = "E=%r\nM=%r\nP=%r\n" % (edges, [tuple(x) for x in hl], pos) + r'''fig,ax=plt.subplots(figsize=(%s,%s)); ax.axis("off"); ax.set_aspect("equal")
def inM(u,v): return (u,v) in M or (v,u) in M
for u,v,w in E:
    t=inM(u,v)
    ax.plot([P[u][0],P[v][0]],[P[u][1],P[v][1]],color=ACCENT if t else "#9aa",lw=3.0 if t else 1.1,zorder=1)
    mx,my=(P[u][0]+P[v][0])/2,(P[u][1]+P[v][1])/2
    ax.text(mx,my,str(w),fontsize=8,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.6),zorder=4,color="#b00020" if t else INK)
for k,p in P.items(): ax.scatter([p[0]],[p[1]],s=330,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],k,ha="center",va="center",fontsize=9,zorder=5)
ax.set_xlim%r; ax.set_ylim%r
''' % (w, h, xl, yl)
    return fig(caption, code)
