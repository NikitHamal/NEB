// Landing check: screenshots (desktop/mobile x light/dark) + toggle behaviour.
//   PW_DIR=/tmp/pw node tools/design/landing.mjs [outdir]
import fs from 'node:fs';
import { createRequire } from 'node:module';
const { chromium } = createRequire((process.env.PW_DIR || process.cwd()) + '/')('playwright');
const out = process.argv[2] || '/tmp/shots-landing'; fs.mkdirSync(out, { recursive: true });
const base = process.env.BASE || 'http://127.0.0.1:8000';
const b = await chromium.launch();
for (const vp of [{ n: 'desktop', w: 1366, h: 850 }, { n: 'mobile', w: 390, h: 844, mobile: true }]) {
  for (const theme of ['light', 'dark']) {
    const ctx = await b.newContext({ viewport: { width: vp.w, height: vp.h }, isMobile: !!vp.mobile, hasTouch: !!vp.mobile });
    await ctx.addInitScript((t) => { if (!sessionStorage.getItem('seeded')) { localStorage.setItem('theme', t); sessionStorage.setItem('seeded', '1'); } }, theme);
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
    await p.goto(base + '/', { waitUntil: 'load' }); await p.waitForTimeout(1500);
    await p.screenshot({ path: `${out}/hero-${vp.n}-${theme}.png` });
    await p.evaluate(() => document.querySelectorAll('[data-reveal],.foot-word').forEach((e) => e.classList.add('in')));
    await p.waitForTimeout(1200);
    await p.screenshot({ path: `${out}/full-${vp.n}-${theme}.png`, fullPage: true });
    const before = await p.evaluate(() => document.documentElement.dataset.theme);
    await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(300);
    await p.click('[data-theme-toggle]'); await p.waitForTimeout(1100);
    const after = await p.evaluate(() => ({ t: document.documentElement.dataset.theme, ls: localStorage.getItem('theme'), pressed: document.querySelector('[data-theme-toggle]').getAttribute('aria-pressed') }));
    console.log(vp.n, theme, 'start', before, '-> click ->', JSON.stringify(after), errs.length ? 'ERRORS ' + errs : 'no js errors');
    await p.screenshot({ path: `${out}/toggled-${vp.n}-${theme}.png` });
    await ctx.close();
  }
}
await b.close();
