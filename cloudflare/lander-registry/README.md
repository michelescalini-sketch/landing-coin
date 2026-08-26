# Landing Lander Registry

Cloudflare Worker and D1 registry for Certified Lander cards.

The service accepts a Solana transaction signature, waits for finalization,
verifies that the transaction used the Jupiter Swap program and delivered the
official LANDING mint to a signing wallet, then assigns that wallet one
progressive Lander ID.

## Local validation

```sh
npm install
npm run types
npx tsc --noEmit
```

## Cloudflare setup

1. Create the D1 database:

   ```sh
   npx wrangler d1 create landing-lander-registry
   ```

2. Add the returned `database_id` to `wrangler.jsonc`.
3. Apply the schema:

   ```sh
   npx wrangler d1 migrations apply landing-lander-registry --remote
   ```

4. Deploy:

   ```sh
   npx wrangler deploy
   ```

The public website should call `POST /api/claim` with JSON shaped as
`{"signature":"<SOLANA_TRANSACTION_SIGNATURE>"}`. Only
`https://landingcoin.fun` and `https://www.landingcoin.fun` receive CORS access.
