const LANDING_MINT = "DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ";
const JUPITER_SWAP_PROGRAM = "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4";
const SOLANA_RPC = "https://solana-rpc.publicnode.com";
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

const servicePage = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Landing Lander Registry</title>
    <meta name="robots" content="noindex, nofollow">
    <style>
      :root { color-scheme: dark; font-family: Inter, system-ui, sans-serif; }
      body { display: grid; min-height: 100vh; margin: 0; place-items: center; background: #080b14; color: #f6f1e7; }
      main { max-width: 36rem; padding: 2rem; text-align: center; }
      p { color: #aeb7c7; }
      strong { color: #34e3c1; }
    </style>
  </head>
  <body>
    <main>
      <h1>Landing Lander Registry</h1>
      <p><strong>Online.</strong> This service verifies finalized LANDING swaps and assigns progressive Lander IDs.</p>
    </main>
  </body>
</html>`;

function isRecord(value: unknown): value is JsonRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
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

async function solanaRpc(method: string, params: unknown[]): Promise<unknown> {
  const response = await fetch(SOLANA_RPC, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
  });

  if (!response.ok) {
    throw new Error(`Solana RPC returned HTTP ${response.status}`);
  }

  const payload: unknown = await response.json();
  if (!isRecord(payload)) throw new Error("Invalid Solana RPC response");
  if (payload.error) {
    const message = isRecord(payload.error) && typeof payload.error.message === "string"
      ? payload.error.message
      : "Solana RPC error";
    throw new Error(message);
  }

  return payload.result;
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

function findRecipient(transaction: SolanaTransaction): [string, bigint] | null {
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

    if (delta > 0n) {
      receivedByOwner.set(item.owner, (receivedByOwner.get(item.owner) ?? 0n) + delta);
    }
  }

  return [...receivedByOwner.entries()]
    .sort((a, b) => (a[1] > b[1] ? -1 : a[1] < b[1] ? 1 : 0))[0] ?? null;
}

async function getLandingBalance(wallet: string): Promise<bigint> {
  const result = await solanaRpc("getTokenAccountsByOwner", [
    wallet,
    { mint: LANDING_MINT },
    { encoding: "jsonParsed", commitment: "finalized" },
  ]);

  if (!isRecord(result) || !Array.isArray(result.value)) {
    throw new Error("Invalid token balance response");
  }

  let total = 0n;
  for (const entry of result.value) {
    if (!isRecord(entry) || !isRecord(entry.account) || !isRecord(entry.account.data)) continue;
    const parsed = entry.account.data.parsed;
    if (!isRecord(parsed) || !isRecord(parsed.info) || !isRecord(parsed.info.tokenAmount)) continue;
    const amount = parsed.info.tokenAmount.amount;
    if (typeof amount === "string") total += BigInt(amount);
  }

  return total;
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

  const [wallet, receivedRaw] = recipient;
  const balanceRaw = await getLandingBalance(wallet);

  return {
    kind: "verified",
    wallet,
    receivedRaw: receivedRaw.toString(),
    balanceRaw: balanceRaw.toString(),
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
