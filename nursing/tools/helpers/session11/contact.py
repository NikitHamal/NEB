import sys,glob,os
from PIL import Image, ImageDraw
d=sys.argv[1]; fs=sorted(glob.glob(f'/tmp/NEB/notes/assets/{d}/*.jpg')+glob.glob(f'/tmp/NEB/notes/assets/{d}/*.png'))
only=sys.argv[3:] 
if only: fs=[f for f in fs if os.path.splitext(os.path.basename(f))[0] in only]
n=len(fs); cols=4; rows=(n+cols-1)//cols; W=300
sheet=Image.new('RGB',(cols*W,rows*(W+20)),'white'); dr=ImageDraw.Draw(sheet)
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGB'); im.thumbnail((W-6,W-6)); x=(i%cols)*W; y=(i//cols)*(W+20)
    sheet.paste(im,(x+3,y+20)); dr.text((x+4,y+4),os.path.basename(f)[:40],fill='black')
sheet.save(sys.argv[2])
