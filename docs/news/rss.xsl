<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom">
<xsl:output method="html" encoding="UTF-8"/>
<xsl:template match="/">
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LANDING Coin News — RSS Feed</title>
  <style>
    *{box-sizing:border-box}
    body{margin:0;background:radial-gradient(circle at 85% 12%,rgba(122,58,237,.20),transparent 32%),radial-gradient(circle at 8% 20%,rgba(0,210,190,.14),transparent 28%),linear-gradient(145deg,#02040a,#080b16 45%,#080511);color:#f7f7f8;font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;min-height:100vh}
    a{color:inherit;text-decoration:none}
    .wrap{width:min(920px,calc(100% - 32px));margin:0 auto;padding:30px 0 70px}
    .top{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:12px 0 34px}
    .brand{display:flex;align-items:center;gap:12px;font-weight:950}.brand img{width:48px;height:48px;border-radius:50%}.home{padding:10px 14px;border:1px solid rgba(255,255,255,.12);border-radius:10px;color:#c4cad5}
    .hero{padding:42px 0}.eyebrow{color:#ffb33a;font-size:.72rem;font-weight:900;letter-spacing:.14em;text-transform:uppercase}.hero h1{margin:14px 0 18px;font-size:clamp(2.8rem,7vw,5.4rem);line-height:.95;letter-spacing:-.06em}.hero p{max-width:720px;margin:0;color:#9aa3b5;line-height:1.7}
    .note{margin:0 0 30px;padding:18px 20px;border:1px solid rgba(255,173,36,.22);border-radius:16px;background:rgba(255,173,36,.05);color:#cfd6e2;line-height:1.6}
    .item{display:block;margin:16px 0;padding:26px;border:1px solid rgba(255,255,255,.10);border-radius:22px;background:linear-gradient(145deg,rgba(18,25,42,.84),rgba(7,10,18,.82))}
    .item:hover{border-color:rgba(34,230,199,.28)}.item h2{margin:0 0 10px;font-size:1.55rem;letter-spacing:-.035em}.item .date{color:#22e6c7;font-size:.76rem;font-weight:850;margin-bottom:12px}.item p{margin:0;color:#9aa3b5;line-height:1.7}
    footer{margin-top:45px;padding-top:25px;border-top:1px solid rgba(255,255,255,.10);color:#697386;font-size:.82rem}
  </style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <a class="brand" href="/"><img src="/landing-logo.jpg" alt="Landing Coin logo"/>LANDING COIN</a>
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