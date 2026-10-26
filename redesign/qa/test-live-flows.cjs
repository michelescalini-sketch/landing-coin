/* Offline contract tests. All wallet signatures and registry records below are
 * isolated test fixtures. No wallet is opened and no request reaches mainnet. */
const assert=require('node:assert/strict');
const fs=require('node:fs');const vm=require('node:vm');const path=require('node:path');
const {webcrypto}=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const web3File=process.argv[2];assert(web3File,'Pass the downloaded pinned @solana/web3.js IIFE path.');
const MINT='DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ';
const RECIPIENT='F7Pio8v6YLwXbwRgQAH8Q7cMqsdaUX3mJeyFyTZbvhhT';
const WALLET='CBPwvUZrDQThyM6a54shKPpywvpTyYQQ2Ng7FWPZPM88';
const API='https://landing-lander-registry.michelescalini.workers.dev';
class Element {
 constructor(tag='div',attrs={}){this.tagName=tag;this.attrs={...attrs};this.hidden='hidden'in attrs;this.disabled='disabled'in attrs;this.value='';this.children=[];this.dataset={};for(const[k,v]of Object.entries(attrs))if(k.startsWith('data-'))this.dataset[k.slice(5)]=v;this.events={};this.textContent='';this.style={setProperty(){}};}
 get id(){return this.attrs.id||''}setAttribute(k,v){this.attrs[k]=String(v)}getAttribute(k){return this.attrs[k]??null}
 addEventListener(k,fn){(this.events[k]??=[]).push(fn)}
 async emit(k,event={}){event.target??=this;for(const fn of this.events[k]||[])await fn(event);}
 appendChild(c){this.children.push(c);return c}append(...cs){this.children.push(...cs)}
 set innerHTML(s){this._html=s;this.children=[]}get innerHTML(){return this._html||''}
 focus(){if(this.doc)this.doc.activeElement=this}querySelectorAll(){return []}remove(){}
 click(){this.clicked=true;return this.emit('click')}scrollIntoView(){}
}
function environment(page,fetcher){
 const source=fs.readFileSync(path.join(root,'docs',page),'utf8');const nodes=new Map();
 for(const m of source.matchAll(/<([a-z][a-z0-9-]*)\b([^>]*\bid="([^"]+)"[^>]*)>/g)){
  const attrs={};for(const a of m[2].matchAll(/([a-z][a-z-]*)(?:="([^"]*)")?/g))attrs[a[1]]=a[2]??'';
  nodes.set(m[3],new Element(m[1],attrs));
 }
 const created=[];const document={getElementById:id=>nodes.get(id)||null,activeElement:null,createElement:tag=>{const e=new Element(tag);created.push(e);return e},body:new Element('body')};
 for(const e of nodes.values())e.doc=document;
 const storage=new Map();const listeners={};
 const win={setTimeout:fn=>{queueMicrotask(fn);return 1},addEventListener:(k,fn)=>(listeners[k]??=[]).push(fn),dispatchEvent:e=>{for(const f of listeners[e.type]||[])f(e)}};
 const context={document,window:win,localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,String(v)),removeItem:k=>storage.delete(k)},console:{log(){},warn(){},error(){}},fetch:fetcher,Response,URL,URLSearchParams,AbortSignal,TextEncoder,TextDecoder,Uint8Array,ArrayBuffer,Buffer,crypto:webcrypto,setTimeout:win.setTimeout,clearTimeout(){},CustomEvent:class{constructor(type,extra={}){this.type=type;Object.assign(this,extra)}},alert:()=>{}};
 vm.createContext(context);return {context,nodes,storage,created,window:win,document};
}
function compile(env,file,hook){let js=fs.readFileSync(path.join(root,file),'utf8');if(hook)js=hook(js);vm.runInContext(js,env.context,{filename:file});}
const settle=()=>new Promise(setImmediate);
function functionText(source,name){const start=source.indexOf('function '+name+'(');assert(start>=0,name);const next=source.indexOf('\n  function ',start+1),asyncNext=source.indexOf('\n  async function ',start+1);const ends=[next,asyncNext].filter(i=>i>=0);return source.slice(start,Math.min(...ends)).trim();}
async function wallTests(){
 const original=fs.readFileSync(path.join(root,'redesign/content/upstream/wall.js'),'utf8'),live=fs.readFileSync(path.join(root,'docs/wall-live.js'),'utf8');
 for(const name of ['encodeTransferChecked','createAtaIdempotentInstruction','createTransferInstruction','createMemoInstruction','associatedTokenAddress','leaveMark'])assert.equal(functionText(live,name),functionText(original,name),'Production transaction function retained: '+name);
 let mode='valid',sent=0,phase=0,allowConfirm;const calls=[];
 const env=environment('wall.html',async(url,options={})=>{
  calls.push({url,options});assert(url.startsWith(API));const u=new URL(url);
  if(u.pathname==='/api/wall/marks')return Response.json({status:'ok',marks:[],nextBefore:null,hasMore:false});
  if(u.pathname==='/api/wall/wallet')return Response.json({status:'ok',wallet:WALLET,totalRaw:mode==='low'?'4999999999':'5000000000',sourceTokenAccount:mode==='low'?null:MINT});
  if(u.pathname==='/api/wall/blockhash')return Response.json({status:'ok',blockhash:'11111111111111111111111111111111',lastValidBlockHeight:1});
  if(u.pathname==='/api/wall/status'){
   if(mode==='invalid')return Response.json({status:'invalid',message:'The transaction failed on-chain.'});
   if(phase++===0)return Response.json({status:'waiting'});
   await new Promise(r=>allowConfirm=r);return Response.json({status:'confirmed'});
  }
  throw new Error('Unexpected test request '+url);
 });
 vm.runInContext(fs.readFileSync(web3File,'utf8'),env.context);env.window.solanaWeb3=env.context.solanaWeb3;
 const w=env.context.solanaWeb3;
 let captured;
 env.window.LandingWalletStandard={list:()=>[],connect:async()=>({address:WALLET,name:'TEST WALLET'}),send:async transaction=>{sent++;captured=transaction;if(mode==='rejected')throw new Error('User rejected');return new Uint8Array(64).fill(1)}};
 compile(env,'docs/wall-live.js',s=>s.replace('  loadNewest();','  globalThis.wallTest = {normalizeMessage, containsLink, connectSelectedWallet, leaveMark, createTransferInstruction, createMemoInstruction, createAtaIdempotentInstruction, associatedTokenAddress, base58Encode};\n  loadNewest();'));
 await settle();const api=env.context.wallTest;
 assert.equal(api.normalizeMessage('a'.repeat(160)).length,140);assert.equal(api.normalizeMessage(' hi\n there '),'hi there');assert(api.containsLink('https://example.com'));
 assert.equal(env.nodes.get('leave-mark').disabled,true);
 mode='low';await api.connectSelectedWallet('TEST WALLET');assert.equal(env.nodes.get('leave-mark').disabled,true);await api.leaveMark();assert.equal(sent,0);
 mode='valid';await api.connectSelectedWallet('TEST WALLET');assert.equal(env.nodes.get('leave-mark').disabled,false);
 env.nodes.get('mark-message').value='https://example.com';await api.leaveMark();assert.equal(sent,0);
 env.nodes.get('mark-message').value='TEST FIXTURE / never broadcast';
 const pending=api.leaveMark();for(let i=0;i<10&&!allowConfirm;i++)await settle();
 assert.equal(sent,1);assert(env.nodes.get('mark-status').textContent.includes('Waiting for final confirmation'));
 assert.equal(captured.instructions.length,3);
 const [ata,transfer,memo]=captured.instructions;
 assert.equal(ata.keys[2].pubkey.toBase58(),RECIPIENT);assert.equal(transfer.keys[1].pubkey.toBase58(),MINT);
 const raw=Buffer.from(transfer.data);assert.equal(raw[0],12);assert.equal(raw.readBigUInt64LE(1),5000000000n);assert.equal(raw[9],6);
 assert.equal(transfer.keys[2].pubkey.toBase58(),api.associatedTokenAddress(new w.PublicKey(RECIPIENT)).toBase58());
 assert.equal(Buffer.from(memo.data).toString(),'LANDING-WALL:v1:TEST FIXTURE / never broadcast');
 allowConfirm();await pending;assert(env.nodes.get('mark-status').textContent.includes('Mark confirmed'));assert.equal(env.nodes.get('mark-message').value,'');
 mode='rejected';env.nodes.get('mark-message').value='TEST REJECTION';await api.leaveMark();assert(!env.nodes.get('mark-status').textContent.includes('Mark confirmed'));assert.equal(env.nodes.get('mark-message').value,'TEST REJECTION');
 mode='invalid';env.nodes.get('mark-message').value='TEST FAILURE';await api.leaveMark();assert(env.nodes.get('mark-status').textContent.includes('failed on-chain'));assert.equal(env.nodes.get('mark-message').value,'TEST FAILURE');
 assert(calls.every(c=>!c.options.method||c.options.method==='GET'),'Wall backend calls remain read-only; signing belongs to the Wallet Standard wallet');
 let signedInput;
 const account={address:WALLET};
 const wallet={name:'ISOLATED TEST WALLET',chains:['solana:mainnet'],accounts:[account],features:{'standard:connect':{connect:async()=>({accounts:[account]})},'solana:signAndSendTransaction':{signAndSendTransaction:async input=>{signedInput=input;return [{signature:new Uint8Array(64).fill(1)}]}}}};
 env.context.__getWallets=()=>({get:()=>[wallet],on(){}});
 compile(env,'docs/wallet-standard.js',s=>s.replace(/import \{ getWallets \} from [^;]+;/,"const getWallets = globalThis.__getWallets;"));
 const bridge=env.window.LandingWalletStandard;assert.equal(bridge.list().length,1);await bridge.connect(wallet.name);await bridge.send(captured);
 assert.equal(signedInput.account,account);assert.equal(signedInput.chain,'solana:mainnet');assert.equal(signedInput.options.skipPreflight,false);
 assert.equal(w.Transaction.from(signedInput.transaction).instructions.length,3);
 assert.equal(Buffer.from(w.Transaction.from(signedInput.transaction).instructions[1].data).readBigUInt64LE(1),5000000000n);
 console.log('PASS: unchanged production transaction functions; 140 characters; no links; insufficient balance; exact recipient/mint/5,000 LANDING/memo; pending vs confirmed; wallet rejection; chain failure. No transaction broadcast.');
}
async function landerTests(){
 let mode='waiting',resolveClaim,canvasCalls=0,initOptions;const calls=[];
 const fixture={id:42,wallet:WALLET,balanceRaw:'123456789',signature:'A'.repeat(88),confirmedSlot:345678901,createdAt:'2026-10-19 12:00:00'};
 const env=environment('lander/index.html',async(url,options={})=>{
  calls.push({url,options});assert(url.startsWith(API));
  if(url.includes('/api/lander?'))return mode==='not-found'?Response.json({status:'not_found'},{status:404}):Response.json({status:'confirmed',lander:fixture});
  assert(url.endsWith('/api/claim'));assert.equal(options.method,'POST');
  if(mode==='invalid')return Response.json({status:'invalid',message:'This is not a finalized Jupiter swap.'},{status:400});
  if(mode==='waiting'){await new Promise(r=>resolveClaim=r);return Response.json({status:'confirmed',lander:fixture});}
  return Response.json({status:'confirmed',lander:fixture});
 });
 env.window.Jupiter={init:o=>{initOptions=o},resume(){},close(){}};
 env.context.html2canvas=async node=>{canvasCalls++;assert.equal(node.id,'registered-card-front');assert.equal(node.hidden,false,'Download captures the visible certified front even when reverse is selected');return {toDataURL:()=> 'data:image/png;base64,TEST_ONLY'}};
 compile(env,'docs/lander-live.js',s=>s.replace('  updateCard();\n  restoreLander();','  globalThis.landerTest = {verifyAndClaim, applyLander, rawLandingToDecimal, formatLanderId};\n  updateCard();\n  restoreLander();'));
 const api=env.context.landerTest;assert.equal(env.nodes.get('download-card').hidden,false);assert.equal(env.nodes.get('download-card').disabled,true);
 await env.nodes.get('download-card').emit('click');assert.equal(canvasCalls,0,'No unissued real-card download');assert.equal(env.nodes.get('download-card').disabled,true);
 await env.nodes.get('buy-landing').emit('click');assert.equal(initOptions.formProps.initialOutputMint,MINT);assert.equal(initOptions.formProps.fixedMint,MINT);
 initOptions.onSwapError();assert.equal(env.nodes.get('download-card').disabled,true);
 assert.throws(()=>api.applyLander({id:0,wallet:WALLET,balanceRaw:'1'}));assert.equal(env.nodes.get('download-card').disabled,true);
 const pending=api.verifyAndClaim('B'.repeat(88));await settle();assert.equal(env.nodes.get('download-card').disabled,true);assert.equal(env.nodes.get('lander-card').dataset.certification,'preview');
 resolveClaim();await pending;assert.equal(env.nodes.get('download-card').disabled,false);assert.equal(env.nodes.get('card-id').textContent,'0042');assert.equal(env.nodes.get('card-back-id').textContent,'0042');assert.equal(env.nodes.get('lander-id').value,'0042');assert.equal(env.nodes.get('lander-balance').value,'123.456789');assert.equal(env.nodes.get('card-slot').textContent,'345,678,901');assert.equal(env.nodes.get('card-issued').textContent,'19 OCT 2026');assert(env.nodes.get('card-signature').textContent.includes('...'));assert.equal(env.nodes.get('card-proof-link').hidden,false);
 assert.equal(env.storage.get('landing:lander-wallet'),WALLET);assert(!env.storage.has('landing:pending-signature'));
 await env.nodes.get('live-card-flip').emit('click');assert.equal(env.nodes.get('registered-card-front').hidden,true);
 await env.nodes.get('download-card').emit('click');assert.equal(canvasCalls,1);assert.equal(env.nodes.get('registered-card-front').hidden,true);
 env.nodes.get('restore-wallet').value=WALLET;mode='not-found';await env.nodes.get('restore-card').emit('click');assert(env.nodes.get('swap-status').textContent.includes('No registered Lander card'));
 mode='confirmed';await env.nodes.get('restore-card').emit('click');assert(env.nodes.get('swap-status').textContent.includes('Existing registry-confirmed card restored'));
 mode='invalid';await api.verifyAndClaim('C'.repeat(88));assert(env.nodes.get('swap-status').textContent.includes('not a finalized'));assert(!env.storage.has('landing:pending-signature'));
 assert.equal(api.rawLandingToDecimal('bad'),'');assert.equal(api.formatLanderId(-1),'');
 console.log('PASS: fixed LANDING Jupiter output; download stays disabled without registry-confirmed finalized proof; waiting/invalid/incomplete claims; registry-only ID/balance/slot/signature/date; pending-state recovery keys; read-only restore; certified PNG target and reverse restoration. Registry responses are isolated fixtures.');
}
async function walletDialogTests(){
 const env=environment('wall.html',async url=>{assert(url.startsWith(API+'/api/wall/marks'));return Response.json({status:'ok',marks:[],nextBefore:null,hasMore:false});});
 vm.runInContext(fs.readFileSync(web3File,'utf8'),env.context);env.window.solanaWeb3=env.context.solanaWeb3;
 env.window.LandingWalletStandard=vm.runInContext("({list:()=>[],connect:async()=>{throw new Error('Connection cancelled');}})",env.context);
 compile(env,'docs/wall-live.js',s=>s.replace('  loadNewest();','  globalThis.modalTest = {connectSelectedWallet};\n  loadNewest();'));
 await settle();const modal=env.nodes.get('wallet-modal'),close=env.nodes.get('wallet-close'),opener=env.nodes.get('connect-wallet');
 await opener.emit('click');await settle();assert.equal(modal.hidden,false);assert.equal(env.document.activeElement,close);
 modal.querySelectorAll=()=>[close];let prevented=false;
 await modal.emit('keydown',{key:'Tab',preventDefault(){prevented=true}});assert(prevented);assert.equal(env.document.activeElement,close);
 const option=new Element('button');option.doc=env.document;modal.querySelectorAll=()=>[close,option];
 await modal.emit('keydown',{key:'Tab',shiftKey:true,preventDefault(){}});assert.equal(env.document.activeElement,option);
 await modal.emit('keydown',{key:'Tab',preventDefault(){}});assert.equal(env.document.activeElement,close);
 await env.context.modalTest.connectSelectedWallet('ISOLATED CANCEL FIXTURE');
 assert.equal(opener.disabled,false);assert.equal(env.nodes.get('leave-mark').disabled,true);assert(env.nodes.get('mark-status').textContent.includes('Connection cancelled'));
 await modal.emit('keydown',{key:'Escape',preventDefault(){}});assert.equal(modal.hidden,true);assert.equal(env.document.activeElement,opener);
 console.log('PASS: simulated wallet-dialog focus entry, forward/reverse Tab boundaries, Escape/return focus, no-wallet and connection-cancellation recovery. No browser keyboard or real wallet action asserted.');
}
async function recoveryTests(){
 const fixture={id:42,wallet:WALLET,balanceRaw:'123456789',signature:'A'.repeat(88),confirmedSlot:345678901,createdAt:'2026-10-19 12:00:00'};
 function boot(fetcher,seed={}){
  const env=environment('lander/index.html',fetcher);
  for(const [k,v]of Object.entries(seed))env.storage.set(k,v);
  env.context.html2canvas=async()=>{throw new Error('ISOLATED EXPORT FAILURE')};
  compile(env,'docs/lander-live.js',s=>s.replace('  updateCard();\n  restoreLander();','  globalThis.recoveryTest={verifyAndClaim,applyLander};\n  updateCard();\n  restoreLander();'));
  return env;
 }
 for(const scenario of ['waiting','network','incomplete','invalid']){
  let attempts=0;
  const env=boot(async(url,options)=>{
   assert.equal(url,API+'/api/claim');assert.equal(options.method,'POST');attempts++;
   if(scenario==='network')throw new Error('ISOLATED OFFLINE');
   if(scenario==='incomplete')return Response.json({status:'confirmed',lander:{...fixture,confirmedSlot:null}});
   if(scenario==='invalid')return Response.json({status:'invalid',message:'The transaction failed on-chain.'},{status:400});
   return Response.json({status:'waiting'});
  });
  await env.context.recoveryTest.verifyAndClaim('B'.repeat(88));
  assert.equal(env.nodes.get('download-card').disabled,true,scenario);
  assert.equal(env.nodes.get('lander-card').dataset.certification,'preview',scenario);
  assert.equal(env.nodes.get('buy-landing').disabled,false,scenario);
  assert.equal(env.storage.has('landing:pending-signature'),scenario!=='invalid',scenario);
  assert.equal(attempts,scenario==='invalid'?1:60,scenario);
 }
 const pending=boot(async(url,options)=>{
  assert.equal(url,API+'/api/claim');assert.equal(JSON.parse(options.body).signature,'B'.repeat(88));
  return Response.json({status:'confirmed',lander:fixture});
 },{'landing:pending-signature':'B'.repeat(88)});
 await settle();assert.equal(pending.nodes.get('card-id').textContent,'0042');assert(!pending.storage.has('landing:pending-signature'));
 const restore=boot(async(url,options)=>{
  assert.equal(url,API+'/api/lander?wallet='+WALLET);assert(!options.method);
  return Response.json({status:'confirmed',lander:fixture});
 },{'landing:lander-wallet':WALLET});
 await settle();assert.equal(restore.nodes.get('card-id').textContent,'0042');assert.equal(restore.nodes.get('download-card').disabled,false);
 for(const [key,value]of [['id',0],['wallet','invalid'],['signature','invalid'],['balanceRaw','0'],['confirmedSlot',0],['createdAt','invalid']]){
  const env=boot(async()=>{throw new Error('No automatic request expected')});
  assert.throws(()=>env.context.recoveryTest.applyLander({...fixture,[key]:value}),key);
  assert.equal(env.nodes.get('download-card').disabled,true,key);
 }
 await restore.nodes.get('live-card-flip').emit('click');
 await restore.nodes.get('download-card').emit('click');
 assert.equal(restore.nodes.get('download-card').disabled,false,'Export failure allows retry');
 assert.equal(restore.nodes.get('registered-card-front').hidden,true,'Export failure restores reverse');
 console.log('PASS: 60-attempt waiting/network/incomplete-proof limits; invalid claim clears pending state; reload resumes pending claim; saved-wallet automatic restore; every proof field required; PNG failure recovery. All responses mocked.');
}
async function wallReadingTests(){
 let stage=0;const requests=[];
 const env=environment('wall.html',async(url,options={})=>{
  requests.push(url);assert(!options.method||options.method==='GET');
  if(stage===2)throw new Error('ISOLATED NETWORK FAILURE');
  if(stage===3)return Response.json({status:'ok',marks:null});
  return Response.json({status:'ok',marks:stage===0?[]:[{signature:'A'.repeat(88),wallet:WALLET,message:'<img src=x onerror=alert(1)>',blockTime:1}],hasMore:stage===0,nextBefore:stage===0?'B'.repeat(88):null});
 });
 vm.runInContext(fs.readFileSync(web3File,'utf8'),env.context);env.window.solanaWeb3=env.context.solanaWeb3;
 compile(env,'docs/wall-live.js',s=>s.replace('  loadNewest();','  globalThis.readingTest={loadPage};\n  loadNewest();'));
 await settle();assert.equal(env.nodes.get('load-more').hidden,false);assert(env.nodes.get('wall-count').textContent.includes('Earlier transactions'));
 stage=1;await env.context.readingTest.loadPage(false);assert(requests.at(-1).includes('before='+ 'B'.repeat(88)));
 const wall=env.nodes.get('wall');assert.equal(wall.children.length,1);assert.equal(wall.children[0].children[1].textContent,'<img src=x onerror=alert(1)>');assert.equal(wall.children[0].children[1].children.length,0,'Wall content remains literal text');
 assert.equal(env.nodes.get('load-more').hidden,true);
 stage=2;await env.context.readingTest.loadPage(false);assert.equal(wall.children.length,1,'Retain loaded marks on service failure');assert.equal(env.nodes.get('load-more').disabled,false);
 stage=3;await env.context.readingTest.loadPage(true);assert(env.nodes.get('wall-count').textContent.includes('unavailable'));
 console.log('PASS: empty transaction batch, pagination cursor, literal message rendering, service failure retaining loaded records, malformed source and retry controls. No real Wall requests.');
}
(async()=>{await wallTests();await landerTests();await walletDialogTests();await recoveryTests();await wallReadingTests();console.log('PASS: offline production-flow contract tests. No real wallet signing, blockchain finalization or live writes were performed.');})().catch(e=>{console.error(e);process.exit(1)});
