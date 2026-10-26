"""About, Supply, Markets and the two buying routes."""

from sections import (hero, band, prose, p, h3, ul, panels, facts, cards,
                      steps, table, callout, cta, qa)
from chrome import MINT, SOLSCAN_TOKEN, POLONIEX, JUPITER

ICON_LOCK = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
             '<rect x="3" y="8" width="12" height="8" rx="2" stroke="var(--accent)" stroke-width="1.5"/>'
             '<path d="M6 8V5.5a3 3 0 016 0V8" stroke="var(--accent)" stroke-width="1.5"/></svg>')
ICON_EYE = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
            '<path d="M1 9s3-5 8-5 8 5 8 5-3 5-8 5-8-5-8-5z" stroke="var(--accent)" stroke-width="1.5"/>'
            '<circle cx="9" cy="9" r="2" stroke="var(--accent)" stroke-width="1.5"/></svg>')
ICON_FLAG = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
             '<path d="M4 16V3h9l-2 3 2 3H4" stroke="var(--accent)" stroke-width="1.5" '
             'stroke-linejoin="round"/></svg>')
ICON_CHAT = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
             '<path d="M2 4h14v9H7l-5 3V4z" stroke="var(--accent)" stroke-width="1.5" '
             'stroke-linejoin="round"/></svg>')
ICON_NO = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
           '<circle cx="9" cy="9" r="6.5" stroke="var(--accent)" stroke-width="1.5"/>'
           '<path d="M4.5 4.5l9 9" stroke="var(--accent)" stroke-width="1.5"/></svg>')
ICON_CHART = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
              '<path d="M2 15h14M5 12V7M9 12V3M13 12V9" stroke="var(--accent)" '
              'stroke-width="1.5" stroke-linecap="round"/></svg>')


# ============================================================== about =======

ABOUT = {
    'route': '/about.html',
    'title': 'About LANDING | The Memecoin That Admits What It Is',
    'description': 'LANDING is a Solana memecoin with no roadmap to riches, '
                   'no price targets and no rocket emojis. Here is what it '
                   'is, what we built, and what we will never tell you.',
    'priority': '0.9',
    'body': ''.join([
        hero(
            title='A memecoin that <mark>admits what it is</mark>.',
            lede='Most tokens open with a promise. This one opens with a '
                 'disclaimer, and then spends the rest of the site showing '
                 'you how to check whether we are lying.',
            chips=[('Independent on Solana', False), ('Mainnet live', True)],
            crumbs=[('LANDING', '/'), ('About', None)],
            actions=[('Check the facts', '/transparency.html', True),
                     ('Read the Flight Plan', '/flight-plan.html', False)],
        ),

        band('01', 'Premise', 'Everyone is going up. We went down.',
             lede='The joke is simple enough to explain in one sentence, and '
                  'we have never needed a second one.',
             body=prose(
                 p('Every token launch borrows the same picture. A rocket, a '
                   'moon, a chart going one way forever. It is a good picture '
                   'because it is a good feeling, and it is a terrible picture '
                   'because nobody has ever been asked what happens next.'),
                 p('LANDING takes the other half of the flight. The part where '
                   'you slow down, pick a spot, and put the thing on the '
                   'ground in one piece. It is less exciting and considerably '
                   'more honest, which is roughly the entire personality of '
                   'this project.'),
                 h3('That is not a strategy. It is a tone.'),
                 p('We are not claiming the metaphor makes the token safer. It '
                   'does not. What it does is set an expectation we can '
                   'actually meet: we will not tell you where the price is '
                   'going, because we do not know, and neither does anyone '
                   'else who is telling you.'),
             )),

        band('02', 'Built', 'Three things that are not a chart.',
             lede='A memecoin does not need software. We built some anyway, '
                  'because a community with something to do outlasts a '
                  'community with something to hope for.',
             body=panels([
                 ('For holders', 'The LANDING Wall',
                  'Everyone who has touched down, on one page. Not a '
                  'leaderboard by balance. A record of who showed up.',
                  '/wall.html'),
                 ('For the stubborn', 'Certified Lander',
                  'Swap through the Lander page for a permanent ID and a '
                  'card, and stop having the argument about whether you hold.',
                  '/lander/'),
                 ('For the sceptical', 'Transparency',
                  'Token facts, the original allocation, the four wallets we '
                  'control, and what the backend can and cannot currently see.',
                  '/transparency.html'),
             ])),

        band('03', 'Fixed', 'The parts nobody can change.',
             lede='Four properties were set when the token was deployed and '
                  'cannot be altered by us, by you, or by anyone who buys the '
                  'project tomorrow.',
             body=cards([
                 ('Max supply', '404,000,000', 'Fixed. No second printing.'),
                 ('Mint authority', 'Disabled', 'No new tokens can ever exist.'),
                 ('Freeze authority', 'Disabled', 'No wallet can be frozen.'),
                 ('Decimals', '6', 'Smallest unit is 0.000001 LANDING.'),
             ]),
             note='Those four values live on the Solana mint account, not on '
                  f'this website. <a href="{SOLSCAN_TOKEN}" target="_blank" '
                  'rel="noopener" style="color:var(--accent)">Read them '
                  'straight off the chain</a> and compare.'),

        band('04', 'Never', 'Things you will not hear from us.',
             lede='Written down so you can hold us to it, and so you know '
                  'something has gone wrong the day one of them appears.',
             body=facts([
                 (ICON_NO, 'A price target',
                  'We do not have one. Anybody quoting you a number for '
                  'LANDING made it up, including if they are standing next '
                  'to our logo while they do it.'),
                 (ICON_NO, 'A partnership that is actually a logo',
                  'If we announce something, it will be a thing that exists '
                  'and that you can use that day.'),
                 (ICON_NO, 'Guaranteed anything',
                  'Not returns, not listings, not liquidity. Liquidity is not '
                  'locked and we say so on every page that touches it.'),
                 (ICON_NO, 'Urgency',
                  'No countdowns, no last chance, no "few understand". If a '
                  'decision only works when it is rushed, it is not a good '
                  'decision.'),
             ])),

        band('05', 'Risk', 'The honest version.',
             body=callout([
                 '<b>LANDING is a speculative memecoin.</b> It has no '
                 'intrinsic value, no revenue, no claim on anything, and no '
                 'team obligation to buy it back. The realistic outcome for '
                 'most memecoins is that they go to near zero and stay there.',
                 'Liquidity is not locked. The project controls four wallets '
                 'holding a meaningful share of supply, all four are listed '
                 'by address on the Transparency page, and you can watch them '
                 'yourself. Do not put in money you need back.',
             ])),

        cta('Verify first. Decide after.',
            'Every number on this site points at a source you can open '
            'without our permission. Start there, not with us.',
            [('Open Transparency', '/transparency.html', True),
             ('See where it trades', '/markets.html', False)]),
    ]),
}


