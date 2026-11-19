import re,html,json,urllib.request,ssl
from concurrent.futures import ThreadPoolExecutor
def get(i):
    u=f'https://npca.edu.np/campus_details/{i}'
    for a in range(2):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25)
            t=r.read().decode('utf8','ignore'); break
        except urllib.error.HTTPError as e:
            return i,None
        except Exception: t=None
    if not t: return i,'ERR'
    s=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    s=re.sub(r'<[^>]+>','\n',s); s=html.unescape(s)
    L=[l.strip() for l in s.split('\n') if l.strip()]
    try:
        k=L.index('Press Releases'); name=L[k+2]; addr=L[k+3]
    except Exception: return i,None
    rec={'id':i,'name':name,'addr':addr}
    if 'Campus Details' in L:
        j=L.index('Campus Details'); seg=L[j+1:j+16]
        for key in ('Established Date','Contact Number','QAA Status','Website'):
            if key in seg: rec[key]=seg[seg.index(key)+1]
    if 'Offered Programs' in L:
        a=L.index('Offered Programs'); b=L.index('Campus Details') if 'Campus Details' in L else a+60
        pr=L[a+1:b]; rec['progs']=[(pr[n],pr[n+1]) for n in range(0,len(pr)-1,2)][:30]
    return i,rec
import sys
lo,hi=int(sys.argv[1]),int(sys.argv[2])
with ThreadPoolExecutor(16) as ex: out=list(ex.map(get,range(lo,hi)))
ok=[r for i,r in out if isinstance(r,dict)]
errs=[i for i,r in out if r=='ERR']
none=[i for i,r in out if r is None]
json.dump(ok,open(f'/tmp/npca_{lo}_{hi}.json','w'),ensure_ascii=False)
print(len(ok),'ok',len(errs),'err',len(none),'404/none; max ok id',max([r['id'] for r in ok]) if ok else None)
