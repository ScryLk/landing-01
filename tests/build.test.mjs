import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, cp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { build } from '../packages/config/build.mjs';
import { httpsUrl } from '../packages/ui/commerce.js';
const root = fileURLToPath(new URL('../', import.meta.url));
const files = ['index.html', 'styles.css', 'app.js', 'config.js', 'assets/capa.webp', 'assets/previa-mercado.webp', 'assets/previa-portfolio.webp', 'assets/previa-plano.webp', 'assets/icon.svg'];

test('Migração preserva os arquivos da primeira página e a entrada legada', async () => {
  for (const file of files) assert.deepEqual(
    await readFile(path.join(root, file)),
    await readFile(path.join(root, 'apps/experiencia-tecnologia', file)),
    `Arquivo alterado na migração: ${file}`
  );
});

for (const name of ['experiencia-tecnologia', 'industria-40', 'inteligencia-artificial']) {
  test(`Build ${name} funciona sem a outra aplicação e publica só arquivos públicos`, async t => {
    const temporary = await mkdtemp(path.join(tmpdir(), 'dobraverse-test-'));
    t.after(() => rm(temporary, {recursive:true,force:true}));
    const app = path.join(temporary, name);
    await cp(path.join(root, 'apps', name), app, {recursive:true,filter: source => !['node_modules','dist'].includes(path.basename(source))});
    await writeFile(path.join(app, '.env'), 'PRIVATE_TEST=not-public');
    const originalConfig = await readFile(path.join(app, 'config.js'));
    const siteUrl = `https://example.test/${name}/`;
    await build(app, path.join(app, 'dist'), {siteUrl});
    const entries = await readdir(path.join(app,'dist'));
    assert.deepEqual(entries.sort(), (name!=='experiencia-tecnologia'
      ? (name==='inteligencia-artificial' ? ['app.js','assets','config.js','index.html','robots.txt','shared','sitemap.xml','styles.css'] : ['app.js','assets','config.js','index.html','shared','styles.css'])
      : ['app.js','assets','config.js','index.html','styles.css']).sort());
    assert.deepEqual(await readFile(path.join(app,'dist/config.js')), originalConfig);
    const html = await readFile(path.join(app,'dist/index.html'),'utf8');
    assert.ok(html.includes(`<link rel="canonical" href="${siteUrl}">`));
    assert.ok(html.includes('property="og:title"'));
    if(name==='experiencia-tecnologia') {
      assert.ok(html.includes(`content="${siteUrl}assets/capa.webp"`));
      assert.deepEqual(await readFile(path.join(app,'dist/styles.css')), await readFile(path.join(app,'styles.css')));
    } else {
      if(name==='industria-40') assert.ok(!html.includes('property="og:image"'), 'Não inventar imagem de capa');
      else assert.ok(html.includes(`${siteUrl}assets/og-ia.png`));
      const css=await readFile(path.join(app,'dist/styles.css'),'utf8');
      assert.ok(css.includes('Primitives share layout'));
      assert.ok(!css.includes('#08bdf1'));
    }
    // Rebuild removes stale generated files, without changing the source configuration.
    await writeFile(path.join(app,'dist/stale.txt'),'old');
    await build(app, path.join(app,'dist'), {siteUrl});
    assert.ok(!(await readdir(path.join(app,'dist'))).includes('stale.txt'));
    assert.deepEqual(await readFile(path.join(app,'config.js')),originalConfig);
  });
}

test('URLs de checkout exigem HTTPS e host permitido, sem credenciais embutidas', () => {
  const hosts=['kiwify.com.br','kiwify.app'];
  assert.equal(httpsUrl('https://pay.kiwify.com.br/produto',hosts),'https://pay.kiwify.com.br/produto');
  for(const url of ['INSERIR_CHECKOUT_KIWIFY','javascript:alert(1)','http://pay.kiwify.com.br/produto','https://kiwify.com.br.evil.test','https://evilkiwify.com.br','https://user:pass@pay.kiwify.com.br/produto','https://example.com']) assert.equal(httpsUrl(url,hosts),null);
});

test('Build rejeita saída no código e URL pública sem HTTPS', async t => {
  const app=path.join(root,'apps/industria-40');
  await assert.rejects(build(app,app), /saída/);
  const temp=await mkdtemp(path.join(tmpdir(),'dobraverse-url-'));
  t.after(()=>rm(temp,{recursive:true,force:true}));
  await assert.rejects(build(app,path.join(temp,'dist'),{siteUrl:'http://example.test/'}),/HTTPS/);
});
