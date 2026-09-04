interface Env {
  BUY_ANALYTICS: AnalyticsEngineDataset;
}

type FunnelEvent =
  | "page_view"
  | "buy_jupiter_click"
  | "copy_contract"
  | "telegram_click"
  | "reddit_click"
  | "x_click"
  | "email_click";

const ALLOWED_EVENTS = new Set<FunnelEvent>([
  "page_view",
  "buy_jupiter_click",
  "copy_contract",
  "telegram_click",
  "reddit_click",
  "x_click",
  "email_click",
]);

const ALLOWED_ORIGINS = new Set([
  "https://landingcoin.fun",
  "https://www.landingcoin.fun",
  "http://localhost:8000",
  "http://127.0.0.1:8000",
]);

interface IncomingEvent {
  event?: unknown;
  view_id?: unknown;
  utm_source?: unknown;
  utm_medium?: unknown;
  utm_campaign?: unknown;
  utm_content?: unknown;
  utm_term?: unknown;
  placement?: unknown;
  landing_path?: unknown;
  referrer_host?: unknown;
  viewport_width?: unknown;
  viewport_height?: unknown;
}

function cleanString(value: unknown, maxLength = 180): string {
  if (typeof value !== "string") return "";
  return value
    .replace(/[\u0000-\u001F\u007F]/g, "")
    .trim()
    .slice(0, maxLength);
}

function cleanNumber(value: unknown, min: number, max: number): number {
  const number = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(number)) return 0;
  return Math.max(min, Math.min(max, number));
}

function deviceClass(width: number): string {
  if (width <= 560) return "mobile";
  if (width <= 900) return "tablet";
  return "desktop";
}

function corsHeaders(origin: string): HeadersInit {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Cache-Control": "no-store",
    "Vary": "Origin",
  };
}

function jsonResponse(body: unknown, status = 200, origin = ""): Response {
  const headers: HeadersInit = {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  };

  if (origin && ALLOWED_ORIGINS.has(origin)) {
    Object.assign(headers, corsHeaders(origin));
  }

  return new Response(JSON.stringify(body), { status, headers });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (request.method === "GET" && url.pathname === "/health") {
      return jsonResponse({ ok: true, service: "landing-buy-tracker" });
    }

    if (url.pathname !== "/collect") {
      return jsonResponse({ error: "Not found" }, 404);
    }

    const origin = request.headers.get("Origin") ?? "";

    if (!ALLOWED_ORIGINS.has(origin)) {
      return jsonResponse({ error: "Origin not allowed" }, 403);
    }

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(origin),
      });
    }

    if (request.method !== "POST") {
      return jsonResponse({ error: "Method not allowed" }, 405, origin);
    }

    const bodyText = await request.text();

    if (!bodyText || bodyText.length > 8192) {
      return jsonResponse({ error: "Invalid payload size" }, 413, origin);
    }

    let body: IncomingEvent;

    try {
      body = JSON.parse(bodyText) as IncomingEvent;
    } catch {
      return jsonResponse({ error: "Invalid JSON" }, 400, origin);
    }

    const event = cleanString(body.event, 40) as FunnelEvent;

    if (!ALLOWED_EVENTS.has(event)) {
      return jsonResponse({ error: "Invalid event" }, 400, origin);
    }

    const viewId = cleanString(body.view_id, 64);
    if (!viewId) {
      return jsonResponse({ error: "Missing view_id" }, 400, origin);
    }

    const utmSource = cleanString(body.utm_source, 100) || "direct";
    const utmMedium = cleanString(body.utm_medium, 100);
    const utmCampaign = cleanString(body.utm_campaign, 140);
    const utmContent = cleanString(body.utm_content, 140);
    const utmTerm = cleanString(body.utm_term, 140);
    const placement = cleanString(body.placement, 80);
    const landingPath = cleanString(body.landing_path, 120) || "/buy/";
    const referrerHost = cleanString(body.referrer_host, 180) || "direct";
    const viewportWidth = cleanNumber(body.viewport_width, 0, 10000);
    const viewportHeight = cleanNumber(body.viewport_height, 0, 10000);
    const country = cleanString(request.cf?.country, 8) || "unknown";
    const device = deviceClass(viewportWidth);

    env.BUY_ANALYTICS.writeDataPoint({
      // Stable schema — keep this order in sync with README.md query aliases.
      blobs: [
        event,          // blob1
        viewId,         // blob2
        utmSource,      // blob3
        utmMedium,      // blob4
        utmCampaign,    // blob5
        utmContent,     // blob6
        utmTerm,        // blob7
        placement,      // blob8
        landingPath,    // blob9
        referrerHost,   // blob10
        country,        // blob11
        device,         // blob12
      ],
      doubles: [
        viewportWidth,  // double1
        viewportHeight, // double2
        1,              // double3 — event count
      ],
      indexes: [event],
    });

    return new Response(null, {
      status: 204,
      headers: corsHeaders(origin),
    });
  },
} satisfies ExportedHandler<Env>;
