import sys,glob,os
from PIL import Image, ImageDraw
fs=sorted(glob.glob('/tmp/NEB/notes/assets/nur7/*.*'))
W=300; cols=5; rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(W*cols,(W+18)*rows),'white'); d=ImageDraw.Draw(S)
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGB'); im.thumbnail((W,W)); x=(i%cols)*W; y=(i//cols)*(W+18)
    S.paste(im,(x,y+18)); d.text((x+4,y+3),os.path.basename(f)+" %dx%d"%Image.open(f).size,fill='black')
S.save('/tmp/shots/sheet.png'); print(len(fs))
