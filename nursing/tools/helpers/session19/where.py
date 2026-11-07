import pymupdf,glob,sys
d=pymupdf.open(glob.glob('/tmp/NEB/nursing/pdfs/*Family-and-Reproductive*.pdf')[0])
keys=sys.argv[1:]
for i,p in enumerate(d):
    t=p.get_text()
    for k in keys:
        if k in t: print(i+1,k)
