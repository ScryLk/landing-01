#!/usr/bin/env node
import http from 'node:http';
import path from 'node:path';
import { readFile, stat } from 'node:fs/promises';
import { watch } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { build } from './build.mjs';
const app = process.cwd();
await build(app);
const root = path.join(app, 'dist');
const args = process.argv.slice(2);
const portIndex = args.lastIndexOf('--port');
const port = Number(portIndex >= 0 ? args[portIndex + 1] : 8000);
if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error('Porta inválida.');
const types = { '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8', '.js':'text/javascript; charset=utf-8', '.svg':'image/svg+xml', '.webp':'image/webp', '.png':'image/png', '.jpg':'image/jpeg' };
const server = http.createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://local').pathname);
    if (pathname.split('/').some(segment => segment.startsWith('.'))) { response.writeHead(404); response.end(); return; }
    let file = path.resolve(root, `.${pathname}`);
    if (file !== root && !file.startsWith(`${root}${path.sep}`)) { response.writeHead(404); response.end(); return; }
    const info = await stat(file);
    if (info.isDirectory()) {
      if (!pathname.endsWith('/')) { response.writeHead(301, { Location: `${pathname}/` }); response.end(); return; }
      file = path.join(file, 'index.html');
    }
    const body = await readFile(file);
    response.writeHead(200, { 'Content-Type':types[path.extname(file)] || 'application/octet-stream', 'Cache-Control':'no-store' });
    response.end(request.method === 'HEAD' ? undefined : body);
  } catch { response.writeHead(404); response.end('Not found'); }
});
server.on('error', error => { console.error(`Falha ao iniciar: ${error.message}. Escolha outra porta com --port.`); process.exit(1); });
server.listen(port, '0.0.0.0', () => console.log(`Servidor local iniciado na porta ${server.address().port}.`));
if (args.includes('--watch')) {
  let timer;
  let queue = Promise.resolve();
  const rebuild = () => {
    clearTimeout(timer);
    timer = setTimeout(() => { queue = queue.then(() => build(app)).catch(error => console.error(error.message)); }, 100);
  };
  for (const entry of ['index.html','styles.css','app.js','config.js','site.json','assets']) watch(path.join(app, entry), { recursive:true }, rebuild);
  watch(fileURLToPath(new URL('../ui/', import.meta.url)), { recursive:true }, rebuild);
}