# ========================================================== tokenomics ======

ALLOC_ROWS = [
    [('Community', 'strong'), ('202,000,000', 'num'), ('50%', 'num'),
     ('Rewards, campaigns and whatever the community talks us into.', '')],
    [('Treasury', 'strong'), ('141,400,000', 'num'), ('35%', 'num'),
     ('Operating reserve. Listings, build costs, the boring bills.', '')],
    [('Liquidity reserve', 'strong'), ('39,000,000', 'num'), ('9.6535%', 'num'),
     ('Held back to deepen pools later if it is needed.', '')],
    [('Creator', 'strong'), ('20,200,000', 'num'), ('5%', 'num'),
     ('The creator allocation. Named, not hidden in the community line.', '')],
    [('Initial liquidity', 'strong'), ('≈1,400,000', 'num'), ('≈0.3465%', 'num'),
     ('What actually went into the pool at launch.', '')],
]

TOKENOMICS = {
    'route': '/tokenomics.html',
    'title': 'LANDING Supply &amp; Allocation | 404,000,000 Fixed',
    'description': 'The full LANDING supply breakdown: 404,000,000 fixed, '
                   'mint and freeze disabled, and where every allocation '
                   'line went at launch.',
    'priority': '0.9',
    'body': ''.join([
        hero(
            title='404,000,000. <mark>That is the whole number</mark>.',
            lede='Fixed at deployment, with the ability to make more switched '
                 'off permanently. Here is how it was divided, what each line '
                 'is for, and what the split does not tell you.',
            chips=[('Supply', False), ('Fixed forever', True)],
            crumbs=[('LANDING', '/'), ('Supply', None)],
            actions=[('Verify on Solscan', SOLSCAN_TOKEN, True),
                     ('Transparency dashboard', '/transparency.html', False)],
        ),

        band('01', 'Fixed', 'Why the number cannot move.',
             lede='Supply is a property of the mint account on Solana, not a '
                  'promise on a website. Two authorities control whether it '
                  'can change, and both were disabled.',
             body=facts([
                 (ICON_LOCK, 'Mint authority: disabled',
                  'Nobody can create another LANDING. Not us, not a future '
                  'owner of the project, not a compromised key. The ability '
                  'was given up, and giving it up is permanent.'),
                 (ICON_LOCK, 'Freeze authority: disabled',
                  'Nobody can freeze your token account. We cannot stop you '
                  'selling, and we could not do it to anyone else either.'),
                 (ICON_EYE, 'Both are public',
                  'You do not have to take this paragraph as evidence. Open '
                  'the mint on an explorer and read the two fields yourself.'),
             ])),

        band('02', 'Split', 'Where the supply went at launch.',
             lede='This is the original allocation. It is not a statement of '
                  'current balances, and tokens have moved since.',
             body=table(
                 ['Allocation', 'LANDING', 'Share', 'What it is for'],
                 ALLOC_ROWS,
                 caption='Original LANDING supply allocation'),
             note='The Community line is project controlled. Calling it '
                  '"community" describes what it is earmarked for, not who '
                  'holds it today. We would rather say that plainly here than '
                  'have you discover it on an explorer and assume we were '
                  'hiding it.'),

        band('03', 'Honest', 'What a supply table cannot tell you.',
             body=prose(
                 p('Allocation charts are the most over-trusted picture in '
                   'crypto. A tidy split says nothing about whether those '
                   'tokens are still sitting where the chart put them, and '
                   'nothing at all about what happens if a large holder '
                   'decides to leave.'),
                 h3('Three things worth knowing'),
                 ul([
                     'A large share of supply is project controlled. The four '
                     'wallets are listed by address, so you can watch them '
                     'rather than trust them.',
                     'Only a small slice went into the pool at launch. Thin '
                     'liquidity means the price moves hard in both '
                     'directions, and that is a structural fact, not a mood.',
                     'Liquidity is not locked. Nothing mechanically prevents '
                     'it being removed, which is exactly why we put that '
                     'sentence on every page that touches the subject.',
                 ]),
                 p('None of this is unusual for a memecoin. It is just '
                   'unusual to print it on the supply page.'),
             )),

        cta('Now go check it.',
            'The allocation above is only as good as the addresses behind it. '
            'All four are published, with explorer links.',
            [('Open Transparency', '/transparency.html', True),
             ('Read the FAQ', '/faq.html', False)]),
    ]),
}


