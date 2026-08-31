const LANDING_MINT = "DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ";
const JUPITER_SWAP_PROGRAM = "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4";
const TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA";
const SOLANA_RPCS = [
  "https://api.mainnet.solana.com",
  "https://solana-rpc.publicnode.com",
];
const ORCA_POOL = "GyCQYByuUEMEWErDX6xFSpKC3stsfXJRDsFy4fQb1prq";
const ORCA_SOL_VAULT = "9ke7GbPNwyK5Pb8gYN4Yob5sVvvX3yQXKT2AD1FkH5ZS";
const ORCA_LANDING_VAULT = "Dbuvyfmnf66cdZ5AwmQwDMFwbFGshEnxKyFHnoY9P6kN";
const GECKOTERMINAL_POOL_API = `https://api.geckoterminal.com/api/v2/networks/solana/pools/${ORCA_POOL}`;

const PROJECT_WALLETS = new Set([
  "CBPwvUZrDQThyM6a54shKPpywvpTyYQQ2Ng7FWPZPM88", // Community
  "3JA9uuNqr5tqBxGP9sQTRTPtwmPAR2KxmJyXyietrQwS", // Treasury
  "34hUkC1XVGMHX64txhfTh7rDBMhtScK8cpCcP54u17vZ", // Liquidity Reserve
  "4fUtkW2LEZxLt2tgPJ9BitViNBqR3AUy58hyG81Q41hg", // Creator
]);

// The user has confirmed that, among currently-positive non-project/non-pool
// owners, two are founder-controlled and one is SuperEx. Until their exact
// addresses are explicitly configured, these are conservative manual counts.
const MANUAL_FOUNDER_HOLDER_COUNT = 2;
const MANUAL_EXCHANGE_HOLDER_COUNT = 1;

const ALLOWED_ORIGINS = new Set([
  "https://landingcoin.fun",
  "https://www.landingcoin.fun",
]);

type JsonRecord = Record<string, unknown>;

type LanderRow = {
  id: number;
  wallet: string;
  signature: string;
  received_raw: string;
  balance_raw: string;
  confirmed_slot: number;
  created_at: string;
};

type Verification =
  | { kind: "waiting" }
  | { kind: "invalid"; reason: string }
  | {
      kind: "verified";
      wallet: string;
      receivedRaw: string;
      balanceRaw: string;
      slot: number;
    };

type Recipient = {
  wallet: string;
  receivedRaw: bigint;
  balanceRaw: bigint;
};

type ParsedAccountKey = {
  pubkey?: unknown;
  signer?: unknown;
};

type TokenBalance = {
  accountIndex?: unknown;
  mint?: unknown;
  owner?: unknown;
  uiTokenAmount?: { amount?: unknown };
};

type SolanaTransaction = {
  slot: number;
  meta?: {
    err?: unknown;
    innerInstructions?: Array<{ instructions?: Array<JsonRecord> }>;
    logMessages?: string[];
    preTokenBalances?: TokenBalance[];
    postTokenBalances?: TokenBalance[];
  };
  transaction?: {
    message?: {
      accountKeys?: Array<string | ParsedAccountKey>;
      instructions?: JsonRecord[];
    };
  };
};

type HolderRecord = {
  owner: string;
  rawBalance: bigint;
  tokenAccounts: string[];
};

type HolderSnapshot = {
  holders: HolderRecord[];
  complete: boolean;
  method: "getProgramAccounts" | "getTokenLargestAccounts";
};

