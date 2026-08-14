if (process.env.LANDING_MAINNET_EXECUTE !== "YES") { console.error("BLOCKED: mainnet transaction script. Set LANDING_MAINNET_EXECUTE=YES only if you intentionally want to execute it."); process.exit(1); }

import fs from 'fs';
import { createUmi } from '@metaplex-foundation/umi-bundle-defaults';
import {
  createSignerFromKeypair,
  signerIdentity,
  publicKey,
  percentAmount
} from '@metaplex-foundation/umi';
import {
  createV1,
  mplTokenMetadata,
  TokenStandard
} from '@metaplex-foundation/mpl-token-metadata';
import { mplToolbox } from '@metaplex-foundation/mpl-toolbox';
import { base58 } from '@metaplex-foundation/umi/serializers';

const umi = createUmi('https://api.mainnet.solana.com')
  .use(mplTokenMetadata())
  .use(mplToolbox());

const secret = new Uint8Array(
  JSON.parse(
    fs.readFileSync(
      '/home/mscal/.config/solana/landing-mainnet-admin.json',
      'utf8'
    )
  )
);

const keypair = umi.eddsa.createKeypairFromSecretKey(secret);
const signer = createSignerFromKeypair(umi, keypair);
umi.use(signerIdentity(signer));

const mint = publicKey(
  'DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ'
);

const tx = await createV1(umi, {
  mint,
  authority: umi.identity,
  payer: umi.identity,
  updateAuthority: umi.identity,
  name: 'Landing Coin',
  symbol: 'LANDING',
  uri: 'https://gateway.irys.xyz/HjntcMtyuuqCcLuFMDKts73MKFXN4jsHpZGuwFVrYRj3',
  sellerFeeBasisPoints: percentAmount(0),
  tokenStandard: TokenStandard.Fungible,
  isMutable: true
}).sendAndConfirm(umi);

console.log('Signature:', base58.deserialize(tx.signature)[0]);
