if (process.env.LANDING_MAINNET_EXECUTE !== "YES") { console.error("BLOCKED: mainnet transaction script. Set LANDING_MAINNET_EXECUTE=YES only if you intentionally want to execute it."); process.exit(1); }

import fs from 'fs';
import { createUmi } from '@metaplex-foundation/umi-bundle-defaults';
import {
  createSignerFromKeypair,
  publicKey,
  signerIdentity
} from '@metaplex-foundation/umi';
import { base58 } from '@metaplex-foundation/umi/serializers';
import {
  mplTokenMetadata,
  verifyCreatorV1
} from '@metaplex-foundation/mpl-token-metadata';

const umi = createUmi('https://api.mainnet.solana.com')
  .use(mplTokenMetadata());

const creatorSecret = new Uint8Array(
  JSON.parse(
    fs.readFileSync(
      `${process.env.HOME}/.config/solana/landing-creator.json`,
      'utf8'
    )
  )
);

const adminSecret = new Uint8Array(
  JSON.parse(
    fs.readFileSync(
      `${process.env.HOME}/.config/solana/landing-mainnet-admin.json`,
      'utf8'
    )
  )
);

const creatorKeypair = umi.eddsa.createKeypairFromSecretKey(creatorSecret);
const adminKeypair = umi.eddsa.createKeypairFromSecretKey(adminSecret);

const creatorSigner = createSignerFromKeypair(umi, creatorKeypair);
const adminSigner = createSignerFromKeypair(umi, adminKeypair);

umi.use(signerIdentity(creatorSigner));

const metadata = publicKey(
  '5SWeVjptsN8191CB1LQLL9YeVYh5Hje1agcY1gj2tApY'
);

const tx = await verifyCreatorV1(umi, {
  authority: creatorSigner,
  metadata
})
  .setFeePayer(adminSigner)
  .sendAndConfirm(umi);

console.log('Signature:', base58.deserialize(tx.signature)[0]);
