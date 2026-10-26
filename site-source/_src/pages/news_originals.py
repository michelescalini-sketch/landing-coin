"""
The three news articles, word for word as the project published them.

These bodies are not rewritten on purpose. The project's own QA
(redesign/qa/audit-final.py) compares the text of each one against its
original and fails the build if a single word differs, so treat them as
quoted material: restyle them in CSS, never edit them here.

One addition: the copy button in the Poloniex article also carries
data-copy, which is the attribute ui.js listens for. Its label and text
are unchanged.
"""

DISCORD = r'''<div class="article-body">
<p><strong>The official LANDING Coin Discord community is now open.</strong></p>
<p>Discord gives LANDING another place to bring project information and community conversations together without replacing the channels that already exist. Telegram remains useful for fast discussion, Reddit for longer-form posts, and Bitcointalk for the project's public ANN history. Discord adds a more structured environment where topics can live in their own spaces.</p>
<div class="cta">
  <h2>Join the LANDING Discord</h2>
  <p>Enter the official server, explore the channels and meet other Landers.</p>
  <a class="button" href="https://discord.gg/UEGNHe9UG" target="_blank" rel="noopener">Join LANDING on Discord</a>
</div>
<h2>Why add Discord?</h2>
<p>LANDING has gradually expanded beyond a token page and a trading pair. The project now includes the LANDING Wall, the Certified Lander experience, public transparency pages, news and several community channels. As that grows, a single fast-moving chat is not always the best place for every kind of conversation.</p>
<p>Discord makes it easier to separate project information, general discussion and future community activities while keeping everything under the same LANDING identity.</p>
<h2>A community space, not an activity counter</h2>
<p>The goal is not to create dozens of empty channels or manufacture the appearance of a busy community. The server is designed to give LANDING a useful structure and then allow participation to grow naturally.</p>
<p>That follows the same principle used elsewhere in the project: build something real first, make it public when it is ready, and avoid pretending that a bigger number automatically means a stronger community.</p>
<h2>LANDING's official community channels</h2>
<p>The project can now be followed and discussed through several official spaces:</p>
<ul>
  <li><a href="https://discord.gg/UEGNHe9UG" target="_blank" rel="noopener"><strong>Discord</strong></a> — structured community discussions and project spaces;</li>
  <li><a href="https://t.me/LandingCoinCommunity" target="_blank" rel="noopener"><strong>Telegram</strong></a> — fast community conversation and updates;</li>
  <li><a href="https://www.reddit.com/r/LandingCoin/" target="_blank" rel="noopener"><strong>Reddit</strong></a> — posts, discussions and longer-form community content;</li>
  <li><a href="https://bitcointalk.org/index.php?topic=5591610.0" target="_blank" rel="noopener"><strong>Bitcointalk</strong></a> — the public LANDING announcement thread.</li>
</ul>
<p>Official project links are also maintained in the <a href="/media-kit.html">LANDING Media Kit</a> and on the main website.</p>
<h2>Come for the meme. Stay for the conversation.</h2>
<p>No LANDING tokens are required to join the server. Holding the token is not a membership requirement, and joining Discord does not imply any financial benefit or promised reward.</p>
<p>It is simply another place to follow the project, talk with the community and see what LANDING builds next.</p>
<p><strong>No moon. No promises. Just landing.</strong></p>
<p class="risk">Risk notice: LANDING is a memecoin and remains speculative. Community participation does not represent a promise of financial value, returns or future performance. Always verify official LANDING links and the token mint address before interacting with third-party services.</p>
</div>'''

