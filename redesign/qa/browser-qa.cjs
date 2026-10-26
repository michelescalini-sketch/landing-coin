/* Isolated localhost browser QA. Never deploys and never contacts a live wallet/API. */
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '../..');
const docs = path.join(root, 'docs');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'redesign/source-manifest.json')));
const output = path.join(root, 'redesign/qa-output');
fs.mkdirSync(output, { recursive: true });
const types = {'.html':'text/html', '.css':'text/css', '.js':'application/javascript', '.svg':'image/svg+xml', '.webp':'image/webp', '.jpg':'image/jpeg', '.ttf':'font/ttf', '.woff2':'font/woff2', '.png':'image/png', '.ico':'image/x-icon'};
const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  let file = path.resolve(docs, '.' + decodeURIComponent(url.pathname));
  if (!file.startsWith(docs + path.sep) && file !== docs) { res.writeHead(403); return res.end(); }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  const found = fs.existsSync(file) && fs.statSync(file).isFile();
  if (!found) file = path.join(docs, '404.html');
  res.writeHead(found ? 200 : 404, {'Content-Type':types[path.extname(file)] || 'application/octet-stream'});
  res.end(fs.readFileSync(file));
});
const results = [];
(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const origin = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch();
  try {
    for (const width of [1440, 1024, 768, 430, 390, 360]) {
      let fixtureId = 42;
      let claimMode='waiting';
      const context = await browser.newContext({viewport:{width, height:900}, reducedMotion:'reduce'});
      // Deterministic read-only fixtures. All other external requests are refused.
      await context.route('**/*', async route => {
        const request = route.request(); const url = new URL(request.url());
        if (url.origin === origin) return route.continue();
        if (url.hostname==='landing-lander-registry.michelescalini.workers.dev' && url.pathname==='/api/claim') {
          assert.equal(request.method(),'POST');
          assert.equal(request.postDataJSON().signature,'B'.repeat(88));
          return route.fulfill({json:claimMode==='waiting'?{status:'waiting'}:{status:'confirmed',lander:{id:fixtureId,wallet:'CBPwvUZrDQThyM6a54shKPpywvpTyYQQ2Ng7FWPZPM88',balanceRaw:'123456789',signature:'A'.repeat(88),confirmedSlot:345678901,createdAt:'2026-10-19 12:00:00'}}});
        }
        assert.equal(request.method(), 'GET', 'No external writes allowed in QA');
        if (url.pathname === '/api/wall/marks') return route.fulfill({json:{status:'ok',marks:[],hasMore:false,nextBefore:null}});
        if (url.pathname === '/api/transparency') return route.fulfill({json:{updatedAt:'2026-10-19T12:00:00Z',holders:{totalPositiveOwners:9,independentHolders:4,projectWallets:4,liquidityPools:1,founderControlled:0,exchangeWallets:0,complete:false},liquidity:{},market:null}});
        if (url.pathname.endsWith('/index.iife.min.js')) return route.fulfill({contentType:'application/javascript',body:fs.readFileSync(process.env.WEB3_IIFE)});
        if (url.pathname.includes('html2canvas') && process.env.HTML2CANVAS_FILE) return route.fulfill({contentType:'application/javascript',body:fs.readFileSync(process.env.HTML2CANVAS_FILE)});
        if (url.hostname === 'esm.sh') return route.fulfill({contentType:'application/javascript',body:'export function getWallets(){return {get:()=>[],on:()=>()=>{}}}'});
        if (url.hostname === 'plugin.jup.ag') return route.fulfill({contentType:'application/javascript',body:'window.Jupiter={init(options){window.__jupiterOptions=options},resume(){},close(){}};'});
        if (url.pathname === '/api/lander') return route.fulfill({json:{status:'confirmed',lander:{id:fixtureId,wallet:'CBPwvUZrDQThyM6a54shKPpywvpTyYQQ2Ng7FWPZPM88',balanceRaw:'123456789',signature:'A'.repeat(88),confirmedSlot:345678901,createdAt:'2026-10-19 12:00:00'}}});
        return route.abort();
      });
      const page = await context.newPage();
      const runtimeErrors=[],consoleErrors=[];
      page.on('pageerror',error=>runtimeErrors.push({url:page.url(),message:error.message}));
      page.on('console',message=>{if(message.type()==='error')consoleErrors.push({url:page.url(),message:message.text()});});
      for (const name of Object.keys(manifest.files).filter(n => n.endsWith('.html') && n !== 'review.html' && !manifest.redirects[n])) {
        const route = '/' + name.replace(/index\.html$/, '');
        const errors = [];
        const listener = error => errors.push(error.message);
        page.on('pageerror', listener);
        const response = await page.goto(origin + route, {waitUntil:'load'});
        assert.equal(response.status(), 200, route);
        await page.evaluate(() => document.fonts.ready);
        const info = await page.evaluate(() => ({
          title: document.title,
          overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
          h1: document.querySelectorAll('h1').length,
          noindex: document.querySelector('meta[name="robots"]')?.content.includes('noindex'),
          privateReviewLabel: document.body.innerText.includes('PRIVATE REVIEW BUILD') || document.body.innerText.includes('PRIVATE REVIEW /'),
          brokenImages: [...document.images].filter(x => x.complete && !x.naturalWidth).map(x => x.src)
        }));
        assert.equal(info.overflow, false, `${width} ${route}: horizontal overflow`);
        assert.equal(info.h1, 1, route);
        assert.equal(info.noindex, name === '404.html', `${width} ${route}: robots state`);
        assert.equal(info.privateReviewLabel, false, `${width} ${route}: private review label`);
        assert.deepEqual(info.brokenImages, [], `${width} ${route}: broken images`);
        assert.deepEqual(errors, [], `${width} ${route}: runtime errors`);
        if (width <= 430) {
          const menu = page.locator('.hdr-burger');
          assert.equal(await menu.getAttribute('aria-label'),'Open menu');
          await menu.click();
          await page.locator('#drawer').waitFor({state:'visible'});
          assert.equal(await page.locator('#main').evaluate(el=>el.inert),true);
          const links=page.locator('#drawer a[href]');
          await links.last().focus();await page.keyboard.press('Tab');
          assert.equal(await menu.evaluate(el=>el===document.activeElement),true,'Drawer traps forward Tab');
          await page.keyboard.press('Shift+Tab');
          assert.equal(await links.last().evaluate(el=>el===document.activeElement),true,'Drawer traps reverse Tab');
          await page.keyboard.press('Escape');
          assert.equal(await menu.getAttribute('aria-expanded'), 'false');
          assert.equal(await menu.evaluate(el=>el===document.activeElement),true,'Escape returns focus');
          assert.equal(await page.locator('#main').evaluate(el=>el.inert),false);
        }
        await page.screenshot({path:path.join(output, `${width}-${name.replaceAll('/', '_')}.png`), fullPage:true});
        results.push({width, route, ...info});
        page.off('pageerror', listener);
      }
      // OS reduced-motion replaces the removed motion toggle.
      for (const route of ['/', '/about.html']) {
        await page.goto(origin + route);
        assert.equal(await page.locator('.motion-toggle').count(), 0);
        assert.equal(await page.evaluate(() => matchMedia('(prefers-reduced-motion: reduce)').matches), true);
        const animations = await page.evaluate(() => [...document.querySelectorAll('main *')].filter(el => {
          const s=getComputedStyle(el);return s.animationName!=='none' && parseFloat(s.animationDuration)>.01;
        }).length);
        assert.equal(animations, 0, 'Reduced motion freezes decorative CSS animations');
      }
      await page.goto(origin + '/faq.html');
      if(width>900){
        const trigger=page.locator('.hdr-link').first();
        await trigger.focus();await page.keyboard.press('Enter');
        assert.equal(await trigger.getAttribute('aria-expanded'),'true');
        await page.keyboard.press('Escape');assert.equal(await trigger.getAttribute('aria-expanded'),'false');
        assert.equal(await trigger.evaluate(el=>el===document.activeElement),true);
      }
      const question = page.locator('main details').first();
      await question.locator('summary').click();
      assert.equal(await question.getAttribute('open'), '');
      await page.goto(origin + '/wall.html');
      assert.equal(await page.locator('#leave-mark').isDisabled(), true);
      await page.locator('#connect-wallet').click();
      await page.locator('#wallet-modal').waitFor({state:'visible'});
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('#wallet-modal').isVisible(),false);
      assert.equal(await page.locator('#connect-wallet').evaluate(el=>el===document.activeElement),true);
      await page.goto(origin + '/lander/');
      assert.equal(await page.locator('#download-card').isVisible(), true);
      assert.equal(await page.locator('#download-card').isDisabled(), true);
      assert.equal(await page.locator('#lander-card').getAttribute('data-certification'), 'preview');
      assert.equal((await page.locator('#registered-card-front .card-brand').innerText()).trim(), 'LANDING');
      assert.equal(await page.locator('#registered-card-front .registered-astronaut').count(), 0);
      assert.equal(await page.locator('#card-id').innerText(), '----');
      await page.locator('#buy-landing').click();
      await page.evaluate(()=>window.__jupiterOptions.onSwapError());
      assert.equal(await page.locator('#download-card').isDisabled(),true);
      await page.evaluate(()=>window.__jupiterOptions.onSuccess({txid:'B'.repeat(88)}));
      await page.waitForFunction(()=>localStorage.getItem('landing:pending-signature'));
      assert.equal(await page.locator('#download-card').isDisabled(),true,'Pending swap cannot download');
      claimMode='confirmed';
      await page.locator('#lander-card[data-certification="confirmed"]').waitFor();
      await page.reload();
      await page.locator('#lander-card[data-certification="confirmed"]').waitFor();
      assert.equal(await page.locator('#card-slot').innerText(),'345,678,901');
      assert.equal(await page.locator('#card-issued').innerText(),'19 OCT 2026');
      assert.equal(await page.locator('#card-proof-link').getAttribute('href'),'https://solscan.io/tx/'+'A'.repeat(88));
      assert.equal(await page.evaluate(()=>localStorage.getItem('landing:pending-signature')),null);
      await page.locator('#lander-name').fill('EXAMPLE LANDER');
      await page.locator('#restore-wallet').fill('CBPwvUZrDQThyM6a54shKPpywvpTyYQQ2Ng7FWPZPM88');
      await page.locator('#restore-card').click();
      await page.locator('#lander-card[data-certification="confirmed"]').waitFor();
      assert.equal(await page.locator('#download-card').isDisabled(), false);
      assert.equal(await page.locator('#card-id').innerText(), '0042');
      assert.equal(await page.locator('#lander-id').inputValue(), '0042');
      async function checkCardLayout() {
        const geometry = await page.evaluate(() => {
          const front = document.getElementById('registered-card-front').getBoundingClientRect();
          const selectors = ['.card-brand', '.card-state', '#card-name', '#card-wallet', '.card-foot', '.card-proof'];
          const boxes = selectors.map(selector => {
            const el = document.querySelector('#registered-card-front ' + selector), r = el.getBoundingClientRect();
            return {selector,left:r.left,right:r.right,top:r.top,bottom:r.bottom,overflow:el.scrollWidth>el.clientWidth+1};
          });
          const intersects = (a,b) => a.left < b.right-1 && a.right > b.left+1 && a.top < b.bottom-1 && a.bottom > b.top+1;
          return {outside:boxes.filter(r=>r.left<front.left-1 || r.right>front.right+1 || r.top<front.top-1 || r.bottom>front.bottom+1 || r.overflow),overlap:intersects(boxes[0],boxes[1]) || intersects(boxes[2],boxes[3]) || intersects(boxes[3],boxes[4]) || intersects(boxes[4],boxes[5])};
        });
        assert.deepEqual(geometry.outside, [], `${width}: card clipping`);
        assert.equal(geometry.overlap, false, `${width}: card overlap`);
      }
      await checkCardLayout();
      const frontSize = await page.locator('#registered-card-front').evaluate(el => ({w:el.clientWidth,h:el.clientHeight}));
      await page.locator('#registered-card-front').screenshot({path:path.join(output, `${width}-certified-lander-card.png`)});
      assert(Math.abs(frontSize.w/frontSize.h - 85.6/53.98) < .01, `${width}: credit-card ratio ${JSON.stringify(frontSize)}`);
      await page.locator('#live-card-flip').click();
      const backSize = await page.locator('#registered-card-back').evaluate(el => ({w:el.clientWidth,h:el.clientHeight,overflow:el.scrollHeight>el.clientHeight+1}));
      assert.deepEqual(backSize, {...frontSize,overflow:false}, 'equal front/back sizes');
      await page.locator('#registered-card-back').screenshot({path:path.join(output, `${width}-certified-lander-back.png`)});
      await page.locator('#live-card-flip').click();
      await page.locator('#registered-card-front').screenshot({path:path.join(output, `${width}-certified-lander-card.png`)});
      const [download] = await Promise.all([page.waitForEvent('download'), page.locator('#download-card').click()]);
      assert.equal(download.suggestedFilename(), 'certified-lander-0042-example-lander.png');
      await download.saveAs(path.join(output, `${width}-certified-lander-export.png`));
      const png=fs.readFileSync(path.join(output, `${width}-certified-lander-export.png`));
      assert.equal(png.subarray(1,4).toString(),'PNG');
      assert(Math.abs(png.readUInt32BE(16)/png.readUInt32BE(20)-85.6/53.98)<.01,'Exported PNG retains physical card ratio');
      fixtureId = 12345678;
      await page.locator('#lander-name').fill('A'.repeat(40));
      await page.locator('#restore-card').click();
      await page.waitForFunction(() => document.getElementById('card-id').textContent === '12345678');
      await checkCardLayout();
      await page.locator('#live-card-flip').click();
      const [reverseDownload]=await Promise.all([page.waitForEvent('download'),page.locator('#download-card').click()]);
      await reverseDownload.saveAs(path.join(output,`${width}-certified-lander-export-from-reverse.png`));
      assert.equal(await page.locator('#registered-card-back').isVisible(),true,'Download restores selected reverse');
      const reversePng=fs.readFileSync(path.join(output,`${width}-certified-lander-export-from-reverse.png`));
      assert(Math.abs(reversePng.readUInt32BE(16)/reversePng.readUInt32BE(20)-85.6/53.98)<.01,'Long-name PNG retains card ratio');
      for (const [alias, target] of Object.entries(manifest.redirects)) {
        await page.goto(origin + '/' + alias + '?ref=1#check');
        await page.waitForURL(origin + target + '?ref=1#check');
      }
      assert.deepEqual(runtimeErrors,[],`${width}: page errors during interactions`);
      assert.deepEqual(consoleErrors,[],`${width}: console errors`);
      console.log(`PASS: ${width}px, all pages, keyboard navigation, card faces and PNG export, aliases, clean JavaScript console.`);
      await context.close();
    }
    fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify({status:'PASS',pages:results.length,widths:[1440,1024,768,430,390,360],results}, null, 2));
    fs.rmSync(path.join(output,'failure.txt'),{force:true});
    console.log(`PASS: ${results.length} production renderings; six widths; indexability state, no private review labels, no overflow, runtime errors or missing images; menus, FAQ, OS reduced-motion safeguards, certified proof/PNG and aliases. External data is fixture-only; live wallet qualification is not asserted.`);
  } finally { await browser.close(); }
})().catch(error => {fs.writeFileSync(path.join(output,'failure.txt'),error.stack); console.error(error); process.exitCode=1;}).finally(() => server.close());
