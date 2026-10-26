/* Local browser integration of data states, copy and normal/reduced motion.
 * All remote requests are mocked or rejected; no wallet/provider is loaded. */
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'../..'),docs=path.join(root,'docs'),out=path.join(root,'redesign/qa-output');
const server=http.createServer((req,res)=>{
 let file=path.resolve(docs,'.'+new URL(req.url,'http://localhost').pathname);
 if(!file.startsWith(docs+path.sep)&&file!==docs){res.writeHead(403);return res.end()}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404);return res.end()}
 const types={'.html':'text/html','.css':'text/css','.js':'application/javascript','.svg':'image/svg+xml','.woff2':'font/woff2','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp'};
 res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch();const results=[];
 try{
  for(const width of [1440,390]){
   let mode='complete';const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'no-preference'});
   await context.addInitScript(()=>{window.__copies=[];window.__clicks=[];document.addEventListener('click',event=>window.__clicks.push(event.target.outerHTML),true);Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>window.__copies.push(text)}})});
   await context.route('**/*',route=>{
    const u=new URL(route.request().url());if(u.origin===origin)return route.continue();
    assert.equal(u.pathname,'/api/transparency','Unexpected external request');assert.equal(route.request().method(),'GET');
    if(mode==='failure')return route.fulfill({status:200,contentType:'application/json',body:'not JSON'});
    if(mode==='missing')return route.fulfill({json:{updatedAt:'2026-10-19T12:00:00Z',holders:null,market:{priceUsd:null,buys24h:2,sells24h:null}}});
    return route.fulfill({json:{updatedAt:'2026-10-19T12:00:00Z',holders:{totalPositiveOwners:20,independentHolders:12,projectWallets:3,liquidityPools:1,founderControlled:2,exchangeWallets:2,complete:true},market:{priceUsd:1.25,liquidityUsd:100,volume24hUsd:50,buys24h:2,sells24h:3,source:'ISOLATED QA FIXTURE'},liquidity:{landingVaultBalance:{amountRaw:'1000000',decimals:6},solVaultBalance:{amountRaw:'1000000000',decimals:9}}}});
   });
   const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/transparency.html');
   await page.waitForFunction(()=>document.querySelector('[data-reading="independent"]').textContent==='12');
   assert((await page.locator('#coverage-note').innerText()).includes('Complete owner coverage'));
   assert.equal(await page.locator('[data-reading="price"]').innerText(),'$1.25');
   assert.equal(await page.locator('[data-reading="transactions"]').innerText(),'5');
   assert.equal(await page.locator('[data-reading="landingVault"]').innerText(),'1 LANDING');
   assert.equal(await page.locator('[data-reading="solVault"]').innerText(),'1 SOL');
   await page.waitForFunction(()=>document.querySelector('[data-reading="price"]').closest('.channel').dataset.state==='live');
   mode='failure';await page.locator('#refresh-transparency').focus();await page.keyboard.press('Enter');
   await page.waitForFunction(()=>document.getElementById('snapshot-status').textContent.startsWith('REFRESH FAILED'),null,{timeout:5000}).catch(async error=>{console.error({mode,snapshot:await page.locator('#snapshot-status').innerText(),errors});throw error});
   assert.equal(await page.locator('[data-reading="independent"]').innerText(),'12','Retain last known snapshot on refresh failure');
   mode='missing';await page.locator('#refresh-transparency').click();
   await page.waitForFunction(()=>document.querySelector('[data-reading="independent"]').textContent==='Unavailable');
   assert((await page.locator('#coverage-note').innerText()).includes('No counts are inferred'));
   assert.equal(await page.locator('[data-reading="transactions"]').innerText(),'Unavailable','Incomplete buys/sells never become invented totals');
   assert.equal(await page.locator('[data-reading="price"]').innerText(),'Unavailable');
   await page.waitForFunction(()=>document.querySelector('[data-reading="price"]').closest('.channel').dataset.state==='unavailable');
   mode='failure';await page.reload();
   await page.waitForFunction(()=>document.getElementById('snapshot-status').textContent==='EXISTING SOURCE UNAVAILABLE');
   assert.equal(await page.locator('[data-reading="independent"]').innerText(),'Unavailable');
   assert.equal(await page.locator('#refresh-transparency').isDisabled(),false);
   await page.goto(origin+'/');
   const copy=page.locator('[data-copy]').first();const expected=await copy.getAttribute('data-copy');await copy.scrollIntoViewIfNeeded();await page.evaluate(()=>document.fonts.ready);await copy.click();
   if(!(await page.evaluate(()=>window.__copies.length)))console.error(await page.evaluate(()=>({clicks:window.__clicks,scrollY,button:document.querySelector('[data-copy]').outerHTML})));
   assert.deepEqual(await page.evaluate(()=>window.__copies),[expected],'Exactly one handler copies the correct mint');
   await page.evaluate(()=>document.querySelector('.scn.mt').scrollIntoView());
   await page.waitForFunction(()=>document.querySelector('.scn.mt').classList.contains('played'));
   await page.screenshot({path:path.join(out,`${width}-home-normal-motion.png`),fullPage:false});
   await page.emulateMedia({reducedMotion:'reduce'});
   const moving=await page.evaluate(()=>[...document.querySelectorAll('svg')].filter(s=>typeof s.animationsPaused==='function'&&s.querySelector('animateMotion')).some(s=>!s.animationsPaused()));
   assert.equal(moving,false,'Reduced motion pauses native SVG motion');
   await page.screenshot({path:path.join(out,`${width}-home-reduced-motion.png`),fullPage:false});
   assert.deepEqual(errors,[]);results.push({width,status:'PASS'});await context.close();
   console.log(`PASS: ${width}px, complete/missing/offline Transparency, stale snapshot, exact single copy, normal motion startup and reduced SVG motion.`);
  }
  fs.writeFileSync(path.join(out,'data-results.json'),JSON.stringify({status:'PASS',results},null,2)+'\n');
 }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1}).finally(()=>server.close());
