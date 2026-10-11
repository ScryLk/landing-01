// Optional integration runner; Playwright belongs to development tooling, never to the sites.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { mkdir } from 'node:fs/promises';
const require=createRequire(import.meta.url);
let chromium;
try { ({chromium}=require(process.env.PLAYWRIGHT_MODULE_PATH || 'playwright')); }
catch { throw new Error('Instale Playwright no ambiente de testes ou defina PLAYWRIGHT_MODULE_PATH para o módulo instalado. Não é uma dependência de produção.'); }
const root=fileURLToPath(new URL('../',import.meta.url));
const servers=[];
let browser;
async function start(name) {
  const child=spawn(process.execPath,[path.join(root,'packages/config/serve.mjs'),'--port','0'],{cwd:path.join(root,'apps',name),stdio:['ignore','pipe','pipe']});
  servers.push(child);
  return new Promise((resolve,reject)=>{
    const timer=setTimeout(()=>reject(new Error(`Timeout: ${name}`)),15000);
    child.stdout.on('data',data=>{
      const match=data.toString().match(/porta (\d+)/);
      if(match){clearTimeout(timer);resolve(`http://127.0.0.1:${match[1]}`)}
    });
    child.stderr.on('data',data=>process.stderr.write(data));
    child.on('error',reject);
    child.on('exit',code=>{clearTimeout(timer);if(code)reject(new Error(`${name}: exit ${code}`))});
  });
}
try {
  const blue=await start('experiencia-tecnologia');
  const orange=await start('industria-40');
  browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{}),args:['--no-sandbox']});
  const errors=[];
  for(const [name,url] of [['experiencia',blue],['industria',orange]]) {
    const page=await browser.newPage();page.on('pageerror',e=>errors.push(e.message));
    for(const width of [320,390,768,1440]) {
      await page.setViewportSize({width,height:900});await page.goto(url);
      await page.locator('img[src]').evaluateAll(async imgs=>Promise.all(imgs.map(img=>{img.loading='eager';return img.decode()})));
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`${name}: overflow ${width}`);
      assert.equal(await page.locator('h1').count(),1);
      assert.ok(await page.locator('[data-buy][aria-disabled="true"]').count()>0);
      if(name === 'industria') {
        assert.equal(await page.locator('#chapter-groups li').count(),12,'Sumário real deve estar disponível');
        assert.ok((await page.locator('#chapter-groups li').first().textContent()).includes('Como chegamos à Indústria 4.0?'));
        assert.ok((await page.locator('#chapter-groups li').last().textContent()).includes('Por onde começar? A Indústria 4.0 é para todos?'));
      }
      await page.locator('summary').first().click();assert.notEqual(await page.locator('details').first().getAttribute('open'),null);
      await page.keyboard.press('Tab');
      if(process.env.SCREENSHOT_DIR){await mkdir(process.env.SCREENSHOT_DIR,{recursive:true});await page.screenshot({path:path.join(process.env.SCREENSHOT_DIR,`${name}-${width}.png`),fullPage:true})}
      console.log(`PASS ${name} ${width}px: layout, imagens, FAQ e checkout pendente`);
    }
    assert.equal((await page.request.get(`${url}/.git/config`)).status(),404);
    assert.equal((await page.request.get(`${url}/config.js`)).status(),200);
    await page.close();
  }
  const page=await browser.newPage();
  const product={title:'Afinal, o que é Indústria 4.0?',subtitle:'Teste de configuração independente',checkoutUrl:'https://pay.kiwify.com.br/teste',price:'Preço de teste',author:'Autoria de teste',contactEmail:'contato@example.test',cover:'assets/icon.svg',previewImages:[{src:'assets/icon.svg',alt:'Prévia de teste',width:64,height:64}],chapterGroups:[{title:'Grupo de teste',chapters:Array.from({length:12},(_,i)=>({number:i+1,title:`Título de teste ${i+1}`}))}],institutionalLinks:[]};
  await page.route('**/config.js',route=>route.fulfill({contentType:'application/javascript',body:`window.INDUSTRIA_CONFIG=${JSON.stringify(product)}`}));
  await page.goto(orange);await page.locator('.official-cover').waitFor({state:'visible'});
  await page.locator('[data-cover]').last().waitFor({state:'visible'});
  assert.equal(await page.locator('[data-cover]:visible').count(),3,'Capa deve aparecer também no produto e na oferta');
  assert.equal(await page.locator('[data-buy][href="https://pay.kiwify.com.br/teste"]').count(),2);
  assert.equal(await page.locator('#price').textContent(),'Preço de teste');
  assert.equal(await page.locator('#chapter-groups li').count(),12);
  assert.equal(await page.locator('#previews figure').count(),1);
  assert.equal(await page.locator('.hero-visual [data-cover-placeholder]').isVisible(),false);
  assert.equal(await page.locator('#author').isVisible(),true);
  const bluePage=await browser.newPage();await bluePage.goto(blue);
  assert.equal(await bluePage.locator('[data-buy][aria-disabled="true"]').count(),3,'Uma configuração não modifica outra aplicação');
  assert.notEqual(await bluePage.locator('#price').textContent(),'Preço de teste');
  product.checkoutUrl='https://kiwify.com.br.evil.test/produto';product.chapterGroups[0].chapters[11].number=1;
  await page.reload();assert.equal(await page.locator('[data-buy][aria-disabled="true"]').count(),2);
  assert.equal(await page.locator('#chapters').isVisible(),false,'Sumário incompleto ou duplicado não deve aparecer');
  await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');
  const noJs=await browser.newPage({javaScriptEnabled:false});await noJs.goto(orange);assert.equal(await noJs.locator('[data-buy][href]').count(),0);
  assert.deepEqual(errors,[],'Erros JavaScript no navegador');
  console.log('PASS configuração de checkout, capa, sumário, prévias, isolamento e movimento reduzido. Dados de teste não são salvos.');
} finally {
  if(browser)await browser.close();
  for(const child of servers)child.kill('SIGTERM');
}
