# LANDING Buy Funnel Tracker

Privacy-light first-party event collector for `https://landingcoin.fun/buy/`.

## Events

- `page_view`
- `buy_jupiter_click`
- `copy_contract`
- `telegram_click`
- `reddit_click`
- `x_click`
- `email_click`

## Analytics Engine dataset

Dataset: `landing_buy_funnel`

Schema:

- `blob1` = event
- `blob2` = view_id
- `blob3` = utm_source
- `blob4` = utm_medium
- `blob5` = utm_campaign
- `blob6` = utm_content
- `blob7` = utm_term
- `blob8` = placement
- `blob9` = landing_path
- `blob10` = referrer_host
- `blob11` = country
- `blob12` = device
- `double1` = viewport_width
- `double2` = viewport_height
- `double3` = event_count (always 1)

No IP address, wallet address, email address or persistent user identifier is written to Analytics Engine.

## Deploy

From this directory:

```bash
npm install
npm run check
npm run deploy
```

After deployment, set the landing page collector URL to the Worker `/collect` endpoint.

## Useful queries

### Funnel by campaign

```sql
SELECT
  blob3 AS utm_source,
  blob5 AS utm_campaign,
  uniq(blob2) AS visits,
  uniqIf(blob2, blob1 = 'buy_jupiter_click') AS visitors_with_buy_click,
  round(100.0 * visitors_with_buy_click / visits, 2) AS buy_click_rate
FROM landing_buy_funnel
WHERE timestamp > NOW() - INTERVAL '7' DAY
GROUP BY utm_source, utm_campaign
ORDER BY visits DESC
```

### Buy clicks by placement and device

```sql
SELECT
  blob8 AS placement,
  blob12 AS device,
  count() AS buy_clicks
FROM landing_buy_funnel
WHERE blob1 = 'buy_jupiter_click'
  AND timestamp > NOW() - INTERVAL '7' DAY
GROUP BY placement, device
ORDER BY buy_clicks DESC
```

### Funnel events by campaign

```sql
SELECT
  blob5 AS utm_campaign,
  blob1 AS event,
  count() AS events,
  uniq(blob2) AS unique_views
FROM landing_buy_funnel
WHERE timestamp > NOW() - INTERVAL '7' DAY
GROUP BY utm_campaign, event
ORDER BY utm_campaign, events DESC
```
