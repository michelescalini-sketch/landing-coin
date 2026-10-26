/* Offline, read-only QA entry point. No blockchain/admin script is executed. */
const fs=require('node:fs'),path=require('node:path');
const {spawnSync}=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const python=process.env.PYTHON_BIN||(process.platform==='win32'?'python':'python3');
let web3=process.env.WEB3_IIFE;
if(!web3){try{web3=require.resolve('@solana/web3.js/lib/index.iife.min.js')}catch{}}
if(!web3||!fs.existsSync(web3))throw new Error('Set WEB3_IIFE to the pinned @solana/web3.js@1.98.4 IIFE used by offline QA.');
const env={...process.env,PYTHON_BIN:python,PYTHONUTF8:'1'};
for(const name of ['verify-migration.py','verify-content.py','audit-final.py','verify-generator.py']){
 const run=spawnSync(python,[path.join(__dirname,name)],{cwd:root,env,stdio:'inherit'});
 if(run.error)throw run.error;if(run.status!==0)process.exit(run.status||1);
}
for(const name of ['test-live-flows.cjs','preproduction-dom-smoke.cjs']){
 const run=spawnSync(process.execPath,[path.join(__dirname,name),web3],{cwd:root,env,stdio:'inherit'});
 if(run.error)throw run.error;if(run.status!==0)process.exit(run.status||1);
}
console.log('PASS: complete offline QA suite. Browser QA: npm run test:browser with isolated browser dependencies.');
