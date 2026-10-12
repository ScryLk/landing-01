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
    // New social metadata is opt-in, so existing applications keep their output.
    const socialImage = site.socialImage ?? '';
    if (typeof socialImage !== 'string' || (socialImage && (!socialImage.startsWith('assets/') ||
      /[\\?#\0]/.test(socialImage) || socialImage.split('/').some(part => !part || part === '.' || part === '..')))) {
      throw new Error('socialImage precisa indicar um arquivo local dentro de assets/.');
    }
    for (const dimension of ['socialImageWidth', 'socialImageHeight']) {
      if (site[dimension] !== undefined && (!socialImage || !Number.isSafeInteger(site[dimension]) || site[dimension] <= 0)) {
        throw new Error(`${dimension} precisa ser um inteiro positivo com socialImage definido.`);
      }
    }
    if (socialImage && !(await stat(path.join(staging, socialImage))).isFile()) {
      throw new Error('socialImage precisa indicar um arquivo.');
    }
    const image = socialImage || site.image;
    const meta = [
      `<meta property="og:type" content="website">`,
      `<meta property="og:locale" content="pt_BR">`,
      `<meta property="og:title" content="${escape(site.title)}">`,
      `<meta property="og:description" content="${escape(site.description)}">`,
      `<meta name="twitter:card" content="${image && base ? 'summary_large_image' : 'summary'}">`
    ];
    if (socialImage) {
      meta.push(`<meta name="twitter:title" content="${escape(site.title)}">`);
      meta.push(`<meta name="twitter:description" content="${escape(site.description)}">`);
    }
    if (base) {
      meta.push(`<link rel="canonical" href="${escape(base.href)}">`, `<meta property="og:url" content="${escape(base.href)}">`);
      if (image) {
        await stat(path.join(staging, image));
        const imageUrl = escape(new URL(image, base).href);
        const imageAlt = escape(socialImage ? site.socialImageAlt || site.title : site.title);
        meta.push(`<meta property="og:image" content="${imageUrl}">`);
        meta.push(`<meta property="og:image:alt" content="${imageAlt}">`);
        if (socialImage) {
          for (const [key, property] of [['socialImageWidth', 'width'], ['socialImageHeight', 'height']]) {
            if (site[key] !== undefined) meta.push(`<meta property="og:image:${property}" content="${site[key]}">`);
          }
          meta.push(`<meta name="twitter:image" content="${imageUrl}">`);
          meta.push(`<meta name="twitter:image:alt" content="${imageAlt}">`);
        }
      }
    }
    if (site.seoFiles === true && base) {
      await writeFile(path.join(staging, 'robots.txt'), `User-agent: *\nAllow: /\n\nSitemap: ${new URL('sitemap.xml', base).href}\n`);
      await writeFile(path.join(staging, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>${escape(base.href)}</loc></url>\n</urlset>\n`);
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
