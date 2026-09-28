# Verbatim anchors for the unrecovered regions
Each failing patch below asserted one of these old_strings against a subagent-written
file whose bytes are not in the export. When regenerating a chapter, these snippets
MUST appear verbatim (they are figure code / table rows the QA patches expect).

## bash#1487 Move overlapping adiabatic label in fig06

```
cd /data/workspace/NEB/notes/content/qbank12 && python3 - <<'PYEOF'
import io
p='unit-03.md'; s=io.open(p,encoding='utf-8').read()
old="ax.annotate('adiabatic', (1.48, 0.56), color=ACCENT, fontsize=8.6, ha='left', va='top')"
new="ax.annotate('adiabatic', (1.05, 0.45), color=ACCENT, fontsize=8.6, ha='left', va='top')"
assert s.count(old)==1
io.open(p,'w',encoding='utf-8').write(s.replace(old,new))
print('ok')
PYEOF
```

## bash#1489 Fix fig19 Paschen label and re-render

```
cd /data/workspace/NEB/notes/content/qbank12 && python3 - <<'PYEOF'
import io
p='unit-03.md'; s=io.open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:60])
    s=s.replace(old,new)

rep("""    dx, ha = (0.025, 'left') if nf < 3 else (-0.03, 'right')
    ax.text(x+dx, (Ei+Ef)/2, lab, fontsize=7.6, color=col, va='center', ha=ha)""",
    """    if nf >= 3:
        ax.annotate(lab.replace('\\n', ' '), xy=(x+0.012, (Ei+Ef)/2),
                    xytext=(0.90, -2.45), fontsize=7.6, color=col,
                    ha='right', va='center',
                    arrowprops=dict(arrowstyle='-', color=col, lw=0.7))
    else:
        ax.text(x+0.025, (Ei+Ef)/2, lab, fontsize=7.6, color=col, va='center')""")

rep("""ax.annotate('$B_r$ (retentivity)', (0.12, Br+0.05), fontsize=8.4,
            color='#A8271F', ha='left', va='bottom')""",
    """ax.annotate('$B_r$ (retentivity)', (0.17, Br+0.10), fontsize=8.4,
            color='#A8271F', ha='left', va='bottom')""")
io.open(p,'w',encoding='utf-8').write(s)
print('ok')
PYEOF
python3 /data/workspace/NEB/notes/pipeline/preview.py /data/workspace/NEB/notes/content/qbank12/unit-03.md /tmp/qb12pc_u03 2>&1 | grep -E 'fig(16|19)|FAIL'
```

## bash#1490 Fix retentivity point in fig16

```
cd /data/workspace/NEB/notes/content/qbank12 && python3 - <<'PYEOF'
import io
p='unit-03.md'; s=io.open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:60])
    s=s.replace(old,new)
# retentivity was marked on the ascending branch (B negative); it belongs on the
# descending branch, where B is positive when H falls to zero
rep("Br = branch(0.0, -1)", "Br = branch(0.0, +1)")
rep("""ax.annotate('$B_r$ (retentivity)', (0.17, Br+0.10), fontsize=8.4,
            color='#A8271F', ha='left', va='bottom')
ax.annotate('$H_c$ (coercivity)', (Hc-0.12, -0.16), fontsize=8.4,
            color='#0B6A62', ha='right', va='top')""",
    """ax.annotate('$B_r$ (retentivity)', (-0.14, Br+0.06), fontsize=8.4,
            color='#A8271F', ha='right', va='bottom')
ax.annotate('$H_c$ (coercivity)', (Hc-0.15, 0.20), fontsize=8.4,
            color='#0B6A62', ha='right', va='bottom')""")
io.open(p,'w',encoding='utf-8').write(s)
print('ok')
PYEOF
python3 /data/workspace/NEB/notes/pipeline/preview.py /data/workspace/NEB/notes/content/qbank12/unit-03.md /tmp/qb12pc_u03 2>&1 | grep -E 'fig16|FAIL'
```

## bash#1503 Insert third photo, dedupe row, count MCQs

```
cd /data/workspace/NEB/notes && python3 - <<'PYEOF'
import io, re
p="content/qbank12/unit-05.md"
s=io.open(p,encoding="utf-8").read()

# remove duplicate nitro row
dup = "| Zn + H₂O, neutral | N-phenylhydroxylamine |\n"
assert dup in s
s = s.replace(dup, "")

# insert titration photo into 5.1 before MCQ 1
anchor = "1. In the reaction K₂Cr₂O₇ + 4H₂SO₄"
photo = ('```photo id="qbank/titration-endpoint" caption="The end point of an '
 'acid–base titration. One drop past equivalence, phenolphthalein turns the '
 'colourless solution permanently pink; the swirl shows the colour just before '
 'it spreads through the flask. Choosing the indicator whose range brackets the '
 'equivalence pH is what makes an end point this sharp." width="56"\n```\n\n')
assert anchor in s
s = s.replace(anchor, photo + anchor, 1)
io.open(p,"w",encoding="utf-8").write(s)

# count MCQs per section
sec=None; counts={}
for line in s.split("\n"):
    m=re.match(r"^## (5\.\d+) (.+)$", line)
    if m: sec=(m.group(1), m.group(2)); counts[sec]=0
    if sec and re.match(r"^\d+\. .*\[1\]</span>$", line.strip()):
        counts[sec]+=1
tot=0
for k,v in counts.items():
    print(k[0], k[1], v); tot+=v
print("TOTAL", tot)
PYEOF
python3 /data/workspace/NEB/notes/pipeline/check.py /data/workspace/NEB/notes/content/qbank12/unit-05.md 2>&1 | tail -3
```

## bash#1505 Add two missing year tags

```
cd /data/workspace/NEB/notes && python3 - <<'PYEOF'
import io
p="content/qbank12/unit-05.md"
s=io.open(p,encoding="utf-8").read()
a="2. The solubility product of chalk is 9.3 × 10⁻⁸. Its solubility in g L⁻¹ (M = 100) is <span"
b="2. The solubility product of chalk is 9.3 × 10⁻⁸. Its solubility in g L⁻¹ (M = 100) is (NEB 2078 model) <span"
assert a in s; s=s.replace(a,b)
a="3. When a lead storage battery is discharged, <span"
b="3. When a lead storage battery is discharged, (NEB 2078 model) <span"
assert a in s; s=s.replace(a,b)
io.open(p,"w",encoding="utf-8").write(s)
PYEOF
grep -o "(NEB [^)]*)" /data/workspace/NEB/notes/content/qbank12/unit-05.md | sort | uniq -c
```
