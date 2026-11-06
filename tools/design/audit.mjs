// Visual + contrast audit for the Django site.
//   node tools/design/audit.mjs [--cookie SESSIONID] [--base http://127.0.0.1:8000] [--out /tmp/shots] [--min 3] path[,path...]
// Needs `npm i playwright` in PW_DIR (default: cwd) and a running server.
import fs from 'node:fs';
import { createRequire } from 'node:module';
const { chromium } = createRequire((process.env.PW_DIR || process.cwd()) + '/')('playwright');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const base = opt('--base', 'http://127.0.0.1:8000');
const out = opt('--out', '/tmp/shots');
const min = parseFloat(opt('--min', '3'));
const shots = !args.includes('--no-shots');
const cookie = opt('--cookie', '');
const paths = (args.filter((a, i) => !a.startsWith('--') && !['--base', '--out', '--min', '--cookie'].includes(args[i - 1]))[0] || '/').split(',');
fs.mkdirSync(out, { recursive: true });

const probe = () => {
  const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p[3] ?? 1 }; };
  const lum = ({ r, g, b }) => { const f = (v) => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
  const over = (top, bot) => { const a = top.a + bot.a * (1 - top.a); if (!a) return { r: 0, g: 0, b: 0, a: 0 }; const k = (t, b) => (t * top.a + b * bot.a * (1 - top.a)) / a; return { r: k(top.r, bot.r), g: k(top.g, bot.g), b: k(top.b, bot.b), a }; };
  const pageBg = parse(getComputedStyle(document.documentElement).backgroundColor) ; 
  const root = (pageBg && pageBg.a) ? pageBg : (parse(getComputedStyle(document.body).backgroundColor) || { r: 255, g: 255, b: 255, a: 1 });
  const bgOf = (el) => { const chain = []; for (let e = el; e; e = e.parentElement) { const cs = getComputedStyle(e); const c = parse(cs.backgroundColor); if (cs.backgroundImage !== 'none') return null; if (c && c.a > 0) { chain.push(c); if (c.a >= 1) break; } } let acc = root.a ? { ...root, a: 1 } : { r: 255, g: 255, b: 255, a: 1 }; for (let i = chain.length - 1; i >= 0; i--) acc = over(chain[i], acc); return acc; };
  const bad = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement; if (!el || seen.has(el)) continue; seen.add(el);
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
    const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
    let hidden = false; for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0 || s.clipPath?.includes('inset(50%')) { hidden = true; break; } }
    if (hidden) continue;
    if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'OPTION'].includes(el.tagName)) continue;
    const fg0 = parse(cs.color); const bg = bgOf(el); if (!fg0 || !bg) continue;
    let eo = 1; for (let e = el; e; e = e.parentElement) eo *= +getComputedStyle(e).opacity;
    const fg = over({ ...fg0, a: fg0.a * eo }, bg);
    const l1 = lum(fg), l2 = lum(bg); const ratio = (Math.max(l1, l2) + .05) / (Math.min(l1, l2) + .05);
    if (ratio < MIN) bad.push({ ratio: +ratio.toFixed(2), text: n.textContent.trim().slice(0, 40), sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.') : ''), fg: cs.color, bg: `rgb(${bg.r | 0},${bg.g | 0},${bg.b | 0})` });
  }
  return bad;
};

const b = await chromium.launch();
const report = {};
for (const vp of [{ n: 'desktop', w: 1366, h: 850 }, { n: 'mobile', w: 390, h: 844 }]) {
  for (const theme of ['light', 'dark']) {
    const ctx = await b.newContext({ viewport: { width: vp.w, height: vp.h }, hasTouch: vp.n === 'mobile', isMobile: vp.n === 'mobile' });
    await ctx.addInitScript((t) => { try { localStorage.setItem('theme', t); } catch (e) {} }, theme);
    if (cookie) await ctx.addCookies([{ name: 'sessionid', value: cookie, url: base }]);
    const page = await ctx.newPage();
    for (const p of paths) {
      const slug = (p.replace(/\W+/g, '_').replace(/^_|_$/g, '') || 'root');
      try {
        await page.goto(base + p, { waitUntil: 'load', timeout: 30000 });
        await page.waitForTimeout(900);
        await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
        await page.waitForTimeout(400);
        if (shots) await page.screenshot({ path: `${out}/${slug}-${vp.n}-${theme}.png`, fullPage: true });
        const bad = await page.evaluate(`(${probe.toString().replace('MIN', min)})()`);
        report[`${p} ${vp.n} ${theme}`] = bad;
      } catch (e) { report[`${p} ${vp.n} ${theme}`] = [{ error: String(e).slice(0, 120) }]; }
    }
    await ctx.close();
  }
}
await b.close();
let total = 0;
for (const [k, v] of Object.entries(report)) {
  total += v.length;
  console.log(`\n## ${k}: ${v.length} low-contrast`);
  const grp = {}; for (const x of v) { const key = x.sel + ' ' + x.fg + ' on ' + x.bg; (grp[key] ||= { ...x, n: 0 }).n++; }
  Object.values(grp).sort((a, b) => a.ratio - b.ratio).slice(0, 12).forEach((x) => console.log(`  ${x.ratio ?? '!'}  x${x.n}  ${x.sel}  "${x.text ?? x.error}"  ${x.fg} on ${x.bg}`));
}
console.log('\nTOTAL', total);
process.exit(0);
