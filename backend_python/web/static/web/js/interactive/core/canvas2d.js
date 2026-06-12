export function createCanvas2D(stage, opts = {}) {
  const canvas = document.createElement('canvas');
  canvas.className = 'ix-sim-canvas';
  stage.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  const dprCap = opts.dprCap || 2;
  let width = 0;
  let height = 0;
  let dpr = 1;
  let updateFn = null;
  let running = false;
  let visible = true;
  let pageVisible = !document.hidden;
  let rafId = 0;
  let disposed = false;
  let last = 0;
  const resizeFns = [];

  function resize() {
    width = stage.clientWidth || 1;
    height = stage.clientHeight || 1;
    dpr = Math.min(window.devicePixelRatio || 1, dprCap);
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    resizeFns.forEach((fn) => fn(width, height));
  }

  const ro = new ResizeObserver(() => resize());
  ro.observe(stage);
  resize();

  const io = new IntersectionObserver((entries) => {
    visible = entries[0] ? entries[0].isIntersecting : true;
    syncLoop();
  }, { threshold: 0.01 });
  io.observe(stage);

  function onVisibility() {
    pageVisible = !document.hidden;
    syncLoop();
  }
  document.addEventListener('visibilitychange', onVisibility);

  function frame(t) {
    rafId = requestAnimationFrame(frame);
    const dt = Math.min((t - last) / 1000 || 0.016, 0.1);
    last = t;
    if (updateFn) updateFn(ctx, dt, width, height);
  }

  function syncLoop() {
    const shouldRun = running && visible && pageVisible && !disposed;
    if (shouldRun && !rafId) {
      last = performance.now();
      rafId = requestAnimationFrame(frame);
    } else if (!shouldRun && rafId) {
      cancelAnimationFrame(rafId);
      rafId = 0;
    }
  }

  return {
    canvas,
    ctx,
    get width() { return width; },
    get height() { return height; },
    setUpdate(fn) { updateFn = fn; },
    onResize(fn) { resizeFns.push(fn); fn(width, height); },
    start() { running = true; syncLoop(); },
    stop() { running = false; syncLoop(); },
    renderOnce() { if (updateFn) updateFn(ctx, 0.016, width, height); },
    dispose() {
      disposed = true;
      running = false;
      syncLoop();
      ro.disconnect();
      io.disconnect();
      document.removeEventListener('visibilitychange', onVisibility);
      if (canvas.parentNode) canvas.parentNode.removeChild(canvas);
    },
  };
}

export function pointerPos(canvas, e) {
  const rect = canvas.getBoundingClientRect();
  return { x: e.clientX - rect.left, y: e.clientY - rect.top };
}
