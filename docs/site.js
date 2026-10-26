'use strict';
(() => {
 const $=(s,r=document)=>r?.querySelector(s), $$=(s,r=document)=>[...(r?.querySelectorAll(s)||[])];
 const root=document.documentElement, home=!!$('#hero-title');
 const motion=$('.motion-toggle');let paused=matchMedia('(prefers-reduced-motion: reduce)').matches;
 let toastTimer;
 function toast(message){const el=$('#toast');if(!el)return;clearTimeout(toastTimer);el.textContent=message;el.classList.add('visible');toastTimer=setTimeout(()=>el.classList.remove('visible'),3500);}
 function motionState(next){paused=next;root.classList.toggle('motion-paused',next);document.body.classList.toggle('static-motion',next);document.body.classList.toggle('motion-enabled',!next);if(motion){motion.setAttribute('aria-pressed',String(next));motion.setAttribute('aria-label',next?'Resume decorative motion':'Pause decorative motion');$('.pause-icon').textContent=next?'▷':'Ⅱ';$('.motion-label').textContent=next?'MOTION OFF':'MOTION ON';}}
 if(!home){
  motionState(paused);
  motion?.addEventListener('click',()=>{root.classList.toggle('motion-opt-in',paused);motionState(!paused);updatePageMotion();});
  matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',ev=>{root.classList.remove('motion-opt-in');motionState(ev.matches);updatePageMotion();});
  const menu=$('.menu-toggle'),nav=$('#mobile-nav');
  function closeMenu(){if(!nav||!menu)return;nav.hidden=true;menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open navigation');}
  menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')==='true';nav.hidden=open;menu.setAttribute('aria-expanded',String(!open));menu.setAttribute('aria-label',open?'Open navigation':'Close navigation');});
  $$('a',nav).forEach(a=>a.addEventListener('click',closeMenu));
  document.addEventListener('click',ev=>{if(!ev.target.closest('.site-header'))closeMenu();});
  document.addEventListener('keydown',ev=>{if(ev.key==='Escape'&&nav&&!nav.hidden){closeMenu();menu.focus();}});
  matchMedia('(min-width:761px)').addEventListener('change',ev=>{if(ev.matches)closeMenu();});
  $$('.site-header [data-copy]').forEach(button=>button.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(button.dataset.copy);toast('Copied. Check the coordinates before you use them.');}catch(_){toast('Copy unavailable. Select the text to copy it manually.');}}));
 }
 // Native details give keyboard/touch access without hover-only navigation.
 const groups=$$('.site-header .nav-group');
 groups.forEach(group=>group.addEventListener('toggle',()=>{if(group.open)groups.filter(g=>g!==group).forEach(g=>g.open=false);}));
 document.addEventListener('click',ev=>{if(!ev.target.closest('.site-header'))groups.forEach(g=>g.open=false);});
 document.addEventListener('keydown',ev=>{if(ev.key==='Escape'){const open=groups.find(g=>g.open);groups.forEach(g=>g.open=false);if(open)$('summary',open).focus();}});
 $$('.site-header a').forEach(a=>{const u=new URL(a.href,location.href);if(u.origin===location.origin&&u.pathname===location.pathname)a.setAttribute('aria-current','page');});
 let pending=false;
 function updatePageMotion(){pending=false;if(home)return;const h=innerHeight,range=Math.max(1,root.scrollHeight-h),p=Math.min(1,Math.max(0,scrollY/range));root.style.setProperty('--inner-progress',root.classList.contains('motion-paused')?'0':p.toFixed(4));$$('.page-section').forEach(s=>{const v=Math.min(1,Math.max(0,(h*.95-s.getBoundingClientRect().top)/(h*.5)));s.style.setProperty('--section-progress',root.classList.contains('motion-paused')?'1':v.toFixed(4));});}
 function schedule(){if(!pending){pending=true;requestAnimationFrame(updatePageMotion);}}
 if(!home){window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule,{passive:true});document.fonts.ready.then(schedule);schedule();}
 async function getJSON(path){const r=await fetch('https://landing-lander-registry.michelescalini.workers.dev'+path,{cache:'no-store',headers:{accept:'application/json'},signal:AbortSignal.timeout(30000)});let data;try{data=await r.json();}catch(_){throw new Error('The existing service did not return valid data.');}if(!r.ok)throw new Error(data.message||'The existing service is unavailable.');return data;}
 function text(id,value){const el=$('#'+id);if(el)el.textContent=value;}
 function num(value,digits=0){if(value===null||value===undefined||value==='')return null;const n=Number(value);return Number.isFinite(n)?n.toLocaleString('en-US',{maximumFractionDigits:digits}):null;}
 function reading(key,value){const el=$('[data-reading="'+key+'"]');if(!el)return;el.textContent=value??'Unavailable';el.classList.toggle('unavailable',value===null||value===undefined);}
 // Reuse the existing read-only transparency source and classification, not estimates.
 if($('#transparency-live')){
  let loading=false,lastSuccess=null;
  async function load(){if(loading)return;loading=true;const button=$('#refresh-transparency');button.disabled=true;text('snapshot-status','REQUESTING EXISTING SOURCE…');
   try{const data=await getJSON('/api/transparency');lastSuccess=data.updatedAt||null;
    const stamp=data.updatedAt?new Date(data.updatedAt).toLocaleString():'timestamp not supplied';text('snapshot-status','SOURCE SNAPSHOT / '+stamp);
    const h=data.holders;
    if(h&&typeof h==='object'){
     reading('positive',num(h.totalPositiveOwners));reading('independent',num(h.independentHolders));reading('project',num(h.projectWallets));reading('pool',num(h.liquidityPools));reading('founder',num(h.founderControlled));reading('other',num(h.exchangeWallets));
     text('coverage-note',h.complete===true?'Complete owner coverage reported by the existing backend. Source classification and exclusions still apply.':'PARTIAL OWNER COVERAGE — the existing backend is using fallback enumeration. These figures are not a complete holder census. Founder and known operational/exchange classification can include manual exclusions.');
    }else{['positive','independent','project','pool','founder','other'].forEach(k=>reading(k,null));text('coverage-note','Owner readings unavailable in this source response. No counts are inferred.');}
    const l=data.liquidity||{};
    for(const [key,field,ticker]of [['landingVault','landingVaultBalance','LANDING'],['solVault','solVaultBalance','SOL']]){const v=l[field];const amount=v&&v.amountRaw!==undefined&&Number.isInteger(Number(v.decimals))?num(Number(v.amountRaw)/10**Number(v.decimals),6):null;reading(key,amount===null?null:amount+' '+ticker);}
    const m=data.market;
    if(m&&typeof m==='object'){
     const usd=(n,d)=>{const v=num(n,d);return v===null?null:'$'+v;};reading('price',usd(m.priceUsd,8));reading('liquidity',usd(m.liquidityUsd,2));reading('volume',usd(m.volume24hUsd,2));reading('buys',num(m.buys24h));reading('sells',num(m.sells24h));
     const both=m.buys24h!==null&&m.buys24h!==undefined&&m.sells24h!==null&&m.sells24h!==undefined;reading('transactions',both?num(Number(m.buys24h)+Number(m.sells24h)):null);
     text('market-source','SOURCE / '+String(m.source||'existing third-party provider'));text('market-state','Market readings are from the source snapshot above. They can lag or differ from execution quotes.');
    }else{['price','liquidity','volume','transactions','buys','sells'].forEach(k=>reading(k,null));text('market-source','MARKET DATA / UNAVAILABLE');text('market-state','The existing backend did not return current market data. Token facts and available on-chain readings remain separate.');}
   }catch(error){text('snapshot-status',lastSuccess?'REFRESH FAILED / KEEPING LAST SNAPSHOT':'EXISTING SOURCE UNAVAILABLE');if(!lastSuccess){['positive','independent','project','pool','founder','other','landingVault','solVault','price','liquidity','volume','transactions','buys','sells'].forEach(k=>reading(k,null));text('coverage-note','The existing source is not reachable. No current counts are inferred.');text('market-state','Current market readings are unavailable. Use the independent verification links below.');}}
   finally{loading=false;button.disabled=false;}
  }
  $('#refresh-transparency').addEventListener('click',load);load();setInterval(()=>{if(!document.hidden)load();},60000);document.addEventListener('visibilitychange',()=>{if(!document.hidden)load();});
 }
 // Actual Wall records only. Empty batches are not treated as proof the whole Wall is empty.
 function markCard(mark){
  const article=document.createElement('article');article.className='real-mark';let hash=0;for(const c of mark.signature||'')hash=(hash*31+c.charCodeAt(0))|0;article.style.setProperty('--mark-angle',((Math.abs(hash)%7)-3)*.6+'deg');
  const tag=document.createElement('span');tag.className='mono';tag.textContent='LANDING MARK / PUBLIC RECORD';
  const body=document.createElement('p');body.textContent=String(mark.message??'');
  const footer=document.createElement('footer');const wallet=document.createElement('span');const w=String(mark.wallet||'');wallet.textContent=w.length>12?w.slice(0,4)+'…'+w.slice(-4):w||'Wallet not supplied';
  const view=document.createElement('a');view.textContent='Verify ↗';view.href='https://solscan.io/tx/'+encodeURIComponent(mark.signature);view.target='_blank';view.rel='noopener noreferrer';
  footer.append(wallet,view);article.append(tag,body,footer);return article;
 }
 function feedState(feed,message){const p=document.createElement('p');p.className='feed-state';p.textContent=message;feed.replaceChildren(p);}
 const feed=$('#public-wall-feed')||$('#home-wall-feed');
 if(feed){
  const preview=feed.id==='home-wall-feed';const more=$('#wall-load-more');const status=$('#public-wall-status');let before=null,busy=false,shown=0,seen=new Set();
  async function load(reset=false){if(busy)return;busy=true;if(more)more.disabled=true;if(status)status.textContent='CHECKING THE EXISTING PUBLIC RECORD…';
   try{const q=new URLSearchParams({limit:preview?'25':'10'});if(!reset&&before)q.set('before',before);const data=await getJSON('/api/wall/marks?'+q);if(!Array.isArray(data.marks))throw new Error('Unexpected Wall response');
    if(reset){shown=0;before=null;seen.clear();feed.replaceChildren();}
    const marks=data.marks.filter(mark=>typeof mark.message==='string'&&typeof mark.signature==='string'&&!seen.has(mark.signature));
    if(marks.length&&shown===0)feed.replaceChildren();
    for(const mark of marks){if(preview&&shown>=3)break;feed.append(markCard(mark));shown++;seen.add(mark.signature);}
    before=typeof data.nextBefore==='string'?data.nextBefore:null;const hasMore=data.hasMore===true&&!!before;
    if(more)more.hidden=!hasMore;
    if(!shown)feedState(feed,hasMore?'No messages were returned in this transaction batch. Earlier records remain to be checked on the public Wall.':'No public messages were returned in the available record. No sample posts are substituted.');
    if(status)status.textContent=shown+' REAL MESSAGE'+(shown===1?'':'S')+' LOADED'+(hasMore?' / MORE TRANSACTIONS AVAILABLE':' / END OF AVAILABLE RECORD');
   }catch(error){if(!shown)feedState(feed,'The existing Wall service is temporarily unavailable. Open the LANDING Wall page to retry or post. No sample messages are shown.');if(status)status.textContent='EXISTING WALL SERVICE UNAVAILABLE';if(more)more.hidden=true;}
   finally{busy=false;if(more)more.disabled=false;}
  }
  more?.addEventListener('click',()=>load(false));$('#wall-refresh')?.addEventListener('click',()=>load(true));load(true);
 }
})();
