<?xml version='1.0' encoding='UTF-8'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom" version="1.0">
<xsl:output method="html" encoding="UTF-8"/>
<xsl:template match="/">
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LANDING Coin News — RSS Feed</title>
  <style>
@import url('/style.css');
body{margin:0;background:#0b0d12;color:#f4f3ec;font-family:'DM Sans',Arial,sans-serif;min-height:100vh}
.wrap{max-width:1000px;width:calc(100% - 48px);margin:auto;padding-bottom:50px}
.top{display:flex;justify-content:space-between;align-items:center;padding:26px 0;border-bottom:1px solid #2c3038;gap:20px}
.brand{display:flex;gap:12px;align-items:center;font-family:'Space Grotesk',Arial,sans-serif;font-size:1.25rem;font-weight:700;letter-spacing:.06em}.brand img{width:38px;height:38px;border-radius:50%}.home{padding:10px 16px;border:1px solid #62646b;border-radius:7px;font-size:.875rem}
.wrap .hero{display:block;min-height:0;padding:50px 0 30px;margin:0}.wrap .hero h1{font-family:'Space Grotesk',Arial,sans-serif;font-size:clamp(2.5rem,7vw,4rem);line-height:1.1;letter-spacing:-.06em;margin:20px 0}.eyebrow{font-size:.75rem;letter-spacing:.12em;color:#ffc44f}.wrap .hero p{max-width:760px;line-height:1.7;font-size:1rem;color:#a5a8b1}
.note{padding:20px 24px;background:#191813;border:1px solid #393326;border-radius:8px;font-size:.9375rem;line-height:1.7;color:#d4d4cf;overflow-wrap:anywhere}.item{display:block;padding:28px;background:#12151b;border:1px solid #2c3038;border-radius:10px;margin-top:20px}.item:hover{border-color:#ffc44f}.item h2{font-family:'Space Grotesk',Arial,sans-serif;font-size:1.8rem;line-height:1.2;letter-spacing:-.04em;margin:12px 0}.date{color:#a5a8b1;font-size:.8125rem}.item p{font-size:1rem;line-height:1.7;color:#a5a8b1}footer{margin-top:45px;padding-top:24px;border-top:1px solid #2c3038;color:#a5a8b1;font-size:.8125rem}@media(max-width:560px){.wrap{width:calc(100% - 40px)}.brand{font-size:1rem}.item{padding:24px}.item h2{font-size:1.5rem}}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <a class="brand" href="/"><img src="/assets/landing-logo-96.webp" alt="Landing Coin logo"/>LANDING COIN</a>
    <a class="home" href="/news/">News</a>
  </div>
  <section class="hero">
    <div class="eyebrow">RSS FEED</div>
    <h1>LANDING NEWS</h1>
    <p><xsl:value-of select="rss/channel/description"/></p>
  </section>
  <div class="note">This is the LANDING Coin RSS feed. Add <strong>https://landingcoin.fun/news/feed.xml</strong> to any RSS reader to follow new articles automatically.</div>
  <xsl:for-each select="rss/channel/item">
    <a class="item">
      <xsl:attribute name="href"><xsl:value-of select="link"/></xsl:attribute>
      <div class="date"><xsl:value-of select="pubDate"/></div>
      <h2><xsl:value-of select="title"/></h2>
      <p><xsl:value-of select="description"/></p>
    </a>
  </xsl:for-each>
  <footer>Landing Coin (LANDING) · Solana Mainnet · RSS 2.0</footer>
</div>
</body>
</html>
</xsl:template>
</xsl:stylesheet>