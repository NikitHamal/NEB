import { spawn } from 'node:child_process';
import { existsSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { Connection, Page } from './cdp.mjs';

const NAMES = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome'];
const ABSOLUTE = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
];

const FLAGS = [
  '--headless=new',
  '--hide-scrollbars',
  '--mute-audio',
  '--no-first-run',
  '--no-default-browser-check',
  '--disable-extensions',
  '--disable-component-update',
  '--disable-background-networking',
  '--disable-sync',
  '--disable-translate',
  '--disable-default-apps',
  '--disable-popup-blocking',
  '--disable-infobars',
  '--metrics-recording-only',
  '--force-color-profile=srgb',
  '--font-render-hinting=none',
  '--disable-lcd-text',
  '--disable-renderer-backgrounding',
  '--disable-background-timer-throttling',
  '--disable-backgrounding-occluded-windows',
  '--disable-ipc-flooding-protection',
  '--force-device-scale-factor=1',
  '--autoplay-policy=no-user-gesture-required',
];

function onPath(name) {
  const exts = process.platform === 'win32' ? (process.env.PATHEXT ?? '.EXE').split(';') : [''];
  for (const dir of (process.env.PATH ?? '').split(path.delimiter)) {
    for (const ext of exts) {
      const candidate = path.join(dir, name + ext);
      if (dir && existsSync(candidate)) return candidate;
    }
  }
  return null;
}

export function resolveChrome() {
  const fromEnv = process.env.CHROME_PATH;
  if (fromEnv) {
    if (!existsSync(fromEnv)) throw new Error(`CHROME_PATH points to a missing file: ${fromEnv}`);
    return fromEnv;
  }
  for (const name of NAMES) {
    const found = onPath(name);
    if (found) return found;
  }
  for (const candidate of ABSOLUTE) if (existsSync(candidate)) return candidate;
  throw new Error('Chrome not found. Install Google Chrome or Chromium, or set CHROME_PATH to the executable.');
}

export async function launchChrome({ width = 1920, height = 1080, args = [] } = {}) {
  const executable = resolveChrome();
  const profile = mkdtempSync(path.join(tmpdir(), 'nebians-video-'));
  const flags = [
    ...FLAGS,
    ...(process.env.CHROME_SANDBOX === '1' ? [] : ['--no-sandbox']),
    `--user-data-dir=${profile}`,
    `--window-size=${width},${height}`,
    '--remote-debugging-port=0',
    ...args,
    'about:blank',
  ];
  const child = spawn(executable, flags, { stdio: ['ignore', 'ignore', 'pipe'] });
  let tail = '';
  const endpoint = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`Chrome exposed no DevTools endpoint in 30s\n${tail.slice(-1500)}`)), 30_000);
    child.stderr.on('data', (chunk) => {
      tail = (tail + chunk.toString()).slice(-4000);
      const match = tail.match(/DevTools listening on (ws:\/\/\S+)/);
      if (match) {
        clearTimeout(timer);
        resolve(match[1]);
      }
    });
    child.once('error', (error) => {
      clearTimeout(timer);
      reject(error);
    });
    child.once('exit', (code) => {
      clearTimeout(timer);
      reject(new Error(`Chrome exited early with code ${code}\n${tail.slice(-1500)}`));
    });
  });

  const connection = await new Connection(endpoint).open();
  let closed = false;

  const close = async () => {
    if (closed) return;
    closed = true;
    connection.close();
    child.kill('SIGKILL');
    await new Promise((resolve) => setTimeout(resolve, 150));
    try {
      rmSync(profile, { recursive: true, force: true });
    } catch {
      return;
    }
  };
  process.once('exit', () => {
    if (!closed) child.kill('SIGKILL');
  });

  const newPage = async ({ viewport = { width, height }, userAgent = undefined } = {}) => {
    const { targetId } = await connection.send('Target.createTarget', { url: 'about:blank' });
    const { sessionId } = await connection.send('Target.attachToTarget', { targetId, flatten: true });
    const page = new Page(connection, sessionId, targetId);
    await page.send('Page.enable');
    await page.send('Runtime.enable');
    await page.send('Log.enable');
    await page.send('Network.enable');
    await page.setViewport(viewport);
    if (userAgent) await page.send('Emulation.setUserAgentOverride', { userAgent });
    return page;
  };

  return { executable, connection, newPage, close };
}
