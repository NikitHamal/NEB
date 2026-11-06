#!/bin/bash
cd /tmp/NEB; P=/tmp/v/bin/python
$P nursing/tools/nebpdf.py course/year-2/nursing-concepts 2>&1 | grep -E "pages=|failures|fail"
$P - "$@" <<'PY'
import pymupdf,sys,glob
f=glob.glob('/tmp/NEB/nursing/pdfs/*Nursing-Concepts*.pdf')[0]
d=pymupdf.open(f)
for k in sys.argv[1:]:
    for i,p in enumerate(d):
        r=[x for x in p.search_for(k) if x.y0>60]
        if r:
            y=r[0].y0; clip=pymupdf.Rect(30,max(0,y-330),p.rect.width-30,min(p.rect.height,y+40))
            p.get_pixmap(clip=clip,dpi=100).save('/tmp/shots/pl_'+k.replace(' ','_').rstrip('.')+'.png'); print(k,'page',i+1); break
PY