WALL = r'''<div class="article-body">
<p><strong>The LANDING Wall is now live.</strong> It is a simple community feature built around the LANDING token: users can leave a public post-it style message on the wall after making the required LANDING payment on Solana.</p>

<p>That may sound deliberately modest. It is. LANDING was never built around a promise of revolutionary utility. The project has consistently avoided inventing features merely to make a memecoin look more important than it is. Instead, the goal is to test small uses that are understandable, transparent and actually connected to the community.</p>

<h2>What is the LANDING Wall?</h2>

<p>The <a href="/wall.html">LANDING Wall</a> is a public community space on the official LANDING Coin website. A post costs <strong>5,000 LANDING</strong>, and the payment is verified through Solana before the message is accepted.</p>

<p>The result is intentionally simple: one payment, one public message, one small mark left behind. The Wall does not claim to create financial value or transform LANDING into a utility token in the regulatory or technical sense. It is simply a token-powered community interaction.</p>

<p>For LANDING, that distinction matters. A feature should exist because people can actually use it, not because a roadmap needs another impressive-looking bullet point.</p>

<div class="cta">
  <h2>Visit the LANDING Wall</h2>
  <p>Read the messages already posted or leave your own mark using LANDING on Solana.</p>
  <a class="button" href="/wall.html">Open the LANDING Wall</a>
</div>

<h2>Why experiment with LANDING token utility?</h2>

<p>Memecoins are usually valued for culture, community and market attention rather than traditional product utility. LANDING does not pretend otherwise. But that does not mean the token has to remain disconnected from everything the community does.</p>

<p>The Wall explores a narrower idea: <strong>using LANDING as a participation layer inside the LANDING ecosystem.</strong></p>

<p>That approach can include experiences where the token has an obvious role:</p>

<ul>
  <li>community interactions such as the LANDING Wall;</li>
  <li>identity features such as the <a href="/lander/">Lander</a> concept and verified community cards;</li>
  <li>future physical merchandise connected to LANDING's visual identity;</li>
  <li>other small features where paying or holding LANDING has a clear purpose.</li>
</ul>

<p>The principle remains the same: build something first, explain exactly what it does, and avoid assigning imaginary value to it.</p>

<h2>Next idea: a LANDING merchandise store</h2>

<p>One of the concepts currently being explored is an official <strong>LANDING merchandise store</strong>. The idea is to turn parts of the project's identity — the LANDING coin, the Lander character, the anti-moon language and the visual style of the project — into physical products.</p>

<p>Potential items include small collectibles and branded products such as keychains, apparel, accessories and other LANDING-themed gadgets. A print-on-demand model is being considered so products can be produced after an order instead of requiring the project to maintain large physical inventory.</p>

<p>The more interesting part is the payment flow. The long-term objective is to evaluate whether customers could place an order using <strong>LANDING tokens</strong>, while the backend handles the conversion required to pay the fulfillment provider in conventional currency.</p>

<div class="future">
  <strong>Important:</strong> the merchandise store and LANDING payment flow are still future project concepts. They are not live today, and technical, commercial and compliance details still need to be completed before any launch is announced.
</div>

<h2>From speculation to participation</h2>

<p>LANDING remains a speculative memecoin. A Wall, a community card or a future merchandise store does not change that fact.</p>

<p>What these features can change is the relationship between the token and the community around it. Instead of LANDING existing only as an asset that moves between wallets and markets, it can also become a way to participate in small parts of the project's culture.</p>

<p>That is a much narrower claim than the word “utility” often carries in crypto, and deliberately so.</p>

<p>The project does not need to claim that LANDING powers a financial revolution. It is enough for LANDING to power things that make sense inside LANDING.</p>

<h2>Building utility without changing the identity</h2>

<p>Any future feature will continue to follow the same communication principles used elsewhere on the project:</p>

<ul>
  <li>no guaranteed returns;</li>
  <li>no invented demand;</li>
  <li>no fake partnerships;</li>
  <li>no utility announced before it actually exists;</li>
  <li>clear separation between live features and future plans.</li>
</ul>

<p>The <a href="/transparency.html">LANDING Transparency page</a> will continue to document verifiable token and market information, while the <a href="/news/">LANDING News</a> section will publish future developments when they become concrete.</p>

<p>For now, the Wall is live. The store is an idea being developed. That is exactly how LANDING intends to communicate progress: <strong>what exists, what is being explored, and nothing in between disguised as certainty.</strong></p>

<p><strong>Everyone is going to the moon. We are finding things to do after landing.</strong></p>

<p class="risk">Risk notice: LANDING is a memecoin and remains speculative. Community features and future merchandise concepts do not represent a promise of financial value, returns or future performance. Cryptocurrency transactions involve risk. Always verify the official LANDING mint address and use official project links.</p>
</div>'''

POLONIEX = r'''<div class="article-body">
<p><strong>LANDING Coin has reached a new milestone: LANDING is listed on Poloniex.</strong> The LANDING/USDT spot market is scheduled to open on September 21, 2026 at 12:00 UTC.</p>

<p>For a project built around a deliberately simple idea — <em>“Everyone is going to the moon. We are landing.”</em> — the Poloniex listing adds a new way for users to access and trade LANDING while the project continues to operate on Solana.</p>

<h2>LANDING/USDT on Poloniex</h2>
<p>The listing introduces a centralized LANDING/USDT market on Poloniex alongside LANDING's existing on-chain presence and Solana liquidity.</p>
<p>The official LANDING mint address remains:</p>
<code class="contract">DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ</code>
<button type="button" class="inline-copy" data-copy-value="DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ" aria-label="Copy address" data-copy="DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ">Copy</button><p>Users should always verify the official mint address before interacting with LANDING or any third-party platform claiming to support the token.</p>

<h2>What the Poloniex listing changes</h2>
<p>Until now, LANDING's market activity has primarily developed through the Solana ecosystem. The addition of a centralized exchange gives traders another access point, with LANDING quoted directly against USDT.</p>
<p>The listing does not change LANDING's fixed token supply of <strong>404,000,000 LANDING</strong>. Mint authority and freeze authority remain disabled.</p>
<p>It also does not change the project's communication policy. LANDING does not promise returns, predetermined price targets or guaranteed outcomes. Developments are announced when they actually happen.</p>

<h2>A milestone, not a destination</h2>
<p>The Poloniex listing is an important step for LANDING, but it is not presented as an end point. The project will continue to develop its community, transparency tools, market infrastructure and public documentation while monitoring what happens after centralized trading begins.</p>
<p>Future exchange updates, project milestones and market-related announcements will be published in the official <a href="/news/">LANDING News</a> section.</p>

<div class="cta">
  <h2>LANDING/USDT on Poloniex</h2>
  <p>Use the official Poloniex market page for the LANDING/USDT trading pair.</p>
  <a class="button" href="https://www.poloniex.com/trade/LANDING_USDT" target="_blank" rel="noopener">Open LANDING/USDT on Poloniex</a>
</div>

<p><strong>No moon. No promises. Just LANDING.</strong></p>

<p class="risk">Risk notice: LANDING is a memecoin. Cryptocurrency trading involves substantial risk and can result in loss of capital. Nothing on this page is financial advice or a guarantee of future performance. Always conduct your own research.</p>
</div>'''

