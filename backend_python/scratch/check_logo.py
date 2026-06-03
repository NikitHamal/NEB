import os
from PIL import Image

img_path = r"f:\NEB\backend_python\web\static\web\img\n-logo-512.png"
if os.path.exists(img_path):
    img = Image.open(img_path)
    print(f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}")
    bbox = img.getbbox()
    print(f"Bounding Box: {bbox}")
    # bbox format: (left, upper, right, lower)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    print(f"Visible dimensions: {w}x{h}")
else:
    print("Logo file not found!")
