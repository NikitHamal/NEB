"""Wave 35 website finder: reads collegenp.com/college/<slug> pages for providers without a website (input /tmp/nosite.json, a list of provider rows). Keeps a page only when its title holds the distinctive name words and a Website field exists. Output: cnp_hits.json, then verified by fetching each site."""
import json, re, ssl, sys, html as H, urllib.request, time
from concurrent.futures import ThreadPoolExecutor
STOP={'college','campus','multiple','public','international','management','sciences','science','technology','and','of','the','for','higher','studies','pvt','ltd','institute','school','academy','education','university','degree','tribhuvan','affiliated','private','limited','center','centre','ctevt','nepal','memorial','technical','health','medical','hospital','teaching','nursing','polytechnic','vocational','secondary'}
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
def get(url,n=150000,t=12):
    try:
        req=urllib.request.Request(url,headers={'User-Agent':UA})
        with urllib.request.urlopen(req,timeout=t,context=ctx) as r:
            return r.geturl(), r.read(n).decode('utf-8','ignore')
    except Exception: return None,None
def slug(s): return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',s.lower())).strip('-')
def words(name):
    name=re.sub(r'\(.*?\)',' ',name)
    return [w for w in re.findall(r'[a-z]+',name.lower()) if w not in STOP and len(w)>2]
def cands(p):
    n=p['name']; base=re.sub(r'\(.*?\)','',n).strip(); abbr=re.findall(r'\(([A-Za-z]{2,8})\)',n)
    out=[slug(base),slug(n)]
    for a in abbr: out+= [slug(base)+'-'+a.lower(), slug(a)]
    out+=[slug(base)+'-'+slug(p['district']), slug(base.replace('and','&'))]
    return list(dict.fromkeys(x for x in out if x))
def work(p):
    ws=words(p['name'])
    if not ws: return None
    for c in cands(p):
        u,t=get('https://www.collegenp.com/college/'+c)
        if not t: continue
        mt=re.search(r'<title>(.*?)</title>',t,re.S); title=H.unescape(mt.group(1)).strip() if mt else ''
        low=re.sub(r'[^a-z ]',' ',title.lower())
        if not all(w in low for w in ws[:3]): continue
        site=re.search(r'<span class="cd-c-k">Website</span>\s*<span class="cd-c-v">(.*?)</span>',t,re.S)
        addr=re.search(r'<span class="cd-c-k">Address</span>\s*<span class="cd-c-v">(.*?)</span>',t,re.S)
        s=re.sub(r'<[^>]+>|\s+',' ',site.group(1)).strip() if site else ''
        a=re.sub(r'<[^>]+>|\s+',' ',addr.group(1)).strip() if addr else ''
        if s: return {'id':p['id'],'name':p['name'],'district':p['district'],'cn':c,'title':title,'addr':a,'site':s}
    return None
if __name__=='__main__':
    nos=json.load(open('/tmp/nosite.json'))
    with ThreadPoolExecutor(8) as ex: res=list(ex.map(work,nos))
    hits=[r for r in res if r]
    json.dump(hits,open('/tmp/w/cnp_hits.json','w'),indent=1)
    print(len(hits),'of',len(res))
