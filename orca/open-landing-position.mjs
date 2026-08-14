if (process.env.LANDING_MAINNET_EXECUTE !== "YES") { console.error("BLOCKED: mainnet transaction script. Set LANDING_MAINNET_EXECUTE=YES only if you intentionally want to execute it."); process.exit(1); }

import fs from 'fs';
import {
  openFullRangePosition,
  setRpc,
  setPayerFromBytes
} from '@orca-so/whirlpools';
import { address } from '@solana/kit';

await setRpc('https://api.mainnet.solana.com');

const secret = new Uint8Array(
  JSON.parse(
    fs.readFileSync(
      `${process.env.HOME}/.config/solana/landing-liquidity.json`,
      'utf8'
    )
  )
);

const signer = await setPayerFromBytes(secret);

const POOL = address(
  'GyCQYByuUEMEWErDX6xFSpKC3stsfXJRDsFy4fQb1prq'
);

const result = await openFullRangePosition(
  POOL,
  {
    tokenMaxA: 100_000_000n,
    tokenMaxB: 1_000_000_000_000n
  },
  {
    funder: signer,
    slippageToleranceBps: 100
  }
);

console.log('Owner:', signer.address);
console.log('Position mint:', result.positionMint);
console.log(
  'Initialization cost SOL:',
  Number(result.initializationCost) / 1e9
);
console.log('Instructions:', result.instructions.length);
console.log('MAX SOL:', 0.10);
console.log('MAX LANDING:', 1_000_000);
console.log('Sending LP transaction...');
const signature = await result.callback();
console.log('Signature:', signature);