const servicePage = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Landing Public Services</title>
    <meta name="robots" content="noindex, nofollow">
    <style>
      :root { color-scheme: dark; font-family: Inter, system-ui, sans-serif; }
      body { display: grid; min-height: 100vh; margin: 0; place-items: center; background: #080b14; color: #f6f1e7; }
      main { max-width: 40rem; padding: 2rem; text-align: center; }
      p { color: #aeb7c7; line-height: 1.6; }
      strong { color: #34e3c1; }
      code { color: #c7d3e6; }
    </style>
  </head>
  <body>
    <main>
      <h1>Landing Public Services</h1>
      <p><strong>Online.</strong> This Worker verifies finalized LANDING swaps, assigns progressive Lander IDs and exposes the public transparency snapshot used by landingcoin.fun.</p>
      <p><code>GET /api/transparency</code></p>
    </main>
  </body>
</html>`;

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function asRecord(value: unknown): JsonRecord | null {
  return isRecord(value) ? value : null;
}

function corsHeaders(request: Request): HeadersInit {
  const origin = request.headers.get("origin");
  if (!origin || !ALLOWED_ORIGINS.has(origin)) return {};

  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function json(
  request: Request,
  body: JsonRecord,
  status = 200,
  extraHeaders: HeadersInit = {},
): Response {
  return Response.json(body, {
    status,
    headers: {
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
      ...corsHeaders(request),
      ...extraHeaders,
    },
  });
}

async function rpcRequest(endpoint: string, method: string, params: unknown[]): Promise<unknown> {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const payload: unknown = await response.json();
  if (!isRecord(payload)) throw new Error("Invalid JSON-RPC response");
  if (payload.error) {
    const message = isRecord(payload.error) && typeof payload.error.message === "string"
      ? payload.error.message
      : "Solana RPC error";
    throw new Error(message);
  }

  return payload.result;
}

async function solanaRpc(method: string, params: unknown[]): Promise<unknown> {
  const failures: string[] = [];

  for (const endpoint of SOLANA_RPCS) {
    try {
      return await rpcRequest(endpoint, method, params);
    } catch (error) {
      failures.push(`${endpoint}: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  throw new Error(`${method} failed on all configured RPC endpoints: ${failures.join(" | ")}`);
}

function publicKey(entry: unknown): string {
  if (typeof entry === "string") return entry;
  if (!isRecord(entry)) return "";
  return typeof entry.pubkey === "string" ? entry.pubkey : "";
}

function isSolanaTransaction(value: unknown): value is SolanaTransaction {
  return isRecord(value) && typeof value.slot === "number";
}

function transactionUsesJupiter(transaction: SolanaTransaction): boolean {
  const message = transaction.transaction?.message;
  const meta = transaction.meta;
  const accountKeys = (message?.accountKeys ?? []).map(publicKey);
  const instructions = [
    ...(message?.instructions ?? []),
    ...((meta?.innerInstructions ?? []).flatMap((group) => group.instructions ?? [])),
  ];

  return accountKeys.includes(JUPITER_SWAP_PROGRAM)
    || instructions.some((instruction) => publicKey(instruction.programId) === JUPITER_SWAP_PROGRAM)
    || (meta?.logMessages ?? []).some((line) => line.includes(JUPITER_SWAP_PROGRAM));
}

function findRecipient(transaction: SolanaTransaction): Recipient | null {
  const message = transaction.transaction?.message;
  const signerSet = new Set(
    (message?.accountKeys ?? [])
      .filter((entry) => isRecord(entry) && entry.signer === true)
      .map(publicKey),
  );
  const preByIndex = new Map<number, bigint>();

  for (const item of transaction.meta?.preTokenBalances ?? []) {
    if (
      item.mint === LANDING_MINT
      && typeof item.accountIndex === "number"
      && typeof item.uiTokenAmount?.amount === "string"
    ) {
      preByIndex.set(item.accountIndex, BigInt(item.uiTokenAmount.amount));
    }
  }

  const receivedByOwner = new Map<string, bigint>();
  const balanceByOwner = new Map<string, bigint>();
  for (const item of transaction.meta?.postTokenBalances ?? []) {
    if (
      item.mint !== LANDING_MINT
      || typeof item.owner !== "string"
      || !signerSet.has(item.owner)
      || typeof item.accountIndex !== "number"
      || typeof item.uiTokenAmount?.amount !== "string"
    ) {
      continue;
    }

    const post = BigInt(item.uiTokenAmount.amount);
    const pre = preByIndex.get(item.accountIndex) ?? 0n;
    const delta = post - pre;

    balanceByOwner.set(item.owner, (balanceByOwner.get(item.owner) ?? 0n) + post);

    if (delta > 0n) {
      receivedByOwner.set(item.owner, (receivedByOwner.get(item.owner) ?? 0n) + delta);
    }
  }

  const winner = [...receivedByOwner.entries()]
    .sort((a, b) => (a[1] > b[1] ? -1 : a[1] < b[1] ? 1 : 0))[0];

  if (!winner) return null;

  return {
    wallet: winner[0],
    receivedRaw: winner[1],
    balanceRaw: balanceByOwner.get(winner[0]) ?? winner[1],
  };
}

async function verifySwap(signature: string): Promise<Verification> {
  const statusResult = await solanaRpc("getSignatureStatuses", [
    [signature],
    { searchTransactionHistory: true },
  ]);

  if (!isRecord(statusResult) || !Array.isArray(statusResult.value)) {
    throw new Error("Invalid transaction status response");
  }

  const status = statusResult.value[0];
  if (!isRecord(status) || status.confirmationStatus !== "finalized") {
    return { kind: "waiting" };
  }

  if (status.err) {
    return { kind: "invalid", reason: "The transaction failed on-chain." };
  }

  const transactionResult = await solanaRpc("getTransaction", [
    signature,
    {
      commitment: "finalized",
      encoding: "jsonParsed",
      maxSupportedTransactionVersion: 0,
    },
  ]);

  if (
    !isSolanaTransaction(transactionResult)
    || transactionResult.meta?.err
    || !transactionUsesJupiter(transactionResult)
  ) {
    return { kind: "invalid", reason: "This is not a finalized Jupiter swap." };
  }

  const recipient = findRecipient(transactionResult);
  if (!recipient) {
    return { kind: "invalid", reason: "The swap did not deliver LANDING to its signer." };
  }

  return {
    kind: "verified",
    wallet: recipient.wallet,
    receivedRaw: recipient.receivedRaw.toString(),
    balanceRaw: recipient.balanceRaw.toString(),
    slot: transactionResult.slot,
  };
}

function normalizeLander(row: LanderRow): JsonRecord {
  return {
    id: Number(row.id),
    wallet: row.wallet,
    signature: row.signature,
    receivedRaw: row.received_raw,
    balanceRaw: row.balance_raw,
    confirmedSlot: Number(row.confirmed_slot),
    createdAt: row.created_at,
  };
}

async function claimLander(request: Request, env: Env): Promise<Response> {
  const contentLength = Number(request.headers.get("content-length") ?? "0");
  if (contentLength > 2048) {
    return json(request, { status: "invalid", message: "Request too large." }, 413);
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return json(request, { status: "invalid", message: "Invalid JSON request." }, 400);
  }

  const signature = isRecord(body) && typeof body.signature === "string"
    ? body.signature.trim()
    : "";

  if (!/^[1-9A-HJ-NP-Za-km-z]{64,100}$/.test(signature)) {
    return json(request, { status: "invalid", message: "Invalid Solana transaction signature." }, 400);
  }

  const existingSignature = await env.DB.prepare(
    "SELECT * FROM landers WHERE signature = ?1 LIMIT 1",
  ).bind(signature).first<LanderRow>();

  if (existingSignature) {
    return json(request, {
      status: "confirmed",
      existing: true,
      lander: normalizeLander(existingSignature),
    });
  }

  let verification: Verification;
  try {
    verification = await verifySwap(signature);
  } catch (error) {
    console.warn(JSON.stringify({
      message: "Unable to verify Solana transaction",
      signature,
      error: error instanceof Error ? error.message : String(error),
    }));
    return json(request, {
      status: "waiting",
      message: "The network is still being checked. Please wait…",
    }, 202, { "Retry-After": "3" });
  }

  if (verification.kind === "waiting") {
    return json(request, {
      status: "waiting",
      message: "Waiting for finalized on-chain confirmation…",
    }, 202, { "Retry-After": "3" });
  }

  if (verification.kind === "invalid") {
    return json(request, { status: "invalid", message: verification.reason }, 422);
  }

  const existingWallet = await env.DB.prepare(
    "SELECT * FROM landers WHERE wallet = ?1 LIMIT 1",
  ).bind(verification.wallet).first<LanderRow>();

  if (existingWallet) {
    return json(request, {
      status: "confirmed",
      existing: true,
      lander: normalizeLander(existingWallet),
    });
  }

  try {
    const inserted = await env.DB.prepare(`
      INSERT INTO landers (
        wallet, signature, received_raw, balance_raw, confirmed_slot
      ) VALUES (?1, ?2, ?3, ?4, ?5)
      RETURNING *
    `).bind(
      verification.wallet,
      signature,
      verification.receivedRaw,
      verification.balanceRaw,
      verification.slot,
    ).first<LanderRow>();

    if (!inserted) throw new Error("Insert returned no Lander record");

    return json(request, {
      status: "confirmed",
      existing: false,
      lander: normalizeLander(inserted),
    }, 201);
  } catch (error) {
    const raced = await env.DB.prepare(
      "SELECT * FROM landers WHERE wallet = ?1 OR signature = ?2 ORDER BY id LIMIT 1",
    ).bind(verification.wallet, signature).first<LanderRow>();

    if (raced) {
      return json(request, {
        status: "confirmed",
        existing: true,
        lander: normalizeLander(raced),
      });
    }

    console.error(JSON.stringify({
      message: "Unable to assign Lander ID",
      wallet: verification.wallet,
      error: error instanceof Error ? error.message : String(error),
    }));
    return json(request, { status: "error", message: "Unable to assign a Lander ID." }, 500);
  }
}

async function findLander(request: Request, env: Env, url: URL): Promise<Response> {
  const wallet = (url.searchParams.get("wallet") ?? "").trim();
  if (!/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(wallet)) {
    return json(request, { status: "invalid", message: "Invalid Solana wallet." }, 400);
  }

  const row = await env.DB.prepare(
    "SELECT * FROM landers WHERE wallet = ?1 LIMIT 1",
  ).bind(wallet).first<LanderRow>();

  return row
    ? json(request, { status: "confirmed", lander: normalizeLander(row) })
    : json(request, { status: "not_found" }, 404);
}

function parseTokenAccount(entry: unknown): { tokenAccount: string; owner: string; rawBalance: bigint } | null {
  if (!isRecord(entry)) return null;
  const tokenAccount = typeof entry.pubkey === "string" ? entry.pubkey : "";
  const account = asRecord(entry.account);
  const data = account ? asRecord(account.data) : null;
  const parsed = data ? asRecord(data.parsed) : null;
  const info = parsed ? asRecord(parsed.info) : null;
  const tokenAmount = info ? asRecord(info.tokenAmount) : null;
  const owner = info && typeof info.owner === "string" ? info.owner : "";
  const amount = tokenAmount && typeof tokenAmount.amount === "string" ? tokenAmount.amount : "";
  if (!tokenAccount || !owner || !/^\d+$/.test(amount)) return null;
  return { tokenAccount, owner, rawBalance: BigInt(amount) };
}

function aggregateHolders(accounts: Array<{ tokenAccount: string; owner: string; rawBalance: bigint }>): HolderRecord[] {
  const byOwner = new Map<string, HolderRecord>();
  for (const account of accounts) {
    if (account.rawBalance <= 0n) continue;
    const current = byOwner.get(account.owner) ?? {
      owner: account.owner,
      rawBalance: 0n,
      tokenAccounts: [],
    };
    current.rawBalance += account.rawBalance;
    current.tokenAccounts.push(account.tokenAccount);
    byOwner.set(account.owner, current);
  }
  return [...byOwner.values()].sort((a, b) => a.rawBalance > b.rawBalance ? -1 : a.rawBalance < b.rawBalance ? 1 : 0);
}

async function fetchHoldersViaLargestAccounts(): Promise<HolderSnapshot> {
  const largestResult = await solanaRpc("getTokenLargestAccounts", [LANDING_MINT, { commitment: "finalized" }]);
  if (!isRecord(largestResult) || !Array.isArray(largestResult.value)) {
    throw new Error("Invalid getTokenLargestAccounts response");
  }

  const addresses = largestResult.value
    .map((item) => isRecord(item) && typeof item.address === "string" ? item.address : "")
    .filter(Boolean);

  if (!addresses.length) return { holders: [], complete: true, method: "getTokenLargestAccounts" };

  const accountResult = await solanaRpc("getMultipleAccounts", [
    addresses,
    { commitment: "finalized", encoding: "jsonParsed" },
  ]);

  if (!isRecord(accountResult) || !Array.isArray(accountResult.value)) {
    throw new Error("Invalid getMultipleAccounts response");
  }

  const parsedAccounts = accountResult.value.map((account, index) => parseTokenAccount({
    pubkey: addresses[index],
    account,
  })).filter((item): item is NonNullable<typeof item> => item !== null);

  return {
    holders: aggregateHolders(parsedAccounts),
    complete: addresses.length < 20,
    method: "getTokenLargestAccounts",
  };
}

async function fetchHoldersViaProgramAccounts(): Promise<HolderSnapshot> {
  const result = await solanaRpc("getProgramAccounts", [
    TOKEN_PROGRAM,
    {
      commitment: "finalized",
      encoding: "jsonParsed",
      filters: [
        { dataSize: 165 },
        { memcmp: { offset: 0, bytes: LANDING_MINT } },
      ],
    },
  ]);

  if (!Array.isArray(result)) throw new Error("Invalid getProgramAccounts response");
  const accounts = result.map(parseTokenAccount).filter((item): item is NonNullable<typeof item> => item !== null);
  return { holders: aggregateHolders(accounts), complete: true, method: "getProgramAccounts" };
}

async function fetchHolderSnapshot(): Promise<HolderSnapshot> {
  try {
    return await fetchHoldersViaLargestAccounts();
  } catch (largestError) {
    console.warn(JSON.stringify({
      message: "getTokenLargestAccounts unavailable; trying getProgramAccounts",
      error: largestError instanceof Error ? largestError.message : String(largestError),
    }));
    return await fetchHoldersViaProgramAccounts();
  }
}

function classifyHolders(snapshot: HolderSnapshot): JsonRecord {
  const project = snapshot.holders.filter((holder) => PROJECT_WALLETS.has(holder.owner));
  const liquidityPool = snapshot.holders.filter((holder) =>
    holder.owner === ORCA_POOL || holder.tokenAccounts.includes(ORCA_LANDING_VAULT)
  );
  const knownOwners = new Set([
    ...project.map((holder) => holder.owner),
    ...liquidityPool.map((holder) => holder.owner),
  ]);
  const otherwiseExternal = snapshot.holders.filter((holder) => !knownOwners.has(holder.owner));
  const founderCount = Math.min(MANUAL_FOUNDER_HOLDER_COUNT, otherwiseExternal.length);
  const afterFounder = Math.max(0, otherwiseExternal.length - founderCount);
  const exchangeCount = Math.min(MANUAL_EXCHANGE_HOLDER_COUNT, afterFounder);
  const independentCount = Math.max(0, afterFounder - exchangeCount);

  return {
    totalPositiveOwners: snapshot.holders.length,
    complete: snapshot.complete,
    enumerationMethod: snapshot.method,
    projectWallets: project.length,
    liquidityPools: liquidityPool.length,
    externalBeforeManualClassification: otherwiseExternal.length,
    founderControlled: founderCount,
    exchangeWallets: exchangeCount,
    independentHolders: independentCount,
    founderClassification: "manual-count-until-addresses-are-configured",
    exchangeClassification: "manual-count-until-address-is-configured",
    independentDefinition: "positive owners excluding known project, pool, founder and known exchange holders",
  };
}

async function fetchMintState(): Promise<JsonRecord> {
  const result = await solanaRpc("getAccountInfo", [
    LANDING_MINT,
    { commitment: "finalized", encoding: "jsonParsed" },
  ]);
  if (!isRecord(result)) throw new Error("Invalid mint account response");
  const value = asRecord(result.value);
  const data = value ? asRecord(value.data) : null;
  const parsed = data ? asRecord(data.parsed) : null;
  const info = parsed ? asRecord(parsed.info) : null;
  if (!info) throw new Error("Unable to parse mint state");

  return {
    supplyRaw: typeof info.supply === "string" ? info.supply : null,
    decimals: typeof info.decimals === "number" ? info.decimals : null,
    mintAuthority: typeof info.mintAuthority === "string" ? info.mintAuthority : null,
    freezeAuthority: typeof info.freezeAuthority === "string" ? info.freezeAuthority : null,
    isInitialized: info.isInitialized === true,
  };
}

async function fetchTokenAccountState(address: string): Promise<JsonRecord> {
  const result = await solanaRpc("getAccountInfo", [
    address,
    { commitment: "finalized", encoding: "jsonParsed" },
  ]);
  if (!isRecord(result)) throw new Error("Invalid token account response");
  const value = asRecord(result.value);
  const data = value ? asRecord(value.data) : null;
  const parsed = data ? asRecord(data.parsed) : null;
  const info = parsed ? asRecord(parsed.info) : null;
  const tokenAmount = info ? asRecord(info.tokenAmount) : null;
  if (!info || !tokenAmount) throw new Error("Unable to parse token account state");

  return {
    owner: typeof info.owner === "string" ? info.owner : null,
    mint: typeof info.mint === "string" ? info.mint : null,
    amountRaw: typeof tokenAmount.amount === "string" ? tokenAmount.amount : null,
    decimals: typeof tokenAmount.decimals === "number" ? tokenAmount.decimals : null,
    uiAmountString: typeof tokenAmount.uiAmountString === "string" ? tokenAmount.uiAmountString : null,
  };
}

async function fetchMarketState(): Promise<JsonRecord | null> {
  try {
    const response = await fetch(GECKOTERMINAL_POOL_API, {
      headers: { accept: "application/json" },
      cf: { cacheTtl: 30, cacheEverything: true },
    });
    if (!response.ok) throw new Error(`GeckoTerminal HTTP ${response.status}`);
    const payload: unknown = await response.json();
    const root = asRecord(payload);
    const data = root ? asRecord(root.data) : null;
    const attributes = data ? asRecord(data.attributes) : null;
    if (!attributes) throw new Error("Invalid GeckoTerminal response");
    const volumes = asRecord(attributes.volume_usd);
    const transactions = asRecord(attributes.transactions);
    const h24 = transactions ? asRecord(transactions.h24) : null;
    return {
      priceUsd: typeof attributes.base_token_price_usd === "string" ? attributes.base_token_price_usd : null,
      liquidityUsd: typeof attributes.reserve_in_usd === "string" ? attributes.reserve_in_usd : null,
      volume24hUsd: volumes && typeof volumes.h24 === "string" ? volumes.h24 : null,
      buys24h: h24 && typeof h24.buys === "number" ? h24.buys : null,
      sells24h: h24 && typeof h24.sells === "number" ? h24.sells : null,
      source: "GeckoTerminal",
    };
  } catch (error) {
    console.warn(JSON.stringify({
      message: "Unable to fetch GeckoTerminal market state",
      error: error instanceof Error ? error.message : String(error),
    }));
    return null;
  }
}

async function transparencySnapshot(request: Request): Promise<Response> {
  const updatedAt = new Date().toISOString();
  const [mintResult, holderResult, landingVaultResult, solVaultResult, marketResult] = await Promise.allSettled([
    fetchMintState(),
    fetchHolderSnapshot(),
    fetchTokenAccountState(ORCA_LANDING_VAULT),
    fetchTokenAccountState(ORCA_SOL_VAULT),
    fetchMarketState(),
  ]);

  const mint = mintResult.status === "fulfilled" ? mintResult.value : null;
  const holders = holderResult.status === "fulfilled" ? classifyHolders(holderResult.value) : null;
  const landingVault = landingVaultResult.status === "fulfilled" ? landingVaultResult.value : null;
  const solVault = solVaultResult.status === "fulfilled" ? solVaultResult.value : null;
  const market = marketResult.status === "fulfilled" ? marketResult.value : null;

  const errors: string[] = [];
  if (!mint) errors.push(`mint_state_unavailable${mintResult.status === "rejected" ? `: ${String(mintResult.reason)}` : ""}`);
  if (!holders) errors.push(`holder_state_unavailable${holderResult.status === "rejected" ? `: ${String(holderResult.reason)}` : ""}`);
  if (!landingVault) errors.push(`landing_vault_unavailable${landingVaultResult.status === "rejected" ? `: ${String(landingVaultResult.reason)}` : ""}`);
  if (!solVault) errors.push(`sol_vault_unavailable${solVaultResult.status === "rejected" ? `: ${String(solVaultResult.reason)}` : ""}`);
  if (!market) errors.push("market_state_unavailable");

  return json(request, {
    status: errors.length ? "partial" : "ok",
    updatedAt,
    token: {
      mint: LANDING_MINT,
      network: "solana-mainnet",
      tokenProgram: TOKEN_PROGRAM,
      ...mint,
    },
    holders,
    liquidity: {
      pool: ORCA_POOL,
      landingVault: ORCA_LANDING_VAULT,
      solVault: ORCA_SOL_VAULT,
      landingVaultBalance: landingVault,
      solVaultBalance: solVault,
    },
    market,
    methodology: {
      positiveHolder: "unique token-account owner with aggregate LANDING balance greater than zero",
      projectWallets: [...PROJECT_WALLETS],
      founderHolderCountManual: MANUAL_FOUNDER_HOLDER_COUNT,
      exchangeHolderCountManual: MANUAL_EXCHANGE_HOLDER_COUNT,
      notes: "Founder and exchange classifications remain manual until their exact holding addresses are explicitly configured. No personal or trader addresses are returned by this endpoint.",
    },
    sources: {
      solanaRpcFallbacks: SOLANA_RPCS,
      market: GECKOTERMINAL_POOL_API,
    },
    errors,
  });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    try {
      if (request.method === "OPTIONS") {
        return new Response(null, { status: 204, headers: corsHeaders(request) });
      }

      if (url.pathname === "/" && request.method === "GET") {
        return new Response(servicePage, {
          headers: {
            "Content-Type": "text/html; charset=utf-8",
            "X-Content-Type-Options": "nosniff",
          },
        });
      }

      if (url.pathname === "/api/transparency" && request.method === "GET") {
        return await transparencySnapshot(request);
      }

      if (url.pathname === "/api/claim" && request.method === "POST") {
        return await claimLander(request, env);
      }

      if (url.pathname === "/api/lander" && request.method === "GET") {
        return await findLander(request, env, url);
      }

      return json(request, { status: "not_found" }, 404);
    } catch (error) {
      console.error(JSON.stringify({
        message: "Unhandled request error",
        method: request.method,
        path: url.pathname,
        error: error instanceof Error ? error.message : String(error),
      }));
      return json(request, { status: "error", message: "Internal server error." }, 500);
    }
  },
} satisfies ExportedHandler<Env>;
