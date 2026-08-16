if (process.env.LANDING_MAINNET_EXECUTE !== "YES") {
  console.error("BLOCKED: mainnet upload script. Set LANDING_MAINNET_EXECUTE=YES only if you intentionally want to upload metadata.");
  process.exit(1);
}

import fs from 'fs';
import { createUmi } from '@metaplex-foundation/umi-bundle-defaults';
import {
  createSignerFromKeypair,
  signerIdentity
} from '@metaplex-foundation/umi';
let irysUploader;
try {
  ({ irysUploader } = await import('@metaplex-foundation/umi-uploader-irys'));
} catch {
  console.error('MISSING DEPENDENCY: install @metaplex-foundation/umi-uploader-irys only when you intentionally need to upload new metadata.');
  process.exit(1);
}

const umi = createUmi('https://api.mainnet.solana.com')
  .use(irysUploader());

const secret = new Uint8Array(
  JSON.parse(
    fs.readFileSync(
      `${process.env.HOME}/.config/solana/landing-mainnet-admin.json`,
      'utf8'
    )
  )
);

const keypair = umi.eddsa.createKeypairFromSecretKey(secret);
const signer = createSignerFromKeypair(umi, keypair);
umi.use(signerIdentity(signer));

const metadata = JSON.parse(
  fs.readFileSync('./assets/landing-coin.json', 'utf8')
);

const uri = await umi.uploader.uploadJson(metadata);

console.log('Metadata URI:', uri);
