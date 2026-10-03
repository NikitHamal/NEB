import http from 'node:http';
import { createReadStream, statSync } from 'node:fs';
import path from 'node:path';

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.ttf': 'font/ttf',
  '.woff2': 'font/woff2',
};

export function serve(mounts) {
  const entries = Object.entries(mounts).map(([prefix, dir]) => [prefix.replace(/\/$/, ''), path.resolve(dir)]);
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, 'http://localhost');
    const pathname = decodeURIComponent(url.pathname);
    for (const [prefix, root] of entries) {
      if (pathname !== prefix && !pathname.startsWith(`${prefix}/`)) continue;
      const rel = pathname.slice(prefix.length) || '/';
      const file = path.resolve(root, `.${rel.endsWith('/') ? `${rel}index.html` : rel}`);
      if (file !== root && !file.startsWith(root + path.sep)) break;
      try {
        const stat = statSync(file);
        if (!stat.isFile()) break;
        res.writeHead(200, {
          'Content-Type': MIME[path.extname(file).toLowerCase()] ?? 'application/octet-stream',
          'Content-Length': stat.size,
          'Cache-Control': 'no-store',
        });
        createReadStream(file).pipe(res);
        return;
      } catch {
        break;
      }
    }
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end(`not found: ${pathname}`);
  });
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({
        origin: `http://127.0.0.1:${port}`,
        close: () => new Promise((done) => server.close(() => done())),
      });
    });
  });
}
