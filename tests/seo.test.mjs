import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { build } from '../packages/config/build.mjs';

const enhancedSite = {
  title: 'Afinal, o que é Inteligência Artificial?',
  description: 'Conheça a IA, seus usos e seus limites.',
  image: 'assets/cover.png',
  socialImage: 'assets/og-ia.png',
  socialImageWidth: 1200,
  socialImageHeight: 630,
  socialImageAlt: 'Capa do e-book & Inteligência Artificial',
  seoFiles: true
};

async function fixture(t, site = enhancedSite) {
  const app = await mkdtemp(path.join(tmpdir(), 'dobraverse-seo-'));
  t.after(() => rm(app, { recursive: true, force: true }));
  await mkdir(path.join(app, 'assets'));
  await Promise.all([
    writeFile(path.join(app, 'site.json'), JSON.stringify(site)),
    writeFile(path.join(app, 'index.html'), '<!doctype html><html lang="pt-BR"><head><title>IA</title></head><body>IA</body></html>'),
    writeFile(path.join(app, 'styles.css'), 'body { color: #111; }'),
    writeFile(path.join(app, 'app.js'), '// Interface'),
    writeFile(path.join(app, 'config.js'), 'export const CHECKOUT_URL = "INSERIR_LINK_KIWIFY_OU_HOTMART";'),
    writeFile(path.join(app, 'assets/cover.png'), 'fixture-cover'),
    writeFile(path.join(app, 'assets/og-ia.png'), 'fixture-social-image'),
    writeFile(path.join(app, '.env'), 'PRIVATE_TEST=not-public'),
    writeFile(path.join(app, 'internal-notes.md'), 'not public')
  ]);
  return app;
}

test('SEO opt-in usa a URL HTTPS em subpasta e a imagem social declarada', async t => {
  const app = await fixture(t);
  const originalSource = await readFile(path.join(app, 'index.html'));
  const originalConfig = await readFile(path.join(app, 'config.js'));
  await build(app, path.join(app, 'dist'), { siteUrl: 'https://example.test/ebooks/inteligencia-artificial' });
  const html = await readFile(path.join(app, 'dist/index.html'), 'utf8');
  const base = 'https://example.test/ebooks/inteligencia-artificial/';
  for (const expected of [
    `<link rel="canonical" href="${base}">`,
    `<meta property="og:url" content="${base}">`,
    `<meta property="og:image" content="${base}assets/og-ia.png">`,
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    '<meta property="og:image:alt" content="Capa do e-book &amp; Inteligência Artificial">',
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta name="twitter:title" content="Afinal, o que é Inteligência Artificial?">',
    '<meta name="twitter:description" content="Conheça a IA, seus usos e seus limites.">',
    `<meta name="twitter:image" content="${base}assets/og-ia.png">`,
    '<meta name="twitter:image:alt" content="Capa do e-book &amp; Inteligência Artificial">'
  ]) assert.ok(html.includes(expected), expected);
  assert.ok(!html.includes(`${base}assets/cover.png`), 'Imagem social substitui a capa nos metadados.');
  assert.equal(await readFile(path.join(app, 'dist/robots.txt'), 'utf8'), `User-agent: *\nAllow: /\n\nSitemap: ${base}sitemap.xml\n`);
  const sitemap = await readFile(path.join(app, 'dist/sitemap.xml'), 'utf8');
  assert.ok(sitemap.includes(`<loc>${base}</loc>`));
  assert.equal((sitemap.match(/<loc>/g) || []).length, 1);
  assert.deepEqual(await readFile(path.join(app, 'index.html')), originalSource);
  assert.deepEqual(await readFile(path.join(app, 'config.js')), originalConfig);
  assert.deepEqual(await readFile(path.join(app, 'dist/config.js')), originalConfig);
  const files = await readdir(path.join(app, 'dist'));
  assert.ok(!files.includes('.env'));
  assert.ok(!files.includes('site.json'));
  assert.ok(!files.includes('internal-notes.md'));
});

test('SITE_URL ausente omite URLs públicas e arquivos SEO, sem inventar domínio', async t => {
  const app = await fixture(t);
  await build(app, path.join(app, 'dist'), { siteUrl: '' });
  const html = await readFile(path.join(app, 'dist/index.html'), 'utf8');
  assert.ok(html.includes('<meta name="twitter:card" content="summary">'));
  assert.ok(html.includes('name="twitter:title"'));
  for (const tag of ['rel="canonical"', 'property="og:url"', 'property="og:image"', 'name="twitter:image"']) {
    assert.ok(!html.includes(tag), `${tag} precisa de SITE_URL.`);
  }
  const files = await readdir(path.join(app, 'dist'));
  assert.ok(!files.includes('robots.txt'));
  assert.ok(!files.includes('sitemap.xml'));
});

test('SEO novo permanece isolado das aplicações que não declaram opt-in', async t => {
  const app = await fixture(t, { title: 'E-book existente', description: 'Descrição existente.', image: 'assets/cover.png' });
  await build(app, path.join(app, 'dist'), { siteUrl: 'https://example.test/existente/' });
  const html = await readFile(path.join(app, 'dist/index.html'), 'utf8');
  assert.ok(html.includes('content="https://example.test/existente/assets/cover.png"'));
  assert.ok(html.includes('<meta name="twitter:card" content="summary_large_image">'));
  for (const tag of ['twitter:title', 'twitter:description', 'twitter:image', 'og:image:width', 'og:image:height']) {
    assert.ok(!html.includes(tag), `${tag} é opt-in.`);
  }
  const files = await readdir(path.join(app, 'dist'));
  assert.ok(!files.includes('robots.txt'));
  assert.ok(!files.includes('sitemap.xml'));
});

test('arquivos SEO e dimensões podem ser omitidos independentemente da imagem social', async t => {
  const app = await fixture(t, { title: 'IA', description: 'IA.', socialImage: 'assets/og-ia.png' });
  await build(app, path.join(app, 'dist'), { siteUrl: 'https://example.test/ia/' });
  const html = await readFile(path.join(app, 'dist/index.html'), 'utf8');
  assert.ok(html.includes('name="twitter:image"'));
  assert.ok(html.includes('property="og:image:alt" content="IA"'));
  assert.ok(!html.includes('property="og:image:width"'));
  assert.ok(!html.includes('property="og:image:height"'));
  assert.ok(!(await readdir(path.join(app, 'dist'))).includes('sitemap.xml'));
});

test('SEO rejeita HTTP, imagens externas ou fora de assets e dimensões inválidas', async t => {
  const app = await fixture(t);
  const output = path.join(app, 'dist');
  await assert.rejects(build(app, output, { siteUrl: 'http://example.test/ia/' }), /HTTPS/);
  for (const socialImage of ['https://example.test/og.png', '../private.png', 'assets/../config.js', 'assets/og-ia.png?x=1', true]) {
    await writeFile(path.join(app, 'site.json'), JSON.stringify({ ...enhancedSite, socialImage }));
    await assert.rejects(build(app, output, { siteUrl: '' }), /socialImage/);
  }
  for (const socialImageWidth of [0, -1, 1200.5, '1200']) {
    await writeFile(path.join(app, 'site.json'), JSON.stringify({ ...enhancedSite, socialImageWidth }));
    await assert.rejects(build(app, output, { siteUrl: '' }), /socialImageWidth/);
  }
  await writeFile(path.join(app, 'site.json'), JSON.stringify({ ...enhancedSite, socialImage: 'assets/missing.png' }));
  await assert.rejects(build(app, output, { siteUrl: '' }), /ENOENT/);
});
