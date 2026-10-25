#!/usr/bin/env python3
"""Check that chemical equations balance (atoms and charge).

    grep -o "[^|]*→[^|]*" notes/content/cee-chem/unit-05.md | python3 notes/tools/eqcheck.py
    echo "2KMnO4 → K2MnO4 + MnO2 + O2" | python3 notes/tools/eqcheck.py

One equation per input line, written as in the books: Unicode subscripts and
superscript charges (MnO₄⁻, Fe³⁺), state symbols ((s), (aq)), hydrates with ·,
species separated by " + ", sides by → or ⇌. Prints OK or BAD with the atom and
charge totals of each side. Lines it cannot parse are reported, not guessed.
"""
import re, sys
from collections import Counter
SUB = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻', '0123456789+-')
def parse_species(s):
    s = s.strip()
    m = re.match(r'^(\d*)\s*(.*)$', s)
    coef = int(m.group(1)) if m.group(1) else 1
    body = m.group(2)
    # charge: trailing superscripts
    ch = 0
    mm = re.search(r'([⁰¹²³⁴⁵⁶⁷⁸⁹]*)([⁺⁻])$', body)
    if mm:
        num = mm.group(1).translate(SUP) or '1'
        ch = int(num) * (1 if mm.group(2) == '⁺' else -1)
        body = body[:mm.start()]
    body = body.translate(SUB)
    if body == 'e':
        return coef, Counter(), -coef if False else -1
    body = re.sub(r'\((s|l|g|aq)\)', '', body)
    def count(f):
        stack = [Counter()]
        i = 0
        while i < len(f):
            c = f[i]
            if c in '([':
                stack.append(Counter()); i += 1
            elif c in ')]':
                i += 1
                n = re.match(r'\d*', f[i:]).group(0); i += len(n)
                top = stack.pop()
                for k, v in top.items(): stack[-1][k] += v * (int(n) if n else 1)
            elif c == '·':
                i += 1
                n = re.match(r'\d*', f[i:]).group(0); i += len(n)
                # hydrate multiplier applies to following group
                rest = f[i:]
                sub = count(rest)
                for k, v in sub.items(): stack[-1][k] += v * (int(n) if n else 1)
                break
            else:
                m2 = re.match(r'([A-Z][a-z]?)(\d*)', f[i:])
                if not m2: raise ValueError('bad '+f)
                stack[-1][m2.group(1)] += int(m2.group(2)) if m2.group(2) else 1
                i += len(m2.group(0))
        return stack[0]
    return coef, count(body), ch
def check(eq):
    l, r = re.split(r'→|⇌', eq)
    tot = []
    for side in (l, r):
        C = Counter(); Q = 0
        for sp in side.split(' + '):
            coef, cnt, ch = parse_species(sp)
            for k, v in cnt.items(): C[k] += coef * v
            Q += coef * ch
        tot.append((C, Q))
    ok = tot[0][0] == tot[1][0] and tot[0][1] == tot[1][1]
    print(('OK ' if ok else 'BAD'), eq, '' if ok else (dict(tot[0][0]), tot[0][1], dict(tot[1][0]), tot[1][1]))
for eq in sys.stdin.read().strip().split('\n'):
    eq = eq.strip()
    if not eq or not re.search(r'→|⇌', eq):
        continue
    try:
        check(eq)
    except Exception as e:
        print('??? ', eq, '(cannot parse: %s)' % e)
