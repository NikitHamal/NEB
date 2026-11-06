#!/usr/bin/env python3
"""tile.py out.png dpi p1 p2 p3 p4 : tile PDF pages (1-based) into a 2x2 contact image"""
import sys,glob,pymupdf
from PIL import Image
f=glob.glob('/tmp/NEB/nursing/pdfs/*Midwifery-II.pdf')[0]; d=pymupdf.open(f); out,dpi=sys.argv[1],int(sys.argv[2]); ps=[int(x) for x in sys.argv[3:]]
ims=[]
for p in ps:
    pm=d[p-1].get_pixmap(dpi=dpi); ims.append(Image.frombytes('RGB',(pm.width,pm.height),pm.samples))
w,h=ims[0].size; cols=2 if len(ims)>1 else 1; rows=(len(ims)+cols-1)//cols
s=Image.new('RGB',(w*cols,h*rows),'white')
for i,im in enumerate(ims): s.paste(im,((i%cols)*w,(i//cols)*h))
s.save(out)
