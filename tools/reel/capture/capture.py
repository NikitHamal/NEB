"""Live captures from nebians.consica.com.np for the reel.

Chapter reader: one tall full-page screenshot at a phone viewport, scrolled by the stage.
3D labs: deterministic frame sequences. A virtual clock replaces performance.now, Date.now and
requestAnimationFrame before the page loads, so every frame is stepped exactly 1/30 s apart and
the WebGL sims render the same frames on any machine, however slow its software GL is.
"""
import argparse, asyncio, json, os, sys, time
from playwright.async_api import async_playwright

SITE = "https://nebians.consica.com.np"
GL_ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist",
           "--no-sandbox", "--disable-gpu-sandbox", "--disable-dev-shm-usage"]

UA = ("Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Mobile Safari/537.36")

VCLOCK = """
(() => {
  let now = 0, id = 0, cbs = new Map();
  const d0 = 1761200000000;
  performance.now = () => now;
  Date.now = () => d0 + now;
  window.requestAnimationFrame = (cb) => { cbs.set(++id, cb); return id; };
  window.cancelAnimationFrame = (i) => cbs.delete(i);
  window.__ixNoGovern = true;
  Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 16 });
  Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
  window.__step = (ms) => {
    now += ms;
    const run = [...cbs.values()]; cbs.clear();
    for (const f of run) { try { f(now); } catch (e) { console.error(e); } }
  };
})();
"""

CLEAN = """
const s = document.querySelector('#ix-sim-shell');
if (s) s.classList.add('ix-fake-fullscreen');
document.body.classList.add('ix-no-scroll');
const css = document.createElement('style');
css.textContent = `.ix-sim-dock,.ix-sim-toolbar,.ix-hud,#ix-fullscreen-btn,header,nav,.toast,[class*=cookie]{display:none!important}
#ix-sim-shell.ix-fake-fullscreen{position:fixed!important;inset:0!important;z-index:99999!important;border-radius:0!important}`;
document.head.appendChild(css);
"""

# At phone width the live reader keeps .rd-article at 760px (margin:auto makes the grid item fit its
# widest child), so lines are clipped on the right. Stretch it to the column for the capture.
READER_CSS = """*{animation:none!important;transition:none!important}
.rd-article{width:100%!important;max-width:100%!important;margin:0!important;justify-self:stretch!important}
.rd-body table,.rd-body .katex-display,.rd-body figure,.rd-body pre{max-width:100%!important;overflow-x:auto!important}
.rd-body img{max-width:100%!important;height:auto!important}
.rd-page>.st-crumbs{display:none!important}"""

HIDE_FIXED = """for (const e of document.querySelectorAll('body *')) {
  const p = getComputedStyle(e).position;
  if (p === 'fixed' || p === 'sticky') e.style.display = 'none';
}"""

SIMS = {
    "pendulum": ("/app/interactive/virtual-physics-lab/pendulum-lab/", "window.__pendulum && __pendulum.set(34, 1.2)"),
    "molecule": ("/app/interactive/virtual-chemistry-lab/molecule-gallery/", ""),
    "orbit": ("/app/interactive/solar-system-journey/earth-moon-and-sun/", ""),
}

def status():
    sys.path.insert(0, "/marimo/neb-reel")
    try:
        import status as st
        return st
    except Exception:
        return None

async def reader(pw, out):
    st = status()
    b = await pw.chromium.launch(args=GL_ARGS)
    ctx = await b.new_context(viewport={"width": 412, "height": 892}, device_scale_factor=2.5, user_agent=UA,
                              is_mobile=True, has_touch=True, color_scheme="light")
    page = await ctx.new_page()
    url = SITE + "/app/syllabus/11/physics/unit-14/"
    await page.goto(url, wait_until="networkidle", timeout=120000)
    await page.add_style_tag(content=READER_CSS)
    await page.evaluate(HIDE_FIXED)
    for y in range(0, 9000, 600):
        await page.evaluate(f"window.scrollTo(0,{y})")
        await page.wait_for_timeout(120)
    await page.evaluate("window.scrollTo(0,0)")
    await page.evaluate("document.fonts.ready")
    await page.wait_for_timeout(1500)
    await page.screenshot(path=os.path.join(out, "reader-full.png"), full_page=True)
    await page.screenshot(path=os.path.join(out, "reader-top.png"))
    h = await page.evaluate("document.documentElement.scrollHeight")
    await b.close()
    if st: st.log(f"Captured chapter reader (Class 11 Physics, unit 14), page height {h}px")

async def sim(pw, name, out, frames, fps, size):
    st = status()
    path, setup = SIMS[name]
    b = await pw.chromium.launch(args=GL_ARGS)
    ctx = await b.new_context(viewport={"width": size, "height": size}, device_scale_factor=2, user_agent=UA,
                              color_scheme="dark")
    await ctx.add_init_script(VCLOCK)
    page = await ctx.new_page()
    await page.goto(SITE + path, wait_until="domcontentloaded", timeout=120000)
    for _ in range(40):
        await page.evaluate("window.__step(16.667)")
        await page.wait_for_timeout(250)
        if await page.evaluate("!!document.querySelector('#sim-stage canvas, canvas')"):
            break
    await page.wait_for_timeout(3000)
    await page.evaluate(CLEAN)
    if setup:
        await page.evaluate(setup)
    for _ in range(30):
        await page.evaluate("window.__step(16.667)")
    d = os.path.join(out, name)
    os.makedirs(d, exist_ok=True)
    t0 = time.time()
    for i in range(frames):
        await page.evaluate(f"window.__step({1000 / fps})")
        await page.screenshot(path=os.path.join(d, f"{i:04d}.jpg"), type="jpeg", quality=92)
        if st and i % 15 == 0:
            st.progress(f"Capturing 3D lab: {name}", i, frames, fps=f"{(i + 1) / (time.time() - t0):.1f}")
    await b.close()
    if st: st.log(f"Captured {frames} frames of the {name} sim ({size * 2}px square)")

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/marimo/neb-reel/captures")
    ap.add_argument("--frames", type=int, default=120)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--size", type=int, default=480)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    async with async_playwright() as pw:
        jobs = []
        if a.only in ("", "reader"):
            jobs.append(reader(pw, a.out))
        for n in SIMS:
            if a.only in ("", n):
                jobs.append(sim(pw, n, a.out, a.frames, a.fps, a.size))
        await asyncio.gather(*jobs)

if __name__ == "__main__":
    asyncio.run(main())
