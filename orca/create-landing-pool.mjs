if (process.env.LANDING_MAINNET_EXECUTE !== "YES") { console.error("BLOCKED: mainnet transaction script. Set LANDING_MAINNET_EXECUTE=YES only if you intentionally want to execute it."); process.exit(1); }

import fs from 'fs';
import {
  createSplashPool,
  setRpc,
  setPayerFromBytes
} from '@orca-so/whirlpools';
import { address } from '@solana/kit';

await setRpc('https://api.mainnet.solana.com');

const secret = new Uint8Array(
  JSON.parse(
    fs.readFileSync(
      '/home/mscal/.config/solana/landing-liquidity.json',
      'utf8'
    )
  )
);

const signer = await setPayerFromBytes(secret);

const SOL = address('So11111111111111111111111111111111111111112');
const LANDING = address('DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ');

const result = await createSplashPool(
  SOL,
  LANDING,
  {
    initialPrice: 10_000_000,
    funder: signer
  }
);

console.log('Funder:', signer.address);
console.log('Pool:', result.poolAddress);
console.log(
  'Initialization cost SOL:',
  Number(result.initializationCost) / 1e9
);
console.log('Instructions:', result.instructions.length);

if (
  result.poolAddress !==
  'GyCQYByuUEMEWErDX6xFSpKC3stsfXJRDsFy4fQb1prq'
) {
  throw new Error('Unexpected pool address - transaction NOT sent');
}

console.log('Sending transaction...');
const signature = await result.callback();
console.log('Signature:', signature);
