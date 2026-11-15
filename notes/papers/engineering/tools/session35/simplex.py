from fractions import Fraction as Fr
import sys
def fmt(p):
    m,k=p
    if m==0: return str(k)
    if k==0: return ("%sM"%m).replace('1M','M') if m!=1 and m!=-1 else ('M' if m==1 else '-M')
    ms = 'M' if m==1 else '-M' if m==-1 else '%sM'%m
    return "%s %s %s"%(ms,'+' if k>0 else '-',abs(k))
def run(names,rows,basis,c,art=(),title=''):
    # maximise sum c_j x_j ; rows = list of (coeffs..., rhs). art = names of artificial vars
    n=len(names)
    T=[[ (Fr(0),Fr(x)) for x in r] for r in rows]
    z=[(Fr(0),-Fr(cj)) for cj in c]+[(Fr(0),Fr(0))]
    for j,nm in enumerate(names):
        if nm in art: z[j]=(Fr(1),Fr(0))
    def sub(a,b,f): return (a[0]-f[0]*b[0] if False else a[0]-b[0]*f, a[1]-b[1]*f)
    # eliminate artificial from row0
    for i,b in enumerate(basis):
        if names[b] in art:
            z=[(z[j][0]-T[i][j][1],z[j][1]) for j in range(n+1)]   # z -= M*row
    out=[]; it=0
    while True:
        def table():
            h='| Basis | '+' | '.join(names)+' | RHS |\n|'+'---|'*(n+2)+'\n'
            for i,b in enumerate(basis): h+='| '+names[b]+' | '+' | '.join(fmt(T[i][j]) for j in range(n+1))+' |\n'
            h+='| Z | '+' | '.join(fmt(z[j]) for j in range(n+1))+' |\n'
            return h
        out.append('**Table %d**\n\n'%(it+1)+table())
        # entering: most negative (m,k)
        e=min(range(n),key=lambda j:(z[j][0],z[j][1]))
        if (z[e][0],z[e][1])>=(0,0): break
        ratios=[(T[i][n][1]/T[i][e][1],i) for i in range(len(basis)) if T[i][e][1]>0]
        if not ratios: out.append('unbounded'); break
        r=min(ratios)[1]
        out.append('Entering %s, leaving %s (pivot %s).\n'%(names[e],names[basis[r]],T[r][e][1]))
        p=T[r][e][1]; T[r]=[(a/p,b/p) if False else (a, b/p) for a,b in T[r]]
        for i in range(len(basis)):
            if i!=r:
                f=T[i][e][1]; T[i]=[(T[i][j][0],T[i][j][1]-f*T[r][j][1]) for j in range(n+1)]
        f=z[e]; z=[(z[j][0]-f[0]*T[r][j][1],z[j][1]-f[1]*T[r][j][1]) for j in range(n+1)]
        basis[r]=e; it+=1
    return '\n'.join(out)
if __name__=='__main__':
    print('### BH Q14 dual: max W=12u+17v; 2u+3v<=21; 5u+7v<=50')
    print(run(['u','v','s1','s2'],[[2,3,1,0,21],[5,7,0,1,50]],[2,3],[12,17,0,0]))
    print('### BH Q15 BigM')
    print(run(['x1','x2','s1','s2','A1'],[[1,1,1,0,0,5],[3,10,0,-1,1,30]],[2,4],[4,5,0,0,0],art=('A1',)))
    print('### BS Q14 BigM')
    print(run(['x1','x2','s1','s2','A1'],[[1,1,1,0,0,10],[-1,1,0,-1,1,2]],[2,4],[2,1,0,0,0],art=('A1',)))
    print('### BS Q15 dual: max 4y1+5y2; y1+2y2<=8; 3y1+y2<=9')
    print(run(['y1','y2','s1','s2'],[[1,2,1,0,8],[3,1,0,1,9]],[2,3],[4,5,0,0]))
