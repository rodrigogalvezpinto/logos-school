// Servidor estático mínimo con fallback SPA para la build (E2E). Uso: node servir_spa.mjs <carpeta> <puerto>
import http from 'node:http'; import { readFile, stat } from 'node:fs/promises'; import path from 'node:path';
const raiz = path.resolve(process.argv[2]); const puerto = Number(process.argv[3]);
const tipos = { '.html':'text/html; charset=utf-8', '.js':'text/javascript', '.css':'text/css', '.json':'application/json', '.svg':'image/svg+xml', '.png':'image/png', '.ico':'image/x-icon', '.woff2':'font/woff2', '.txt':'text/plain', '.m4a':'audio/mp4' };
http.createServer(async (req, res) => {
  let p = path.join(raiz, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(raiz)) { res.writeHead(403); return res.end(); }
  try { if (!(await stat(p)).isFile()) throw 0; } catch { p = path.join(raiz, 'index.html'); }
  res.writeHead(200, { 'Content-Type': tipos[path.extname(p)] || 'application/octet-stream' });
  res.end(await readFile(p));
}).listen(puerto, '127.0.0.1');
