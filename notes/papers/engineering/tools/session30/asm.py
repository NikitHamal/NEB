import re, sys
exec(open('/app/shots/figs_ec2.py').read())
F['zen'] = ZEN
exec(open('/app/shots/figs_cad.py').read())
for _k,_v in G.items(): F[_k]=_v
exec(open('/app/shots/snips.py').read())
DEFCAP={'c_canal_fill':'Typical canal section in complete fill (embankment).','c_canal_cut':'Typical canal section in complete cut.','c_road_fill':'Typical hill-road section in complete fill.','c_road_cutfill':'Typical hill-road section in partial cut and fill.','c_cantilever4':'Typical 4 m cantilever retaining wall with dimensions and details.'}
F['q6mos2'] = F['q6mos2'].replace('"%s"', '""')
q=F['q3load']; q=q.split("b=fig.add_axes")[0].replace("fig=plt.figure(figsize=(7.2,2.9))\nax=fig.add_axes([0.0,0.0,0.46,1.0]); ","fig,ax=ckt_canvas(3.6,3.3); ")
F['q3ckt']=q
C = '/app/notes/papers/engineering/content/'
ex = open(C + 'ioe-ex151-2081-ashwin.md').read().split('\n')

PRE = """def _w(f):
    def g(ax,a,b,text=None,side=1,**kw):
        if text and abs(a[0]-b[0])<1e-6:
            f(ax,a,b,None,side=side,**{k:v for k,v in kw.items() if k!='off'})
            u=np.array([b[0]-a[0],b[1]-a[1]],float); u/=np.hypot(*u); v=np.array([-u[1],u[0]])*side
            m=np.array([(a[0]+b[0])/2,(a[1]+b[1])/2])+v*0.5
            ax.text(m[0],m[1],text,ha='left' if v[0]>0 else 'right',va='center',fontsize=8)
        else: f(ax,a,b,text,side=side,**kw)
    return g
res=_w(res); cap=_w(cap); ind=_w(ind); diode=_w(diode); vsrc=_w(vsrc); acsrc=_w(acsrc); batt=_w(batt); isrc=_w(isrc)
"""

def fig(m):
    parts = m.group(1).split('|')
    name = parts[0].strip(); cap = parts[1].strip() if len(parts) > 1 else ''
    code = PRE + (CPRE if name.startswith('c_') else '') + F[name]
    if not cap: cap = DEFCAP.get(name,'')
    cap = cap.replace('"','')
    if len(parts) > 2:
        for kv in parts[2].split(';'):
            k, v = kv.split('=', 1); code = code.replace('__' + k.strip() + '__', v.strip())
    return '```figure caption="%s"\n%s```' % (cap, code)

def inc(m):
    a, b = int(m.group(1)), int(m.group(2))
    return '\n'.join(ex[a - 1:b])

for pid in sys.argv[1:]:
    t = open('/app/shots/src/%s.md' % pid).read()
    t = re.sub(r'%%SNIP (\w+)%%', lambda m: S[m.group(1)], t)
    t = re.sub(r'%%FIG (.*?)%%', fig, t)
    t = re.sub(r'%%INC (\d+) (\d+)%%', inc, t)
    open(C + pid + '.md', 'w').write(t)
    print('wrote', pid, len(t))
