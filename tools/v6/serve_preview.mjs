import { createReadStream } from 'node:fs';
import { stat } from 'node:fs/promises';
import { createServer } from 'node:http';
import { dirname, extname, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const port = Number(process.env.CWI_PREVIEW_PORT ?? 22222);
if (!Number.isInteger(port) || port < 1 || port > 65535) throw new RangeError('CWI_PREVIEW_PORT 1–65535 arasında olmalı.');
const types = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8',
  '.webp': 'image/webp',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.mp4': 'video/mp4',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
};

const server = createServer(async (request, response) => {
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    response.writeHead(405, { Allow: 'GET, HEAD' }).end();
    return;
  }

  let pathname;
  try {
    pathname = decodeURIComponent(new URL(request.url, 'http://127.0.0.1').pathname);
  } catch {
    response.writeHead(400).end();
    return;
  }
  const file = resolve(root, `.${pathname.endsWith('/') ? `${pathname}index.html` : pathname}`);
  const nested = relative(root, file);
  if (nested.startsWith('..' + sep) || nested === '..' || nested.split(sep).some(part => part.startsWith('.')) || !types[extname(file)]) {
    response.writeHead(404).end();
    return;
  }

  try {
    const details = await stat(file);
    if (!details.isFile()) throw new Error('Dosya bulunamadı.');
    response.writeHead(200, { 'Content-Type': types[extname(file)], 'Content-Length': details.size, 'Cache-Control': 'no-store' });
    if (request.method === 'HEAD') response.end();
    else createReadStream(file).pipe(response);
  } catch {
    response.writeHead(404).end();
  }
});

server.on('error', error => {
  if (error.code === 'EADDRINUSE') console.error(`127.0.0.1:${port} zaten kullanılıyor. Çalışan servisi değiştirmedim.`);
  else console.error(error.message);
  process.exitCode = 1;
});
server.listen(port, '127.0.0.1', () => {
  console.log(`Önizleme: http://127.0.0.1:${port}/examples/v7/reference-compare/`);
});
