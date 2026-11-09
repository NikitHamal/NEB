import sys,re
def split_top(s):
    out=[];d=0;i=0;last=0
    while i<len(s):
        c=s[i]
        if c=='{':d+=1
        elif c=='}':d-=1
        elif d==0 and s.startswith('\\qquad',i):
            out.append(s[last:i]);i+=6;last=i;continue
        i+=1
    out.append(s[last:]);return out
for p in sys.argv[1:]:
    L=open(p,encoding='utf-8').read().split('\n');n=0
    for k,l in enumerate(L):
        m=re.match(r'^\$\$(.*)\$\$$',l)
        if m and '\\begin' not in l and '\\qquad' in l:
            parts=[x.strip().rstrip(',').strip() for x in split_top(m.group(1))]
            parts=[x for x in parts if x]
            if len(parts)>1:
                L[k]='$$\\begin{gathered}'+' \\\\ '.join(parts)+'\\end{gathered}$$';n+=1
    open(p,'w',encoding='utf-8').write('\n'.join(L));print(p,n)