# ============================================================= markets ======

MARKETS = {
    'route': '/markets.html',
    'title': 'Where to Buy LANDING | Markets and Routes',
    'description': 'LANDING trades on Poloniex, Jupiter and Orca. Compare '
                   'the routes, understand the trade-offs, and verify the '
                   'mint address before you buy anything.',
    'priority': '0.9',
    'body': ''.join([
        hero(
            title='Two ways in. <mark>One address that matters</mark>.',
            lede='You can buy LANDING on a centralised exchange or swap for '
                 'it from your own wallet. The routes behave differently and '
                 'the wrong one costs you money, so here is the comparison '
                 'before the buttons.',
            chips=[('Markets', False), ('Verify the mint', True)],
            crumbs=[('LANDING', '/'), ('Markets', None)],
            actions=[('Jupiter route', '/routes/jupiter.html', True),
                     ('Poloniex route', '/routes/poloniex.html', False)],
        ),

        band('01', 'Compare', 'Which route is yours.',
             lede='Neither one is better. They are better at different things, '
                  'and which fits depends on what you already have.',
             body=table(
                 ['', 'Poloniex', 'Jupiter / Orca'],
                 [
                     [('What it is', 'strong'), ('A centralised exchange', ''),
                      ('On-chain swap from your own wallet', '')],
                     [('You need', 'strong'), ('An account and a deposit', ''),
                      ('A Solana wallet and some SOL', '')],
                     [('Holds your keys', 'strong'), ('The exchange does', ''),
                      ('You do', '')],
                     [('Pair', 'strong'), ('LANDING / USDT', 'num'),
                      ('LANDING / SOL', 'num')],
                     [('Wrong-token risk', 'strong'),
                      ('Low. The listing is the listing.', ''),
                      ('Real. Anyone can make a lookalike token.', '')],
                     [('Best for', 'strong'), ('First purchase, no wallet yet', ''),
                      ('Anyone already on Solana', '')],
                 ],
                 caption='Comparison of the two routes to buy LANDING'),
             ),

        band('02', 'Addresses', 'The only mint that is LANDING.',
             lede='On a decentralised exchange the token you receive is '
                  'whatever address you pasted. Nothing stops someone '
                  'deploying a token called LANDING with our logo on it.',
             body=''.join([
                 f'''<div class="verify rise" style="--ac:var(--accent)">
<span class="verify-beam" aria-hidden="true"></span>
<div class="verify-body">
<div class="verify-top">
<span class="gauge-label">Official LANDING mint</span>
<span class="stamp"><span aria-hidden="true">&#10003;</span>Check every time</span>
</div>
<div class="verify-code">{MINT}</div>
</div>
<div class="srcbar">
<button type="button" class="vbtn" data-copy="{MINT}">Copy address</button>
<a class="vbtn" href="{SOLSCAN_TOKEN}" target="_blank" rel="noopener">Solscan <span aria-hidden="true">&#8599;</span></a>
</div>
</div>''',
                 callout([
                     'Paste the address into the swap yourself rather than '
                     'picking LANDING from a search result. A search list is '
                     'populated by whoever registered a name first, and that '
                     'is not a security check.',
                 ], mark='!'),
             ]),
             ),

        band('03', 'Expect', 'What thin liquidity actually feels like.',
             body=facts([
                 (ICON_CHART, 'Slippage is not a bug',
                  'A small pool means your own order moves the price. Buying '
                  'more does not get you a better average, it gets you a '
                  'worse one.'),
                 (ICON_CHART, 'The two venues will disagree',
                  'An exchange price and a pool price drift apart constantly. '
                  'Neither is the real one. They are two different markets.'),
                 (ICON_NO, 'Depth can change without notice',
                  'Liquidity is not locked. The pool you looked at this '
                  'morning is not guaranteed to be the same size tonight.'),
             ])),

        cta('Pick a route, read it properly.',
            'Both walkthroughs are written for someone who has not done this '
            'before, and both end with the same verification step.',
            [('Jupiter walkthrough', '/routes/jupiter.html', True),
             ('Poloniex walkthrough', '/routes/poloniex.html', False)]),
    ]),
}


