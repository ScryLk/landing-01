#!/usr/bin/env node
import { cp, readFile, mkdir, writeFile, rename, rm, stat } from 'node:fs/promises';
import path from 'node:path';
import { realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const ui = fileURLToPath(new URL('../ui/', import.meta.url));
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export async function build(app = process.cwd(), output = path.join(app, 'dist'), options = {}) {
  const site = JSON.parse(await readFile(path.join(app, 'site.json'), 'utf8'));
  const destination = path.resolve(output);
  if (destination === path.resolve(app) || !path.basename(destination).startsWith('dist')) {
    throw new Error('A saída deve ser um diretório dist dedicado; não use a pasta do código.');
  }
  const staging = path.join(path.dirname(destination), `.dist-${process.pid}-${Date.now()}`);
  await mkdir(staging, { recursive: true });
  try {
    for (const name of ['index.html', 'styles.css', 'app.js', 'config.js', 'assets']) {
      await cp(path.join(app, name), path.join(staging, name), { recursive: true });
    }
    if (site.sharedUi) {
      const css = await readFile(path.join(ui, 'primitives.css'), 'utf8');
      const own = await readFile(path.join(staging, 'styles.css'), 'utf8');
      await writeFile(path.join(staging, 'styles.css'), `${css}\n${own}`);
      await mkdir(path.join(staging, 'shared'));
      await cp(path.join(ui, 'commerce.js'), path.join(staging, 'shared/commerce.js'));
    }
    const publicUrl = options.siteUrl ?? process.env.SITE_URL ?? '';
    let base;
    if (publicUrl) {
      base = new URL(publicUrl.endsWith('/') ? publicUrl : `${publicUrl}/`);
      if (base.protocol !== 'https:') throw new Error('SITE_URL precisa usar HTTPS.');
    }
    const meta = [
      `<meta property="og:type" content="website">`,
      `<meta property="og:locale" content="pt_BR">`,
      `<meta property="og:title" content="${escape(site.title)}">`,
      `<meta property="og:description" content="${escape(site.description)}">`,
      `<meta name="twitter:card" content="${site.image && base ? 'summary_large_image' : 'summary'}">`
    ];
    if (base) {
      meta.push(`<link rel="canonical" href="${escape(base.href)}">`, `<meta property="og:url" content="${escape(base.href)}">`);
      if (site.image) {
        await stat(path.join(staging, site.image));
        meta.push(`<meta property="og:image" content="${escape(new URL(site.image, base).href)}">`);
        meta.push(`<meta property="og:image:alt" content="${escape(site.title)}">`);
      }
    }
    let html = await readFile(path.join(staging, 'index.html'), 'utf8');
    html = html.replace('</head>', `${meta.join('\n')}\n</head>`);
    await writeFile(path.join(staging, 'index.html'), html);
    // Only generated output is replaced. Source and product configuration are never modified.
    await rm(destination, { recursive: true, force: true });
    await rename(staging, destination);
    console.log(`Build estático: ${path.basename(app)} → ${destination}`);
  } catch (error) {
    await rm(staging, { recursive: true, force: true });
    throw error;
  }
}
if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await build();
}
