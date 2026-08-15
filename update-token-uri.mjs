if (process.env.LANDING_MAINNET_EXECUTE !== "YES") {
  console.error("BLOCKED: mainnet metadata update script. Set LANDING_MAINNET_EXECUTE=YES only if you intentionally want to update token metadata.");
  process.exit(1);
}

import fs from 'fs';
import { createUmi } from '@metaplex-foundation/umi-bundle-defaults';
import {
  keypairIdentity,
  publicKey,
  some
} from '@metaplex-foundation/umi';
import {
  mplTokenMetadata,
  fetchDigitalAsset,
  updateV1
} from '@metaplex-foundation/mpl-token-metadata';
import { base58 } from '@metaplex-foundation/umi/serializers';

const umi = createUmi('https://api.mainnet.solana.com')
  .use(mplTokenMetadata());

const secret = new Uint8Array(
  JSON.parse(
    fs.readFileSync(
      `${process.env.HOME}/.config/solana/landing-mainnet-admin.json`,
      'utf8'
    )
  )
);

const keypair = umi.eddsa.createKeypairFromSecretKey(secret);
umi.use(keypairIdentity(keypair));

const mint = publicKey('DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ');
const newUri = 'https://gateway.irys.xyz/HMjDFXazvaWKVaGciDCkXymf5t66RrpS8XbVEvKVrhHp';

const asset = await fetchDigitalAsset(umi, mint);

const tx = await updateV1(umi, {
  mint,
  authority: umi.identity,
  data: some({
    name: asset.metadata.name,
    symbol: asset.metadata.symbol,
    uri: newUri,
    sellerFeeBasisPoints: asset.metadata.sellerFeeBasisPoints,
    creators: asset.metadata.creators,
  })
}).sendAndConfirm(umi);

console.log('Updated URI:', newUri);
console.log('Signature:', base58.deserialize(tx.signature)[0]);
