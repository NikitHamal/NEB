import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { launchChrome } from '../lib/chrome.mjs';
import { loadSpec } from '../lib/spec.mjs';
import { list } from '../lib/args.mjs';
import { P } from '../lib/paths.mjs';

const STYLE = (cfg) => `
  *, *::before, *::after { animation: none !important; transition: none !important; caret-color: transparent !important; scroll-behavior: auto !important; }
  ${(cfg.hide ?? []).map((s) => `${s}`).join(',') || '.nothing-to-hide'} { display: none !important; }
  ${(cfg.redact ?? []).map((s) => `${s}`).join(',') || '.nothing-to-redact'} { filter: blur(7px) !important; }
`;

async function prepare(page, cfg) {
  await page.evaluate(`(() => {
    const style = document.createElement('style');
    style.textContent = ${JSON.stringify(STYLE(cfg))};
    document.head.appendChild(style);
    document.documentElement.setAttribute('data-theme', ${JSON.stringify(cfg.theme ?? 'light')});
  })()`);
  await page.evaluate(`(async () => {
    const step = window.innerHeight * 0.8;
    for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 220));
    }
    window.scrollTo(0, 0);
    await Promise.all([...document.images].map((img) => (img.complete ? null : new Promise((r) => { img.onload = img.onerror = r; setTimeout(r, 6000); }))));
    await document.fonts.ready;
  })()`, { timeout: 120_000 });
  await new Promise((r) => setTimeout(r, cfg.settleMs ?? 1500));
}

async function captureOne(chrome, base, cfg) {
  const vp = cfg.viewport ?? { width: 1440, height: 900, deviceScaleFactor: 1 };
  const page = await chrome.newPage({ viewport: vp });
  let status = 0;
  const docUrl = new URL(cfg.url, base).href;
  page.connection.on(`${page.sessionId}:Network.responseReceived`, (p) => {
    if (p.type === 'Document' && p.response.url === docUrl) status = p.response.status;
  });
  await page.goto(docUrl, { timeout: 120_000 });
  await page.idle({ quiet: 1200, timeout: 40_000 });
  if (status && status !== (cfg.expectStatus ?? 200)) throw new Error(`${docUrl} answered ${status}, expected ${cfg.expectStatus ?? 200}`);
  await prepare(page, cfg);
  const title = await page.evaluate('document.title');
  let clip;
  let beyond = false;
  if (cfg.fullPage) {
    const height = Math.min(await page.evaluate('document.documentElement.scrollHeight'), cfg.maxHeight ?? 4000);
    clip = { x: 0, y: 0, width: vp.width, height, scale: 1 };
    beyond = true;
  } else if (cfg.selector) {
    const box = await page.evaluate(`(() => { const r = document.querySelector(${JSON.stringify(cfg.selector)})?.getBoundingClientRect(); return r ? { x: r.x + scrollX, y: r.y + scrollY, width: r.width, height: r.height } : null; })()`);
    if (!box) throw new Error(`selector ${cfg.selector} matched nothing on ${docUrl}`);
    clip = { ...box, scale: 1 };
    beyond = true;
  }
  const buffer = await page.screenshot({ format: 'jpeg', quality: cfg.quality ?? 88, clip, beyond });
  await page.close();
  const file = `${cfg.id}.jpg`;
  writeFileSync(path.join(P.captures, file), buffer);
  return {
    id: cfg.id,
    file,
    url: docUrl,
    title,
    status: status || 200,
    capturedAt: new Date().toISOString(),
    viewport: vp,
    bytes: buffer.length,
    sha256: createHash('sha256').update(buffer).digest('hex'),
  };
}

export async function run({ flags }) {
  const spec = loadSpec();
  const only = list(flags.only);
  const configs = (spec.captures ?? []).filter((c) => !only.length || only.includes(c.id));
  if (!configs.length) throw new Error('no captures to take (spec.captures is empty or --only matched nothing)');
  const base = flags.base ?? `https://${spec.brand.url}`;
  mkdirSync(P.captures, { recursive: true });
  const manifestFile = path.join(P.captures, 'manifest.json');
  const manifest = existsSync(manifestFile) ? JSON.parse(readFileSync(manifestFile, 'utf8')) : { items: [] };
  const chrome = await launchChrome();
  try {
    for (const cfg of configs) {
      process.stdout.write(`capturing ${cfg.id} <- ${new URL(cfg.url, base).href} ... `);
      const item = await captureOne(chrome, base, cfg);
      manifest.items = [...manifest.items.filter((i) => i.id !== item.id), item];
      console.log(`${(item.bytes / 1024).toFixed(0)} KB`);
    }
  } finally {
    await chrome.close();
  }
  manifest.items.sort((a, b) => a.id.localeCompare(b.id));
  writeFileSync(manifestFile, `${JSON.stringify(manifest, null, 2)}\n`);
  console.log(`manifest -> ${path.relative(process.cwd(), manifestFile)}`);
}
