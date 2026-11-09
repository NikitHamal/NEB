import sys,re
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','pipeline'))
import mathsvg
t=open(sys.argv[1]).read()
for m in re.finditer(r'\$\$(.+?)\$\$|\$([^$\n]+?)\$',t,re.S):
    x=m.group(1) or m.group(2)
    mathsvg.render(x,display=bool(m.group(1)))
print(len(mathsvg.FAILS),'fails',len(mathsvg.OVERWIDE),'overwide')
for a,b in mathsvg.FAILS: print(repr(a[:90]),'|',b[:60])
for a,b in mathsvg.OVERWIDE: print('WIDE',a[:60],b)