# ============================================================= jupiter ======

JUPITER_PAGE = {
    'route': '/routes/jupiter.html',
    'title': 'Buy LANDING on Jupiter | Solana Wallet Walkthrough',
    'description': 'Step-by-step: swap SOL for LANDING on Jupiter from your '
                   'own Solana wallet, with the mint address to verify and '
                   'the mistakes to avoid.',
    'body': ''.join([
        hero(
            title='Swap for LANDING <mark>from your own wallet</mark>.',
            lede='Jupiter routes your swap across Solana liquidity, including '
                 'the Orca pool LANDING sits in. You keep your keys the whole '
                 'way through. It takes about four minutes.',
            chips=[('Route', False), ('On-chain', True)],
            crumbs=[('LANDING', '/'), ('Markets', '/markets.html'),
                    ('Jupiter', None)],
            actions=[('Open Jupiter', JUPITER, True),
                     ('Compare routes', '/markets.html', False)],
        ),

        band('01', 'Walkthrough', 'Four minutes, done carefully.',
             body=steps([
                 ('Get a Solana wallet', [
                     'Phantom and Solflare are the usual two. Install one, '
                     'write the recovery phrase on paper, and put the paper '
                     'somewhere that is not a photo on your phone.',
                     'Nobody from this project will ever ask you for that '
                     'phrase. There is no support process that needs it, and '
                     'anyone requesting it is stealing from you.',
                 ]),
                 ('Fund it with SOL', [
                     'You are swapping SOL for LANDING, and you also need a '
                     'small amount of SOL left over to pay network fees. '
                     'Leaving roughly 0.01 SOL spare is plenty.',
                     'Buy SOL on any exchange and withdraw it to your wallet '
                     'address, or use the wallet\'s own buy option.',
                 ]),
                 ('Open Jupiter and connect', [
                     f'Go to <a href="{JUPITER}" target="_blank" '
                     'rel="noopener">jup.ag</a> and connect your wallet. '
                     'Connecting lets the site read your balances. It does '
                     'not give it permission to move anything.',
                 ]),
                 ('Paste the mint address', [
                     'This is the step that matters. In the output field, '
                     'paste the LANDING mint address rather than searching '
                     'for the name. Anyone can deploy a token called LANDING.',
                     f'<span style="font-family:var(--font-mono);'
                     f'word-break:break-all;color:var(--accent)">{MINT}</span>',
                 ]),
                 ('Check slippage, then swap', [
                     'Jupiter will show you the expected output and the price '
                     'impact. If the impact looks severe, your order is large '
                     'relative to the pool. Splitting it into smaller swaps '
                     'usually costs you less.',
                     'Approve in your wallet. Solana confirms in seconds.',
                 ]),
                 ('Verify what you received', [
                     'Open your wallet and check the token you now hold has '
                     'the mint address above. If it does not, you bought '
                     'something else, and no amount of it is LANDING.',
                 ]),
             ])),

        band('02', 'Mistakes', 'The three that cost people money.',
             body=facts([
                 (ICON_NO, 'Picking the token from a search list',
                  'Token lists are populated by whoever registered the name. '
                  'Paste the address. Every time, including the fifth time.'),
                 (ICON_NO, 'Spending every last bit of SOL',
                  'Without a little SOL for fees your next transaction fails, '
                  'including the one where you try to sell.'),
                 (ICON_NO, 'Approving a transaction you did not read',
                  'Read what the wallet is asking before you approve it. That '
                  'habit is worth more than any advice on this page.'),
             ])),

        cta('Landed?',
            'Get a permanent Lander ID, or leave one line on the Wall. Both '
            'are optional and both are public.',
            [('Get certified', '/lander/', True),
             ('See the Wall', '/wall.html', False)]),
    ]),
}


