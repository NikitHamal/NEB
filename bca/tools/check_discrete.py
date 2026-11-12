"""Recompute the numeric answers of the Discrete Structure book. Run: python3 check_discrete.py"""
import itertools, math, heapq
from math import comb, perm, factorial, gcd
ok=True
def chk(label,a,b):
    global ok
    r = a==b or (isinstance(a,float) and abs(a-b)<1e-9)
    if not r: ok=False
    print("ok  " if r else "FAIL",label,a if r else (a,b))
# logic
rows=[(p,q,r) for p in (1,0) for q in (1,0) for r in (1,0)]
f=lambda p,q,r: ((not p) or q) and ((not q) or r)
chk("U1Q1 true rows",sum(1 for x in rows if f(*x)),4)
chk("hyp syllogism taut",all((not(((not p) or q) and ((not q) or r))) or ((not p) or r) for p,q,r in rows),True)
# sets/relations
chk("neither",60-(35+28-10),7)
n=3; chk("relations",2**(n*n),512); chk("reflexive",2**(n*n-n),64); chk("symmetric",2**(n*(n+1)//2),64)
chk("onto 4->3",sum((-1)**k*comb(3,k)*(3-k)**4 for k in range(4)),36)
# counting
chk("pwd",26**3*100,1757600); chk("bitstr",128+64-32,160)
chk("banana",factorial(6)//(factorial(3)*factorial(2)),60)
chk("mississippi",factorial(11)//(factorial(4)*factorial(4)*factorial(2)),34650)
chk("committee",comb(9,3)-comb(5,3),74); chk("solutions",comb(12,2),66); chk("solutions>=1",comb(9,2),36)
chk("poker",comb(52,5),2598960); chk("lottery",comb(40,6),3838380)
chk("ie100",sum(1 for i in range(1,101) if i%2==0 or i%3==0 or i%5==0),74)
D=lambda n: round(factorial(n)*sum((-1)**k/factorial(k) for k in range(n+1)))
chk("D4",D(4),9); chk("D5",D(5),44)
chk("coef 2x+y",comb(5,2)*4,40); chk("coef (1+2x)^6",comb(6,4)*16,240); chk("coef x+3y",comb(5,2)*9,90)
chk("div4or6",sum(1 for i in range(1,201) if i%4==0 or i%6==0),67)
chk("4digit",9*8*7*6,3024)
chk("bday23",round(1-math.prod((365-i)/365 for i in range(23)),3),0.507)
chk("pin",round(1-(10*9*8*7)/10**4,3),0.496)
chk("circular apart",factorial(7)-factorial(6)*2,3600)
chk("3 heads of 5",comb(5,3)/32,0.3125)
# recurrences
a=[1,0]
for i in range(2,10): a.append(5*a[-1]-6*a[-2])
chk("rec1",all(a[i]==3*2**i-2*3**i for i in range(10)),True)
b=[1,3]
for i in range(2,10): b.append(4*b[-1]-4*b[-2])
chk("rec2",all(b[i]==(2+i)*2**i//2 for i in range(10)),True)
c=[2,3]
for i in range(2,10): c.append(3*c[-1]-2*c[-2])
chk("rec3",all(c[i]==1+2**i for i in range(10)),True)
d=[1,6]
for i in range(2,10): d.append(6*d[-1]-9*d[-2])
chk("rec4",all(d[i]==(1+i)*3**i for i in range(10)),True)
e=[1]
for i in range(1,10): e.append(2*e[-1]+3)
chk("rec5",all(e[i]==2**(i+2)-3 for i in range(10)),True)
chk("no 11 strings n=6",sum(1 for s in itertools.product("01",repeat=6) if "11" not in "".join(s)),21)
# graphs
E={('A','B'):4,('A','C'):2,('B','C'):1,('B','D'):5,('C','D'):8,('C','E'):10,('D','E'):2,('D','F'):6,('E','F'):3}
adj={}
for (u,v),w in E.items(): adj.setdefault(u,[]).append((v,w)); adj.setdefault(v,[]).append((u,w))
def dijk(adj,s):
    dist={s:0}; pq=[(0,s)]
    while pq:
        d,u=heapq.heappop(pq)
        if d>dist[u]: continue
        for v,w in adj[u]:
            if d+w<dist.get(v,1e9): dist[v]=d+w; heapq.heappush(pq,(d+w,v))
    return dist
chk("dijkstra",dijk(adj,'A'),{'A':0,'C':2,'B':3,'D':8,'E':10,'F':13})
par={x:x for x in adj}
def find(x):
    while par[x]!=x: par[x]=par[par[x]]; x=par[x]
    return x
w=0
for (u,v),wt in sorted(E.items(),key=lambda kv:kv[1]):
    if find(u)!=find(v): par[find(u)]=find(v); w+=wt
chk("kruskal",w,13)
E2={('S','A'):7,('S','B'):2,('B','A'):3,('A','C'):1,('B','C'):8,('C','T'):2,('A','T'):6}
adj2={}
for (u,v),wt in E2.items(): adj2.setdefault(u,[]).append((v,wt)); adj2.setdefault(v,[]).append((u,wt))
chk("dijkstra2 T",dijk(adj2,'S')['T'],8)
par={x:x for x in adj2}; w=0
for (u,v),wt in sorted(E2.items(),key=lambda kv:kv[1]):
    if find(u)!=find(v): par[find(u)]=find(v); w+=wt
chk("kruskal2",w,8)
g={'A':['B','C'],'B':['A','D'],'C':['A','D','E'],'D':['B','C','F'],'E':['C','F'],'F':['D','E']}
from collections import deque
q=deque(['A']); seen=['A']
while q:
    u=q.popleft()
    for v in g[u]:
        if v not in seen: seen.append(v); q.append(v)
chk("bfs",seen,list("ABCDEF"))
order=[]
def dfs(u):
    order.append(u)
    for v in g[u]:
        if v not in order: dfs(v)
dfs('A'); chk("dfs",order,list("ABDCEF"))
g2={'A':['B','D'],'B':['A','C'],'C':['B','D','E'],'D':['A','C'],'E':['C']}
q=deque(['A']); seen=['A']
while q:
    u=q.popleft()
    for v in g2[u]:
        if v not in seen: seen.append(v); q.append(v)
order=[]
def dfs2(u):
    order.append(u)
    for v in g2[u]:
        if v not in order: dfs2(v)
dfs2('A'); chk("bfs2",seen,list("ABDCE")); chk("dfs2",order,list("ABCDE"))
chk("huffman",round(.45*1+.12*3+.13*3+.16*3+.05*4+.09*4,2),2.24)
chk("hamilton K5",factorial(4)//2,12)
# number theory
def egcd(a,b):
    if b==0: return a,1,0
    g,x,y=egcd(b,a%b); return g,y,x-(a//b)*y
chk("gcd252",egcd(252,105)[0],21); g_,x,y=egcd(105,252); chk("bezout",105*x+252*y,21)
g_,x,y=egcd(1071,462); chk("1071,462",(g_,1071*x+462*y),(21,21))
chk("inv7 mod26",pow(7,-1,26),15); chk("inv3 mod7",pow(3,-1,7),5); chk("inv5 mod17",pow(5,-1,17),7)
chk("last digit 7^222",pow(7,222,10),9); chk("2^100 mod 7",pow(2,100,7),2); chk("3^13 mod 7",pow(3,13,7),3)
chk("3^100 mod100",pow(3,100,100),1); chk("7^100 mod13",pow(7,100,13),9)
chk("crt1",[x for x in range(105) if x%3==2 and x%5==3 and x%7==2],[23])
chk("crt2",[x for x in range(36) if x%4==1 and x%9==2],[29])
n,phi=61*53,60*52; chk("rsa d",pow(17,-1,phi),2753); chk("rsa enc",pow(65,17,n),2790); chk("rsa dec",pow(2790,2753,n),65)
chk("rsa2",(55,pow(7,-1,40),pow(8,7,55),pow(2,23,55)),(55,23,2,8))
chk("123*456 mod 11",(123*456)%11,10)
print("ALL OK" if ok else "SOME FAILED")
