# PERT example in 12-sepm-2080-9371 Q15: recompute ES/EF/LS/LF/slack
dur = {'A':3,'B':4,'C':2,'D':5,'E':3,'F':2}
pred = {'A':[],'B':['A'],'C':['A'],'D':['B'],'E':['C'],'F':['D','E']}
order = list('ABCDEF')
ES, EF = {}, {}
for k in order:
    ES[k] = max([EF[p] for p in pred[k]] or [0]); EF[k] = ES[k] + dur[k]
T = max(EF.values()); assert T == 14
succ = {k:[s for s in order if k in pred[s]] for k in order}
LF, LS = {}, {}
for k in reversed(order):
    LF[k] = min([LS[s] for s in succ[k]] or [T]); LS[k] = LF[k] - dur[k]
table = {'A':(0,3,0,3,0),'B':(3,7,3,7,0),'C':(3,5,7,9,4),'D':(7,12,7,12,0),'E':(5,8,9,12,4),'F':(12,14,12,14,0)}
for k,(es,ef,ls,lf,sl) in table.items():
    assert (ES[k],EF[k],LS[k],LF[k],LS[k]-ES[k]) == (es,ef,ls,lf,sl), k
assert 3+4+5+2 == 14 and 3+2+3+2 == 10
print("12-sepm-2080-9371: all checks pass")
