#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const shared = fileURLToPath(new URL('../ui/commerce.js', import.meta.url));
export async function check(app = process.cwd()) {
  const site = JSON.parse(await readFile(path.join(app, 'site.json'), 'utf8'));
  JSON.parse(await readFile(path.join(app, 'package.json'), 'utf8'));
  const files = [path.join(app, 'app.js'), path.join(app, 'config.js')];
  if (site.sharedUi) files.push(shared);
  for (const file of files) {
    const result = spawnSync(process.execPath, ['--check', file], { stdio: 'inherit' });
    if (result.status !== 0) throw new Error(`JavaScript inválido: ${file}`);
  }
  const html = await readFile(path.join(app, 'index.html'), 'utf8');
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  if (new Set(ids).size !== ids.length) throw new Error('IDs HTML duplicados.');
  if (!/<html lang="pt-BR"/.test(html) || !/<main\b/.test(html) || !/<h1\b/.test(html)) throw new Error('Estrutura semântica incompleta.');
  console.log(`Verificação: ${path.basename(app)} OK`);
}
if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) await check();
