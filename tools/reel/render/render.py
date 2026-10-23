#!/usr/bin/env python3
"""Render the NEBians v1.7 reel from tools/reel/stage with headless Chromium.

    python tools/reel/render/render.py --out tools/reel/out                    # 1080x1920, 60 fps
    python tools/reel/render/render.py --out /tmp/sheet --scale 0.5 --every 30 # quick check
    python tools/reel/render/render.py --dump-cues tools/reel/out/cues.json   # cue sheet for audio.py

Each worker opens the stage, waits for window.__ready, then for every frame calls window.__seek(t)
and screenshots the viewport. Frames inside window.FAST (whips, slams) are rendered as four
sub-frames across a 0.9-frame shutter and averaged: that is the motion blur.
"""
import argparse, asyncio, functools, http.server, io, json, os, socketserver, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
STAGE = "/tools/reel/stage/index.html"
ARGS = ["--no-sandbox", "--disable-gpu-sandbox", "--disable-dev-shm-usage", "--force-color-profile=srgb",
        "--font-render-hinting=none", "--disable-lcd-text", "--hide-scrollbars"]
SUB = [-0.375, -0.125, 0.125, 0.375]
SHUTTER = 0.9


def status():
    d = os.environ.get("NEB_REEL_STATUS_DIR", "/marimo/neb-reel")
    if not os.path.exists(os.path.join(d, "status.py")):
        return None
    sys.path.insert(0, d)
    import status as st
    return st


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve(root):
    handler = functools.partial(QuietHandler, directory=root)
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


async def open_stage(pw, url, scale):
    b = await pw.chromium.launch(args=ARGS)
    ctx = await b.new_context(viewport={"width": 1080, "height": 1920}, device_scale_factor=scale)
    page = await ctx.new_page()
    page.on("console", lambda m: m.type == "error" and print("[stage]", m.text, file=sys.stderr))
    page.on("pageerror", lambda e: print("[stage error]", e, file=sys.stderr))
    await page.goto(url, wait_until="load")
    info = await page.evaluate("window.__ready")
    fast = await page.evaluate("window.FAST")
    return b, page, info, fast


def in_fast(t, fast):
    return any(a <= t < b for a, b in fast)


def average(shots):
    acc = None
    for s in shots:
        a = np.asarray(Image.open(io.BytesIO(s)).convert("RGB"), dtype=np.float32)
        acc = a if acc is None else acc + a
    return Image.fromarray(np.clip(acc / len(shots) + 0.5, 0, 255).astype(np.uint8))


async def worker(pw, url, args, queue, out, fps, pool, stats):
    b, page, info, fast = await open_stage(pw, url, args.scale)
    loop = asyncio.get_running_loop()
    while True:
        try:
            chunk = queue.get_nowait()
        except asyncio.QueueEmpty:
            break
        for i in chunk:
            t = i / fps
            path = os.path.join(out, f"f_{i:05d}.jpg")
            if args.blur and in_fast(t, fast):
                shots = []
                for o in SUB:
                    await page.evaluate(f"window.__seek({max(0.0, t + o * SHUTTER / fps):.6f})")
                    shots.append(await page.screenshot(type="jpeg", quality=96))
                img = await loop.run_in_executor(pool, average, shots)
                await loop.run_in_executor(pool, functools.partial(img.save, path, quality=95, subsampling=0))
            else:
                await page.evaluate(f"window.__seek({t:.6f})")
                shot = await page.screenshot(type="jpeg", quality=95)
                await loop.run_in_executor(pool, lambda p=path, s=shot: open(p, "wb").write(s))
            stats["done"] += 1
    await b.close()


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "tools/reel/out/frames"))
    ap.add_argument("--workers", type=int, default=min(16, (os.cpu_count() or 4) - 2))
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--every", type=int, default=1)
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--no-blur", dest="blur", action="store_false")
    ap.add_argument("--dump-cues", default=None)
    ap.add_argument("--times", default=None, help="comma-separated seconds to render instead of a range")
    args = ap.parse_args()
    srv = serve(REPO)
    url = f"http://127.0.0.1:{srv.server_address[1]}{STAGE}"
    st = status()
    async with async_playwright() as pw:
        if args.dump_cues:
            b, page, info, _ = await open_stage(pw, url, 0.25)
            cues = await page.evaluate("window.__cues()")
            os.makedirs(os.path.dirname(os.path.abspath(args.dump_cues)), exist_ok=True)
            json.dump({"duration": info["duration"], "cues": cues}, open(args.dump_cues, "w"), indent=1)
            await b.close()
            print(f"{len(cues)} cues -> {args.dump_cues}")
            return
        os.makedirs(args.out, exist_ok=True)
        b, page, info, _ = await open_stage(pw, url, 0.25)
        await b.close()
        end = args.end if args.end is not None else info["duration"]
        frames = list(range(int(round(args.start * args.fps)), int(round(end * args.fps)), args.every))
        if args.times:
            frames = [int(round(float(x) * args.fps)) for x in args.times.split(",")]
        size = 24 if args.every == 1 else 1
        queue = asyncio.Queue()
        for k in range(0, len(frames), size):
            queue.put_nowait(frames[k:k + size])
        stats = {"done": 0}
        pool = ThreadPoolExecutor(max(4, args.workers))
        t0 = time.time()
        jobs = [asyncio.create_task(worker(pw, url, args, queue, args.out, args.fps, pool, stats)) for _ in range(args.workers)]
        while not all(j.done() for j in jobs):
            await asyncio.sleep(2)
            el = time.time() - t0
            rate = stats["done"] / el if el else 0
            eta = (len(frames) - stats["done"]) / rate if rate else 0
            print(f"{stats['done']}/{len(frames)} frames  {rate:.1f} fps  eta {eta:.0f}s", flush=True)
            if st:
                st.progress("Rendering frames", stats["done"], len(frames), speed=f"{rate:.1f} fps", eta=f"{eta:.0f}s",
                            workers=args.workers)
        for j in jobs:
            j.result()
        print(f"rendered {len(frames)} frames in {time.time() - t0:.1f}s -> {args.out}")


if __name__ == "__main__":
    asyncio.run(main())
