if (process.env.LANDING_MAINNET_EXECUTE !== "YES") { console.error("BLOCKED: mainnet transaction script. Set LANDING_MAINNET_EXECUTE=YES only if you intentionally want to execute it."); process.exit(1); }

import fs from 'fs';
import { createUmi } from '@metaplex-foundation/umi-bundle-defaults';
import {
  publicKey,
  keypairIdentity,
  some
} from '@metaplex-foundation/umi';
import {
  mplTokenMetadata,
  fetchDigitalAsset,
  updateV1
} from '@metaplex-foundation/mpl-token-metadata';

const umi = createUmi('https://api.mainnet.solana.com')
  .use(mplTokenMetadata());

const secret = new Uint8Array(
  JSON.parse(
    fs.readFileSync(
      '/home/mscal/.config/solana/landing-mainnet-admin.json',
      'utf8'
    )
  )
);

const keypair = umi.eddsa.createKeypairFromSecretKey(secret);
umi.use(keypairIdentity(keypair));

const mint = publicKey(
  'DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ'
);

const creator = publicKey(
  '4fUtkW2LEZxLt2tgPJ9BitViNBqR3AUy58hyG81Q41hg'
);

const asset = await fetchDigitalAsset(umi, mint);

const tx = await updateV1(umi, {
  mint,
  authority: umi.identity,
  data: some({
    name: asset.metadata.name,
    symbol: asset.metadata.symbol,
    uri: asset.metadata.uri,
    sellerFeeBasisPoints: asset.metadata.sellerFeeBasisPoints,
    creators: some([
      {
        address: creator,
        verified: false,
        share: 100
      }
    ])
  })
}).sendAndConfirm(umi);

console.log('Creator metadata updated.');
console.log('Signature:', tx.signature);
