import sys

import numpy as np
import skia
from PIL import Image

import film
from kit import H, W

times = [float(x) for x in sys.argv[2:]] or [0.4, 1.5, 2.6, 3.6, 5.8, 7.4, 9.2, 10.6, 12.2, 13.6, 15.6, 17.4]
out = sys.argv[1]
tiles = []
for t in times:
    s = skia.Surface(W, H)
    film.frame(s.getCanvas(), t)
    tiles.append(Image.fromarray(s.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]).resize((640, 360)))
cols = 3
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 644, rows * 364), "black")
for i, im in enumerate(tiles):
    sheet.paste(im, ((i % cols) * 644, (i // cols) * 364))
sheet.save(out)
