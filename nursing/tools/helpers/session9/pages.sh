#!/bin/bash
# pages.sh "Plate 2.2" "Plate 2.4" ... : crop plates from fresh PDF into /tmp/shots/pl_*.png
cd /tmp/NEB; P=/tmp/v/bin/python
$P nursing/tools/nebpdf.py course/year-2/psychiatric-nursing 2>&1 | grep -E "pages=|failures"
$P - "$@" <<'PY'
import pymupdf,sys
d=pymupdf.open('/tmp/NEB/nursing/pdfs/NEBians-BScNursing-Year-2-Psychiatric-Nursing.pdf')
for k in sys.argv[1:]:
    for i,p in enumerate(d):
        r=[x for x in p.search_for(k) if x.y0>60]
        if r:
            y=r[0].y0; clip=pymupdf.Rect(30,max(0,y-330),p.rect.width-30,min(p.rect.height,y+40))
            p.get_pixmap(clip=clip,dpi=110).save('/tmp/shots/pl_'+k.replace(' ','_').rstrip('.')+'.png'); print(k,'page',i+1); break
PY
