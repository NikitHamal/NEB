"""Contact sheet of a rendered video: python3 contact.py video.mp4 out.png [count] [start] [end]"""
import subprocess, sys, json
from PIL import Image

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",p],capture_output=True,text=True).stdout)

def sheet(video, out, n=12, a=0.0, b=None, cols=3, w=640):
    b = b or dur(video)
    tiles = []
    for i in range(n):
        t = a + (b - a) * (i + 0.5) / n
        f = f"/tmp/_cs_{i}.png"
        subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t:.2f}","-i",video,"-frames:v","1","-vf",f"scale={w}:-2",f], check=True)
        tiles.append((t, Image.open(f).convert("RGB")))
    h = tiles[0][1].size[1]
    rows = (n + cols - 1) // cols
    sh = Image.new("RGB", (cols * (w + 4), rows * (h + 4)), "black")
    for i, (t, im) in enumerate(tiles):
        sh.paste(im, ((i % cols) * (w + 4), (i // cols) * (h + 4)))
    sh.save(out)
    print([round(t, 1) for t, _ in tiles])

if __name__ == "__main__":
    a = sys.argv
    sheet(a[1], a[2], int(a[3]) if len(a) > 3 else 12, float(a[4]) if len(a) > 4 else 0.0, float(a[5]) if len(a) > 5 else None)
