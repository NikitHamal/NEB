import { serve } from './server.mjs';
import { launchChrome } from './chrome.mjs';
import { mounts } from './paths.mjs';
import { loadSpec, assertSpec, aspectSize } from './spec.mjs';

export async function openStage({ aspect = '16:9', scale = 1, workers = 1 } = {}) {
  const spec = assertSpec(loadSpec());
  const { width, height } = aspectSize(spec, aspect);
  const server = await serve(mounts());
  let chrome;
  try {
    chrome = await launchChrome({ width, height });
    const pages = [];
    for (let i = 0; i < workers; i += 1) {
      const page = await chrome.newPage({ viewport: { width, height, deviceScaleFactor: scale } });
      await page.goto(`${server.origin}/stage/index.html?aspect=${encodeURIComponent(aspect)}`);
      try {
        await page.evaluate('window.__ready', { timeout: 180_000 });
      } catch (error) {
        throw new Error(`stage failed to boot: ${error.message}\n${page.errors.join('\n')}`);
      }
      pages.push(page);
    }
    return {
      spec,
      width,
      height,
      scale,
      pages,
      page: pages[0],
      server,
      chrome,
      async close() {
        await chrome.close();
        await server.close();
      },
    };
  } catch (error) {
    if (chrome) await chrome.close();
    await server.close();
    throw error;
  }
}

export async function seekAndShot(page, t, { format = 'png', quality = 92, fast = true } = {}) {
  const before = page.errors.length;
  await page.evaluate(`window.__seek(${t})`);
  if (page.errors.length > before) throw new Error(`stage error at t=${t}s: ${page.errors.slice(before).join(' | ')}`);
  return page.screenshot({ format, quality, fast });
}