# ============================================================ poloniex ======

POLONIEX_PAGE = {
    'route': '/routes/poloniex.html',
    'title': 'LANDING on Poloniex | LANDING/USDT Walkthrough',
    'description': 'How to buy LANDING on Poloniex against USDT, what an '
                   'exchange listing does and does not mean, and how to move '
                   'tokens to your own wallet afterwards.',
    'body': ''.join([
        hero(
            title='Buy LANDING <mark>without touching a wallet</mark>.',
            lede='Poloniex lists LANDING against USDT. If you have never used '
                 'a Solana wallet, this is the shorter path in, with one '
                 'trade-off you should understand before you take it.',
            chips=[('Route', False), ('LANDING / USDT', True)],
            crumbs=[('LANDING', '/'), ('Markets', '/markets.html'),
                    ('Poloniex', None)],
            actions=[('Open Poloniex', POLONIEX, True),
                     ('Compare routes', '/markets.html', False)],
        ),

        band('01', 'Walkthrough', 'From nothing to holding.',
             body=steps([
                 ('Create and verify an account', [
                     'Exchanges require identity verification. How long it '
                     'takes varies by country and by how busy they are, so '
                     'start it before you want to trade rather than after.',
                 ]),
                 ('Deposit USDT', [
                     'Send USDT from another exchange or buy it on Poloniex '
                     'directly. Make sure the network you withdraw on matches '
                     'the network the deposit address expects. Mismatched '
                     'networks are the most common way people lose a deposit.',
                 ]),
                 ('Find the LANDING / USDT market', [
                     'Search for LANDING in the markets list and open the '
                     'LANDING/USDT pair.',
                 ]),
                 ('Use a limit order', [
                     'A market order fills at whatever the book offers, which '
                     'on a thin market can be a long way from the price you '
                     'just looked at. A limit order sets the worst price you '
                     'will accept and waits.',
                     'Slower, occasionally unfilled, usually cheaper.',
                 ]),
                 ('Decide whether to withdraw', [
                     'Tokens on an exchange are held by the exchange. That is '
                     'convenient, and it means the balance is their record of '
                     'what you own rather than yours.',
                     'To hold LANDING yourself, withdraw to a Solana wallet '
                     'address. Send a small test amount first and confirm it '
                     'arrives before moving the rest.',
                 ]),
             ])),

        band('02', 'Context', 'What a listing does not mean.',
             lede='Exchange listings get read as endorsements. They are not '
                  'endorsements, and pretending otherwise would be the exact '
                  'behaviour this project exists to avoid.',
             body=facts([
                 (ICON_EYE, 'It is a venue, not a verdict',
                  'A listing means a market exists. It is not an exchange '
                  'telling you a token is sound, and it carries no opinion '
                  'about price.'),
                 (ICON_NO, 'It does not make the token less speculative',
                  'Every risk on the rest of this site applies identically to '
                  'tokens bought here.'),
                 (ICON_CHART, 'The price will differ from the pool',
                  'The exchange book and the on-chain pool are separate '
                  'markets and routinely disagree. Neither is the true price.'),
             ])),

        cta('Prefer to hold your own keys?',
            'The Jupiter route swaps from your own wallet and never asks you '
            'to verify your identity with anyone.',
            [('Jupiter walkthrough', '/routes/jupiter.html', True),
             ('Back to Markets', '/markets.html', False)]),
    ]),
}


