import pymupdf,glob,sys
from PIL import Image
d=pymupdf.open(glob.glob('/tmp/NEB/nursing/pdfs/*Family-and-Reproductive*.pdf')[0])
keys=sys.argv[3:]; dpi=int(sys.argv[2]); pages=[]
for k in keys:
    for i,p in enumerate(d):
        if i+1 in pages: continue
        if k in p.get_text(): pages.append(i+1); break
print(pages)
ims=[]
for p in pages:
    pm=d[p-1].get_pixmap(dpi=dpi); ims.append(Image.frombytes('RGB',(pm.width,pm.height),pm.samples))
w,h=ims[0].size; cols=2; rows=(len(ims)+1)//2
s=Image.new('RGB',(w*cols,h*rows),'white')
for i,im in enumerate(ims): s.paste(im,((i%2)*w,(i//2)*h))
s.save(sys.argv[1])
