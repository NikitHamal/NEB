"""Scheduling / Banker / page-replacement helpers for the Operating System papers (ENCT 254)."""
from collections import deque

def stats(procs, ct):
    rows=[]
    for n,a,b in procs:
        tat=ct[n]-a; rows.append((n,a,b,ct[n],tat,tat-b))
    return rows

def sjf_np(procs):
    t=0; done={}; segs=[]; left=list(procs)
    while left:
        ready=[p for p in left if p[1]<=t]
        if not ready:
            t=min(p[1] for p in left); continue
        p=min(ready,key=lambda p:(p[2],p[1]))
        segs.append((p[0],t,t+p[2])); t+=p[2]; done[p[0]]=t; left.remove(p)
    return segs,stats(procs,done)

def srtf(procs):
    t=0; rem={n:b for n,a,b in procs}; done={}; segs=[]
    while len(done)<len(procs):
        ready=[(rem[n],a,n) for n,a,b in procs if a<=t and n not in done]
        if not ready: t+=1; continue
        _,_,n=min(ready)
        if segs and segs[-1][0]==n and segs[-1][2]==t: segs[-1]=(n,segs[-1][1],t+1)
        else: segs.append((n,t,t+1))
        rem[n]-=1; t+=1
        if rem[n]==0: done[n]=t
    return segs,stats(procs,done)

def hrrn(procs):
    t=0; done={}; segs=[]; left=list(procs); trace=[]
    while left:
        ready=[p for p in left if p[1]<=t]
        if not ready:
            t=min(p[1] for p in left); continue
        rr=[(((t-p[1])+p[2])/p[2],p) for p in ready]
        trace.append((t,[(p[0],round(r,3)) for r,p in rr]))
        r,p=max(rr,key=lambda x:(x[0],-x[1][1]))
        segs.append((p[0],t,t+p[2])); t+=p[2]; done[p[0]]=t; left.remove(p)
    return segs,stats(procs,done),trace

def rr(procs,q):
    procs=sorted(procs,key=lambda p:p[1])  # stable: listed order breaks ties
    t=0; rem={n:b for n,a,b in procs}; done={}; segs=[]; Q=deque(); i=0; n_=len(procs)
    def admit(upto):
        nonlocal i
        while i<n_ and procs[i][1]<=upto: Q.append(procs[i][0]); i+=1
    admit(0)
    while len(done)<n_:
        if not Q:
            t=procs[i][1]; admit(t); continue
        n=Q.popleft(); d=min(q,rem[n]); segs.append((n,t,t+d)); t+=d; rem[n]-=d; admit(t)
        if rem[n]==0: done[n]=t
        else: Q.append(n)
    return segs,stats(procs,done)

def avg(rows):
    return sum(r[4] for r in rows)/len(rows), sum(r[5] for r in rows)/len(rows)

def banker(alloc,mx,total):
    n=len(alloc); m=len(total)
    avail=[total[j]-sum(alloc[i][j] for i in range(n)) for j in range(m)]
    need=[[mx[i][j]-alloc[i][j] for j in range(m)] for i in range(n)]
    work=avail[:]; fin=[False]*n; order=[]; steps=[]
    while len(order)<n:
        for i in range(n):
            if not fin[i] and all(need[i][j]<=work[j] for j in range(m)):
                steps.append((i,work[:],need[i][:]))
                work=[work[j]+alloc[i][j] for j in range(m)]; fin[i]=True; order.append(i); break
        else: break
    return avail,need,order,steps,work

def fifo(refs,k):
    fr=[]; out=[]; f=0
    for r in refs:
        hit=r in fr
        if not hit:
            f+=1
            if len(fr)==k: fr.pop(0)
            fr.append(r)
        out.append((r,fr[:],hit))
    return out,f

def lru(refs,k):
    fr=[]; out=[]; f=0
    for r in refs:
        hit=r in fr
        if hit: fr.remove(r); fr.append(r)
        else:
            f+=1
            if len(fr)==k: fr.pop(0)
            fr.append(r)
        out.append((r,fr[:],hit))
    return out,f

def opt(refs,k):
    fr=[]; out=[]; f=0
    for idx,r in enumerate(refs):
        hit=r in fr
        if not hit:
            f+=1
            if len(fr)==k:
                fut={x:(refs[idx+1:].index(x) if x in refs[idx+1:] else 10**9) for x in fr}
                v=max(fr,key=lambda x:(fut[x],-fr.index(x)))
                fr[fr.index(v)]=r
            else: fr.append(r)
        out.append((r,fr[:],hit))
    return out,f

def trace_md(out,k):
    """markdown table: rows = reference, frames, fault"""
    hdr="| Ref | "+" | ".join(str(o[0]) for o in out)+" |"
    sep="|---|"+"---|"*len(out)
    lines=[hdr,sep]
    # frame rows keep slot positions for FIFO/OPT (list order) -- show as stack
    for s in range(k):
        cells=[ (str(o[1][s]) if s<len(o[1]) else "–") for o in out]
        lines.append(f"| Fr. {s+1} | "+" | ".join(cells)+" |")
    lines.append("| Fault | "+" | ".join("" if o[2] else "F" for o in out)+" |")
    return "\n".join(lines)

def gantt_code(segs,title=None,width=6.2):
    names=sorted({s[0] for s in segs}); 
    return f"segs={segs!r}\nfig,ax=plt.subplots(figsize=({width},1.35))\n"+(
"cols=[ACCENT,'#2a7a4b','#b46a00','#7a3fb0','#b00020','#0c7c8c']\n"
"names=sorted({s[0] for s in segs}); cm={n:cols[i%6] for i,n in enumerate(names)}\n"
"for n,a,b in segs:\n"
"    ax.barh(0,b-a,left=a,height=0.6,color=cm[n],alpha=0.85,edgecolor='white')\n"
"    ax.text((a+b)/2,0,n,ha='center',va='center',fontsize=8,color='white',fontweight='bold')\n"
"ts=sorted({s[1] for s in segs}|{s[2] for s in segs}); ax.set_xticks(ts); ax.tick_params(labelsize=7)\n"
"ax.set_yticks([]); ax.set_ylim(-0.5,0.5)\n"
"for sp_ in ('top','right','left'): ax.spines[sp_].set_visible(False)\n"
"fig.tight_layout()\n")