# ============================================================= buy ==========

BUY = {
    'route': '/buy/',
    'title': 'Buy LANDING | Start Here',
    'description': 'The short version of how to buy LANDING, the mint address '
                   'to verify, and an honest note about what you are buying.',
    'priority': '0.9',
    'body': ''.join([
        hero(
            title='Read this bit first. <mark>Then buy if you still want to</mark>.',
            lede='We are not going to rush you. LANDING is a speculative '
                 'memecoin, most memecoins end up near zero, and nothing here '
                 'is an exception to that.',
            chips=[('Buy', False), ('Mainnet live', True)],
            crumbs=[('LANDING', '/'), ('Buy', None)],
            actions=[('Jupiter route', '/routes/jupiter.html', True),
                     ('Poloniex route', '/routes/poloniex.html', False)],
        ),

        band('01', 'Honest', 'What you are actually buying.',
             body=callout([
                 '<b>A memecoin is a bet on attention.</b> It has no revenue, '
                 'no assets and no claim on anything. If people stop caring, '
                 'the price goes to near zero and stays there. That is the '
                 'normal outcome, not the bad case.',
                 'Liquidity is not locked. Project wallets hold a meaningful '
                 'share of supply. Both facts are published with addresses so '
                 'you can check them rather than take our word for it.',
                 'Only put in what you are prepared to see go to zero.',
             ])),

        band('02', 'Verify', 'The address, before anything else.',
             body=f'''<div class="verify rise" style="--ac:var(--accent)">
<span class="verify-beam" aria-hidden="true"></span>
<div class="verify-body">
<div class="verify-top">
<span class="gauge-label">Official LANDING mint</span>
<span class="stamp"><span aria-hidden="true">&#10003;</span>Solana mainnet</span>
</div>
<div class="verify-code">{MINT}</div>
</div>
<div class="srcbar">
<button type="button" class="vbtn" data-copy="{MINT}">Copy address</button>
<a class="vbtn" href="{SOLSCAN_TOKEN}" target="_blank" rel="noopener">Verify on Solscan <span aria-hidden="true">&#8599;</span></a>
</div>
</div>''',
             note='If a site, a bot or a very friendly stranger gives you a '
                  'different address, it is not LANDING. There is no second '
                  'official contract, no migration and no new mint.'),

        band('03', 'Routes', 'Pick the one that fits.',
             body=panels([
                 ('No wallet yet', 'Poloniex',
                  'Create an account, deposit USDT, trade the LANDING/USDT '
                  'pair. The exchange holds the tokens unless you withdraw.',
                  '/routes/poloniex.html'),
                 ('Already on Solana', 'Jupiter',
                  'Swap SOL for LANDING from your own wallet in about four '
                  'minutes. You keep your keys throughout.',
                  '/routes/jupiter.html'),
                 ('Still deciding', 'Compare them',
                  'The side-by-side, including what each route costs you in '
                  'control, convenience and slippage.',
                  '/markets.html'),
             ])),

        band('04', 'After', 'Three things worth doing.',
             body=qa([
                 ('Confirm the mint address of what you received', [
                     'Open your wallet or the exchange and check the token '
                     'matches the address above. This takes ten seconds and '
                     'it is the only way to know you bought the right thing.',
                 ]),
                 ('Get certified', [
                     'A swap through the Certified Lander page gets your '
                     'wallet a permanent Lander ID and a card to download. '
                     'A purchase on an exchange or in another app does not '
                     'qualify through that page.',
                 ]),
                 ('Set your own exit before you need one', [
                     'Decide now what would make you sell. Writing it down '
                     'while you are calm is worth more than any chart you '
                     'will read later while you are not.',
                 ]),
             ], open_first=True)),

        cta('Landed.',
            'Put yourself on the Wall, or go and read exactly what the '
            'project controls before you do anything else.',
            [('Get certified', '/lander/', True),
             ('Transparency', '/transparency.html', False)]),
    ]),
}
