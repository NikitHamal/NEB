#!/usr/bin/env python3
"""Print every MCQ of a chapter beside its keyed option, for a fast human review.

    python3 notes/tools/keyview.py notes/content/cee-chem/unit-05.md

One line per question: number, key letter, the text of the keyed option, the stem.
Reading the column of keyed options is the quickest way to catch a key that points
at the wrong option.
"""
import re, sys
path = sys.argv[1]
s = open(path, encoding='utf-8').read()
prac = s[s.index('## Practice questions'):]
# split into sets
sets = re.split(r'\n\*\*Set ', prac)[1:]
for st in sets:
    name = st.split('\n',1)[0]
    qpart, apart = st.split('::: note Answers',1)
    qs = re.findall(r'^(\d+)\. (.*?)\n   (\(a\).*?)$', qpart, re.M)
    ans = dict(re.findall(r'^\*\*(\d+)\.\*\* \(([a-d])\)', apart, re.M))
    print('=== Set', name)
    for n, stem, opts in qs:
        parts = re.split(r'\(([a-d])\) ', opts)
        od = {parts[k]: parts[k+1].strip() for k in range(1, len(parts)-1, 2)}
        k = ans.get(n)
        print(f"{n:>2} [{k}] {od.get(k)!s:40.40s} | {stem[:70]}")
