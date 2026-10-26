"""Flight Plan, Team, Media Kit, FAQ and News."""

from . import news_originals as originals
from sections import (hero, band, prose, p, h3, panels, facts, cards,
                      callout, cta, qa, faq_schema)
from chrome import SOCIAL, MINT, SOLSCAN_TOKEN, POLONIEX

ICON_CHECK = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
              '<path d="M3.5 9.5l3.5 3.5 7.5-8" stroke="var(--accent)" '
              'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_DOT = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
            '<circle cx="9" cy="9" r="5" stroke="var(--accent)" stroke-width="1.5"/>'
            '<circle cx="9" cy="9" r="1.8" fill="var(--accent)"/></svg>')
ICON_NO = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
           '<circle cx="9" cy="9" r="6.5" stroke="var(--accent)" stroke-width="1.5"/>'
           '<path d="M4.5 4.5l9 9" stroke="var(--accent)" stroke-width="1.5"/></svg>')
ICON_DOC = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
            '<path d="M4 2h7l3 3v11H4V2z" stroke="var(--accent)" stroke-width="1.5" '
            'stroke-linejoin="round"/><path d="M11 2v3h3" stroke="var(--accent)" '
            'stroke-width="1.5" stroke-linejoin="round"/></svg>')


# ========================================================= flight plan ======

# The five phases are the project's own, word for word: status, title,
# summary and every item. The project's QA (redesign/qa/audit-final.py)
# compares them against the original Flight Plan, so change the wording
# only together with that original. The layout around them is ours.
PHASES = [
    ('01', 'Completed', 'Touchdown',
     'The foundation exists on-chain and can be independently checked.',
     ['LANDING launched on Solana Mainnet',
      'Fixed supply of 404,000,000 LANDING',
      'Mint and freeze authorities permanently disabled',
      'Token allocations and project wallets published',
      'Orca liquidity pool activated and Jupiter routing available',
      'Website, documentation and official channels launched']),
    ('02', 'Advanced', 'Build the Runway',
     'Make LANDING easier to verify, discover and access without '
     'manufacturing activity.',
     ['Expand visibility across reputable trackers and wallets',
      'First centralized exchange listing announced: '
      f'<a href="{POLONIEX}" target="_blank" rel="noopener">LANDING/USDT on '
      'Poloniex</a>',
      'Keep token information and public documentation accurate',
      'Develop editorial, exchange and ecosystem visibility',
      'Continue evaluating future trading venues individually',
      'Grow without fake holders, wash trading or coordinated shilling']),
    ('03', 'In progress', 'Bring More Landers Aboard',
     'Turn attention into an active community rather than a temporary '
     'audience.',
     ['Telegram, Discord and Reddit community spaces established',
      'Develop recurring community content across official channels',
      'Encourage community-created memes, articles and videos',
      "Explore collaborations aligned with LANDING's identity",
      'Create ways for Landers to participate without becoming shillers',
      'Pursue larger opportunities only when organic traction supports '
      'them']),
    ('04', 'Direction', 'Beyond the Landing',
     "Use the project's reach and resources only when there is something "
     'real worth building.',
     ['Evaluate practical uses for the Community allocation',
      'Invite Landers to propose and shape future initiatives',
      'Define transparent criteria before resources are committed',
      'Support selected experiments connected to the blockchain world',
      'Document completed initiatives instead of announcing imaginary '
      'ones']),
    ('05', 'Long-term direction', 'The Lander Era',
     'The long-term direction of LANDING is not to create another crowd '
     'watching a price chart. It is to build a recognizable community with '
     'its own identity, culture and voice.',
     ['Lander identity, Lander Code and Certified Lander system established',
      'Grow recognition and adoption of the Lander identity',
      'Give active community members opportunities to contribute',
      'Develop initiatives shaped with the community',
      'Recognize genuine participation, creativity and long-term presence',
      'Turn LANDING from a token people hold into a culture people '
      'represent'],
     'A holder owns a token. A Lander belongs to something.',
     "You don't just hold LANDING.<br>You become a Lander."),
]


def _phase(num, status, title, lede, items, identity=None, closing=None):
    """
    One phase. The article carries exactly class="flight-phase" because the
    project's QA selects it by that attribute value, so the reveal class
    lives on the inner wrapper instead. The status is printed in capitals
    in the markup for the same reason, not just styled that way.
    """
    rows = ''.join(f'<li>{i}</li>' for i in items)
    ident = f'<p class="leg-identity">{identity}</p>\n' if identity else ''
    close = f'\n<p class="leg-closing">{closing}</p>' if closing else ''
    return f'''<article class="flight-phase">
<div class="rise">
<div class="leg-head">
<span class="leg-n">{num}</span>
<div>
<span class="leg-status status-pill">{status.upper()}</span>
<h2>{title}</h2>
</div>
</div>
{ident}<p class="leg-lede">{lede}</p>
<ul class="leg-list">{rows}</ul>{close}
</div>
</article>'''


FLIGHT_PLAN = {
    'route': '/flight-plan.html',
    'title': 'LANDING Flight Plan | Direction, Not Prophecy',
    'description': 'What LANDING has finished, what is active now and what '
                   'may come later. No dates, no guaranteed listings and no '
                   'invented utility.',
    'priority': '0.8',
    'body': ''.join([
        hero(
            title='A flight plan, <mark>not a prophecy</mark>.',
            lede='Most roadmaps are a wish list with quarters attached. This '
                 'one has no dates on it, because a date we made up would be '
                 'the first dishonest thing on this site.',
            chips=[('Flight Plan', False), ('Five phases', True)],
            crumbs=[('LANDING', '/'), ('Flight Plan', None)],
        ),

        band('01', 'Rules', 'How this page behaves.',
             body=facts([
                 (ICON_NO, 'No deadlines',
                  'We do not know when things will be done. Publishing a '
                  'guess as a commitment is how roadmaps become lies on a '
                  'schedule.'),
                 (ICON_CHECK, 'Status changes when the work exists',
                  'A phase moves because something shipped, not because '
                  'enough time passed or enough people asked.'),
                 (ICON_NO, 'No guaranteed listings',
                  'Exchange listings are decisions other companies make. We '
                  'can pursue them. We cannot promise them.'),
                 (ICON_NO, 'No invented utility',
                  'We are not going to bolt a fake use case onto a memecoin '
                  'to make it sound like infrastructure.'),
             ])),

        band('02', 'Phases', 'Where it actually is.',
             body='<div class="legs">' +
                  ''.join(_phase(*ph) for ph in PHASES) + '</div>'),

        band('03', 'Check', 'Hold us to the finished column.',
             lede='Everything marked done in phase one can be verified right '
                  'now, by you, without asking us anything.',
             body=panels([
                 ('Supply and authorities', 'On Solscan',
                  'The fixed supply and both disabled authorities are fields '
                  'on the mint account. Open it and read them.',
                  SOLSCAN_TOKEN),
                 ('Project wallets', 'On Transparency',
                  'All four addresses, published, each linked to its full '
                  'transfer history.', '/transparency.html'),
                 ('The Poloniex listing', 'On Poloniex',
                  'The LANDING/USDT market exists or it does not. One click '
                  'settles it.', POLONIEX),
             ])),

        cta('Nothing here is a promise.',
            'Go and check the parts that claim to be finished. That is the '
            'only part of a roadmap worth anything.',
            [('Open Transparency', '/transparency.html', True),
             ('Read the FAQ', '/faq.html', False)]),
    ]),
}


# ================================================================ team ======

TEAM = {
    'route': '/team.html',
    'title': 'The LANDING Team | Small, Named and Reachable',
    'description': 'LANDING is run by Michele Scalini, Founder &amp; Project '
                   'Operator, with Furqan on brand design and community. A '
                   'small independent project that says so rather than '
                   'inventing departments.',
    'priority': '0.7',
    'body': ''.join([
        hero(
            title='Small team. <mark>Said out loud</mark>.',
            lede='Plenty of projects this size present an org chart with six '
                 'departments and a head of ecosystem. This one is two people '
                 'and some tooling, and pretending otherwise would undercut '
                 'everything else on the site.',
            chips=[('Team', False), ('Independent', True)],
            crumbs=[('LANDING', '/'), ('Team', None)],
        ),

        band('01', 'Who', 'The ground crew.',
             body='''<div class="team-grid">
<article class="person rise">
<img class="person-photo" src="/assets/team/michele-scalini.jpg" width="640" height="640"
     alt="Michele Scalini" loading="lazy" decoding="async">
<div class="person-text">
<span class="panel-k">Project</span>
<h3>Michele Scalini</h3>
<span class="person-role">Founder &amp; Project Operator</span>
<p>Direction, public communication and the day-to-day running of LANDING.
Signing authority and custody of project wallets sit here and nowhere else.</p>
</div>
</article>

<article class="person rise">
<img class="person-photo" src="/assets/team/furqan.jpg" width="640" height="640"
     alt="Furqan" loading="lazy" decoding="async">
<div class="person-text">
<span class="panel-k">Brand &amp; Community</span>
<h3>Furqan</h3>
<span class="person-role">Brand Designer &amp; Senior Community Manager</span>
<p>Brand design and community for LANDING: the visual identity, the
channels where Landers meet, and how the project shows up in them. Has been
building brands and communities since 2019.</p>
</div>
</article>

<article class="person person-wide rise">
<img class="person-photo" src="/assets/team/nova.jpg" width="640" height="640"
     alt="Nova" loading="lazy" decoding="async">
<div class="person-text">
<span class="panel-k">Support</span>
<h3>Nova</h3>
<span class="person-role">Digital executive assistant</span>
<p>Research, documentation, coordination and communication workflows.
Nova holds no funds, no wallets, no private keys and no signing authority,
which is worth stating plainly rather than leaving you to assume either way.</p>
</div>
</article>
</div>'''),

        band('02', 'Later', 'Roles that do not exist yet.',
             lede='Listed as possibilities, not as staff. Nobody holds these '
                  'and nobody is about to be announced into one.',
             body=''.join([
                 '''<div class="chips2" style="margin-bottom:var(--space-6)">
<span class="chip2">Development &middot; planned</span>
<span class="chip2">Communications &middot; planned</span>
<span class="chip2">Partnerships &middot; planned</span>
</div>''',
                 callout([
                     'These are areas the project might expand into if it '
                     'grows enough to justify it. They are not current '
                     'departments, not open positions, and not people whose '
                     'names we are keeping back.',
                 ], mark='i'),
             ])),

        band('03', 'Contact', 'One line in.',
             lede='No ticketing system, no support tier, no form that goes '
                  'nowhere.',
             body=prose(
                 p('For anything that needs a record, including press, '
                   'exchanges, verification requests and complaints, email '
                   '<a href="mailto:contact@landingcoin.fun">'
                   'contact@landingcoin.fun</a>.'),
                 p('For everything else, the open channels are faster and '
                   'the answer is visible to everyone else who had the same '
                   'question.'),
                 h3('We will never contact you first'),
                 p('No direct message from this project will ever arrive '
                   'uninvited, and nobody here will ever ask for a recovery '
                   'phrase. If either happens, it is not us.'),
             )),

        cta('Prefer evidence to introductions?',
            'The Transparency page is the part of this project that does not '
            'require trusting anyone on this one.',
            [('Open Transparency', '/transparency.html', True),
             ('Community channels', '/community.html', False)]),
    ]),
}


# =========================================================== media kit ======

# ---- Media kit downloads ----------------------------------------------------
# The current LANDING logo and banner, as new files under assets/brand and
# assets/banners. Nothing the project already had is changed.

def _download(title, meta, thumb, w, h, href, filename, alt):
    return f'''<figure class="dl-card rise">
<div class="dl-thumb"><img src="{thumb}" width="{w}" height="{h}" alt="{alt}"
     loading="lazy" decoding="async"></div>
<figcaption><b>{title}</b><span>{meta}</span></figcaption>
<a class="vbtn" href="{href}" download="{filename}">Download <span aria-hidden="true">&#8595;</span></a>
</figure>'''


DOWNLOADS = '<div class="dl-grid dl-grid-2">' + ''.join([
    _download('Logo', 'PNG &middot; 2048 &times; 2048 &middot; 1.2 MB',
              '/assets/brand/landing-logo-preview.webp', 400, 400,
              '/assets/brand/landing-logo-2048.png', 'LANDING-logo.png',
              'LANDING Coin logo'),
    _download('Banner', 'PNG &middot; 1500 &times; 500 &middot; 392 KB',
              '/assets/banners/landing-banner-preview.webp', 760, 253,
              '/assets/banners/landing-banner-1500x500.png',
              'LANDING-banner-1500x500.png',
              'LANDING banner: Everyone is going to the moon. We are landing.'),
]) + '</div>'


MEDIA_KIT = {
    'route': '/media-kit.html',
    'title': 'LANDING Media Kit | Logos, Facts and Approved Language',
    'description': 'Official LANDING descriptions, token facts, brand assets '
                   'and verified links for journalists, exchanges and '
                   'creators. Copy-ready and checkable.',
    'priority': '0.7',
    'body': ''.join([
        hero(
            title='Everything you need, <mark>already checked</mark>.',
            lede='Descriptions you can paste, facts you can verify, and the '
                 'official links so nobody ends up citing an impersonator. '
                 'Take what you need without asking.',
            chips=[('Media Kit', False), ('Free to use', True)],
            crumbs=[('LANDING', '/'), ('Media Kit', None)],
        ),

        band('01', 'Copy', 'Descriptions, ready to paste.',
             body='''<div class="grid-2">
<div class="panel">
<span class="panel-k">Short &middot; 1 line</span>
<p style="font-size:var(--step-0);color:var(--text-2)">Landing Coin (LANDING)
is an independent Solana memecoin built on transparency, irony and
expectations that can actually be met.</p>
<button type="button" class="vbtn" data-copy="Landing Coin (LANDING) is an independent Solana memecoin built on transparency, irony and expectations that can actually be met.">Copy</button>
</div>

<div class="panel">
<span class="panel-k">Standard &middot; 1 paragraph</span>
<p style="font-size:var(--step-0);color:var(--text-2)">Everyone is going to
the moon. LANDING is going the other way. An independent Solana memecoin
with a fixed supply of 404,000,000, mint and freeze authorities permanently
disabled, and every project wallet published by address. It makes no price
claims and invents no utility story.</p>
<button type="button" class="vbtn" data-copy="Everyone is going to the moon. LANDING is going the other way. An independent Solana memecoin with a fixed supply of 404,000,000, mint and freeze authorities permanently disabled, and every project wallet published by address. It makes no price claims and invents no utility story.">Copy</button>
</div>
</div>'''),

        band('02', 'Assets', 'Logo and banner.',
             lede='The official files, free to use when you write about or '
                  'list LANDING. Download them here rather than saving a copy '
                  'from somewhere else.',
             body=DOWNLOADS),

        band('03', 'Facts', 'The numbers, with their source.',
             body=cards([
                 ('Network', 'Solana Mainnet', 'Mainnet beta. No sidechain.'),
                 ('Max supply', '404,000,000', 'Fixed at deployment.'),
                 ('Decimals', '6', 'Smallest unit 0.000001.'),
                 ('Mint and freeze', 'Disabled', 'Both given up permanently.'),
                 ('Liquidity lock', 'Not locked', 'Stated, not buried.'),
             ]),
             note=f'Please link the mint address rather than retyping it: '
                  f'<a href="{SOLSCAN_TOKEN}" target="_blank" rel="noopener" '
                  f'style="color:var(--accent)">verify on Solscan</a>.'),

        band('04', 'Mint', 'The address, for citation.',
             body=f'''<div class="verify rise" style="--ac:var(--accent)">
<span class="verify-beam" aria-hidden="true"></span>
<div class="verify-body">
<div class="verify-top">
<span class="gauge-label">Official LANDING mint</span>
<span class="stamp"><span aria-hidden="true">&#10003;</span>Only one</span>
</div>
<div class="verify-code">{MINT}</div>
</div>
<div class="srcbar">
<button type="button" class="vbtn" data-copy="{MINT}">Copy address</button>
<a class="vbtn" href="{SOLSCAN_TOKEN}" target="_blank" rel="noopener">Solscan <span aria-hidden="true">&#8599;</span></a>
</div>
</div>'''),

        band('05', 'Voice', 'Lines you can quote.',
             lede='These are the project\'s own, and they are the only '
                  'slogans attached to it.',
             body='''<div class="quotes">
<blockquote class="quote rise">Everyone is going to the moon. We are landing.</blockquote>
<blockquote class="quote rise">No moon. No promises. Just landing.</blockquote>
<blockquote class="quote rise">Gravity still works.</blockquote>
</div>''',
             note='There is no approved language about price, returns, '
                  'partnerships or future listings, because there is nothing '
                  'true we could say about any of them.'),

        band('06', 'Links', 'Official, and nothing else.',
             lede='If a source is not on this list, it is not us. This '
                  'matters more than usual for a project with an '
                  'impersonation problem.',
             body=panels([
                 ('Site', 'landingcoin.fun', 'The public project site.', '/'),
                 ('Data', 'Transparency', 'Token facts, wallets and readings '
                  'with their source labelled.', '/transparency.html'),
                 ('Chain', 'Token on Solscan', 'Verify the mint and '
                  'configuration independently.', SOLSCAN_TOKEN),
                 ('Social', 'X', 'Announcements and the jokes.', SOCIAL['X']),
                 ('Social', 'Discord', 'The main community room.', SOCIAL['Discord']),
                 ('Formal', 'LinkedIn', 'The company page.', SOCIAL['LinkedIn']),
             ])),

        cta('Writing about LANDING?',
            'Check the facts first. We would rather be covered accurately '
            'than covered kindly.',
            [('Open Transparency', '/transparency.html', True),
             ('Email the project', 'mailto:contact@landingcoin.fun', False)]),
    ]),
}


# ================================================================= faq ======

FAQ_ROWS = [
    ('Is LANDING going to go up?', [
        'We do not know, and anyone who tells you they do is guessing or '
        'selling. LANDING is a speculative memecoin with no revenue and no '
        'assets behind it. The realistic outcome for most memecoins is that '
        'they end up near zero.',
        'That sentence appears on several pages of this site on purpose.',
    ]),
    ('Does LANDING promise any returns?', [
        'No. There is no price target and no promised return. Buying '
        'LANDING gives you no claim on profits, products or any outcome, '
        'and you can lose what you spend.',
    ]),
    ('Is the liquidity locked?', [
        'No. It is not locked, and we say so on every page that touches the '
        'subject rather than leaving you to find out.',
        'Nothing mechanically prevents liquidity being removed. The project '
        'wallets are published by address so you can watch them instead of '
        'trusting a sentence about them.',
    ]),
    ('What is the official mint address?', [
        f'{MINT}, on Solana mainnet. Check it before you buy anywhere. A '
        'token with the same name and a different address is not LANDING.',
    ]),
    ('How do I buy LANDING?', [
        'Two ways. Swap through Jupiter from your own Solana wallet, or '
        'trade LANDING/USDT on Poloniex. Either way, check the mint '
        'address, the quote and the fees before you approve anything.',
    ]),
    ('Can more LANDING ever be created?', [
        'No. The mint authority was disabled at deployment, which is '
        'permanent and cannot be undone by us or by anyone who takes over '
        'the project later. Supply is fixed at 404,000,000 forever.',
        'This is a field on the mint account, not a claim on a website. Open '
        'the token on an explorer and read it yourself.',
    ]),
    ('Can my wallet be frozen?', [
        'No. The freeze authority was also disabled. Nobody, including us, '
        'can stop you moving or selling your tokens.',
    ]),
    ('How much of the supply does the project hold?', [
        'A meaningful share. The Community, Treasury, Liquidity reserve and '
        'Creator allocations are all project controlled, and all four '
        'addresses are published on the Transparency page with explorer '
        'links.',
        'The Community allocation being called community describes what it '
        'is set aside for, not who holds it today. We would rather say that '
        'here than have you discover it and assume we hid it.',
    ]),
    ('Why is the market data sometimes blank?', [
        'Because the third-party market source is not answering. When that '
        'happens the dashboard shows the field as unavailable instead of '
        'filling it with the last number it saw.',
        'A stale figure presented as live is worse than no figure. Unavailable '
        'means unavailable, and it is never an estimate.',
    ]),
    ('What is the LANDING Wall?', [
        'A public message wall on Solana. A mark is one line of up to 140 '
        'characters and costs 5,000 LANDING plus the network fee. Reading '
        'the Wall is free and needs no wallet.',
    ]),
    ('Is the Certified Lander card an NFT?', [
        'No. It is not a token, not tradeable, and not a claim on anything. '
        'It is a permanent Lander ID and a card you can download, issued '
        'after an eligible swap through the Certified Lander page.',
        'Anyone offering to buy your card is running a different operation.',
    ]),
    ('Does connecting my wallet put my funds at risk?', [
        'Connecting lets a site read public balances. Nothing moves until '
        'you approve a transaction in your own wallet: 5,000 LANDING for a '
        'mark on the Wall, or the swap you choose on the Lander page.',
        'Nothing on this site will ever ask you to approve a token '
        'allowance, and nobody from this project will ever ask for a '
        'recovery phrase. There is no support process that needs one.',
    ]),
    ('Is there a second contract, a v2 or a migration?', [
        'No. There is one mint address, it is printed on several pages here, '
        'and it will not change.',
        'Any announcement of a new contract is an impersonation attempt, '
        'however convincing the account looks.',
    ]),
    ('Who is behind the project?', [
        'Michele Scalini, who founded LANDING and operates it, with Furqan '
        'on brand design and community. The Team page says so plainly '
        'rather than listing departments that do not exist.',
    ]),
    ('Why is the supply 404,000,000?', [
        'Because 404 is the error code for something that was not found, '
        'which seemed like the right number for a token whose whole position '
        'is that the moon is not there.',
        'That is the entire reason. There is no tokenomics model behind it '
        'and we are not going to invent one.',
    ]),
    ('Do I need LANDING to join the community?', [
        'No. You do not need any tokens to join the Discord, which is the '
        'main community hub. Every official channel is listed on the '
        'Community page.',
    ]),
    ('How do I report an impersonator?', [
        'Email contact@landingcoin.fun, or post it in the open channels so '
        'other people see it too. Scam accounts work by catching the people '
        'who have not heard yet, so speed matters more than process.',
    ]),
]

FAQ = {
    'route': '/faq.html',
    'title': 'LANDING FAQ | The Questions We Keep Getting',
    'description': 'Straight answers on supply, liquidity, project wallets, '
                   'wallet safety and why the market data sometimes shows '
                   'nothing at all.',
    'priority': '0.8',
    'jsonld': faq_schema(FAQ_ROWS),
    'body': ''.join([
        hero(
            title='Straight answers, <mark>including the bad ones</mark>.',
            lede='These are the questions that actually get asked, answered '
                 'the way we would answer them in the Discord rather than the '
                 'way a disclaimer would.',
            chips=[('FAQ', False), ('No hedging', True)],
            crumbs=[('LANDING', '/'), ('FAQ', None)],
        ),

        band('01', 'Answers', 'The list.',
             body=qa(FAQ_ROWS, one_paragraph=True)),

        band('02', 'Missing', 'Not here?',
             body=prose(
                 p('Ask in the open channels, where the answer is visible to '
                   'everyone else who was about to ask the same thing. If it '
                   'needs a record, email '
                   '<a href="mailto:contact@landingcoin.fun">'
                   'contact@landingcoin.fun</a>.'),
                 p('Questions that get asked more than a few times end up on '
                   'this page.'),
             )),

        cta('Still sceptical?',
            'Good. The Transparency page is built for exactly that, and it '
            'does not require believing a word of this one.',
            [('Open Transparency', '/transparency.html', True),
             ('Community channels', '/community.html', False)]),
    ]),
}


# ================================================================ news ======

# The essay sits under /news/ with the rest of the writing. It is
# deliberately NOT at /why-landing-doesnt-promise-the-moon.html: the project
# already retired that URL and folds it into /about.html, and its QA asserts
# that redirect still exists. Publishing a page there would overwrite the
# redirect and fail the check. The old URL keeps going to About.
ARTICLE_SLUG = '/news/the-argument-behind-the-joke.html'


def _article(route, title, description, kicker, heading, standfirst,
             published, read, body, ldtitle=None):
    """
    One write-up. The date is the one the project published it on, and it
    is carried in the markup as well as in the structured data so the two
    can never disagree.
    """
    nice = {'09': 'September', '10': 'October'}[published[5:7]]
    shown = f'{int(published[8:10])} {nice} {published[:4]}'

    return {
        'route': route,
        'title': title,
        'description': description,
        'og_type': 'article',
        'priority': '0.6',
        'changefreq': 'yearly',
        'jsonld': {
            '@context': 'https://schema.org',
            '@type': 'NewsArticle',
            '@id': f'https://landingcoin.fun{route}#article',
            'headline': ldtitle or heading,
            'description': description,
            'datePublished': published,
            'inLanguage': 'en',
            'author': {'@type': 'Organization', 'name': 'Landing Coin'},
            'publisher': {'@type': 'Organization', 'name': 'Landing Coin'},
            'mainEntityOfPage': f'https://landingcoin.fun{route}',
        },
        'body': ''.join([
            hero(
                title=heading,
                lede=standfirst,
                crumbs=[('LANDING', '/'), ('News', '/news/'), (kicker, None)],
                chips=[(kicker, False), (shown, True)],
            ),
            band('01', 'Record', title.split(' | ')[0] + '.',
                 body=f'''<div class="art rise">
<div class="art-meta">
<span>{kicker}</span><span>&middot;</span>
<time datetime="{published}">{shown}</time><span>&middot;</span>
<span>{read} minute read</span>
</div>
{body}
</div>'''),
            cta('Check it rather than take it from us.',
                'Every claim in this post points at something you can open '
                'yourself.',
                [('Open Transparency', '/transparency.html', True),
                 ('Back to News', '/news/', False)]),
        ]),
    }

NEWS_INDEX = {
    'route': '/news/',
    'title': 'LANDING News | Updates and Write-ups',
    'description': 'Project updates and longer write-ups from LANDING. '
                   'Published when something happened, not on a schedule.',
    'priority': '0.7',
    'body': ''.join([
        hero(
            title='Published when <mark>something happened</mark>.',
            lede='Not weekly, not on a content calendar. If this page is '
                 'quiet it means there was nothing worth your time, which is '
                 'a perfectly good state for a project to be in.',
            chips=[('News', False), ('Irregular', True)],
            crumbs=[('LANDING', '/'), ('News', None)],
        ),

        band('01', 'Latest', 'Write-ups.',
             body=panels([
                 ('Community &middot; 7 Oct 2026', 'The Discord is open',
                  'A room with more than one table in it, for the '
                  'conversations the fast channels keep burying.',
                  '/news/landing-coin-discord-community.html'),
                 ('Project &middot; 25 Sep 2026', 'The Wall is live',
                  'One of these exists and you can use it today. The '
                  'merchandise store is an idea, and is described as one.',
                  '/news/landing-wall-and-future-merch-store.html'),
                 ('Markets &middot; 21 Sep 2026', 'LANDING is on Poloniex',
                  'A second route to the token. The same fixed supply, and '
                  'the same refusal to tell you where the price is going.',
                  '/news/landing-coin-poloniex-listing.html'),
                 ('Essay', 'Why LANDING does not promise the moon',
                  'The argument behind the joke, and why a project that '
                  'promises nothing is harder to run than one that promises '
                  'everything.', ARTICLE_SLUG),
             ], cols=2)),

        band('02', 'Elsewhere', 'Where updates land first.',
             lede='Anything significant goes out in the channels before it '
                  'becomes a write-up here.',
             body=panels([
                 ('Day to day', 'Discord', 'Announcements land here first.',
                  SOCIAL['Discord']),
                 ('Public', 'X', 'The short version, and the jokes.', SOCIAL['X']),
                 ('Longer', 'Reddit', 'Where the arguments happen.', SOCIAL['Reddit']),
             ])),

        cta('Prefer data to writing?',
            'The Transparency dashboard updates itself and never needs a '
            'blog post to explain what changed.',
            [('Open Transparency', '/transparency.html', True),
             ('Read the Flight Plan', '/flight-plan.html', False)]),
    ]),
}


ARTICLE = {
    'route': ARTICLE_SLUG,
    'title': 'Why LANDING Does Not Promise the Moon',
    'description': 'The argument behind the joke: why a memecoin that '
                   'promises nothing is harder to run, and why we think it '
                   'is the only honest version.',
    'og_type': 'article',
    'priority': '0.6',
    # Left out of sitemap.xml on purpose. The project's QA requires the
    # sitemap to list exactly its core pages and its three news posts. The
    # page stays public and indexable, and News links to it.
    'sitemap': False,
    'body': ''.join([
        hero(
            title='Why we do not <mark>promise the moon</mark>.',
            lede='Every memecoin makes the same promise. Here is what happens '
                 'when you refuse to make it.',
            crumbs=[('LANDING', '/'), ('News', '/news/'), ('Essay', None)],
            chips=[('Essay', False), ('Project note', True)],
        ),

        band('01', 'Essay', 'The argument behind the joke.',
             body='''<div class="art rise">
<div class="art-meta">
<span>Project note</span><span>&middot;</span><span>6 minute read</span>
</div>

<p>The rocket is the most efficient piece of marketing in crypto. It
compresses an entire argument into one image: this goes up, you should be
on it, and anyone asking questions is going to miss out. It works because
it skips the part where somebody has to explain why.</p>

<p>We went the other way, and not because we are more virtuous. We went the
other way because the rocket has a problem nobody talks about. It sets an
expectation that the project cannot meet, and then the project has to spend
the rest of its life managing the gap.</p>

<h2>Promises create a debt</h2>

<p>The moment you tell people a token is going up, you have borrowed
against a future you do not control. Every week it does not happen, you owe
an explanation. Most projects pay that debt with more promises, which is
how a community goes from excited to exhausted in about two months.</p>

<p>A project that promised nothing has no debt. When the price falls, and
it will, there is no broken commitment to account for. The only thing we
ever claimed is that the supply is fixed and the authorities are off, and
those two things are as true on a bad day as a good one.</p>

<blockquote>It is easier to keep a promise you never made.</blockquote>

<h2>This is harder, not easier</h2>

<p>Refusing to promise anything removes the easiest tool available. You
cannot run a campaign on momentum you are not allowed to claim. You cannot
answer "why should I buy this" with a number. Every piece of writing has to
earn attention on something other than greed, which is a considerably
smaller lever.</p>

<p>What you get in return is a community that arrived for a reason that
still exists next month. People who came for a price target leave when the
price target does. People who came because the project was straight with
them tend to stay, and they are better company.</p>

<h2>What honesty actually costs</h2>

<p>Saying liquidity is not locked costs us holders. We know. There is a
version of this site where that sentence is in a footer in grey text, and
that version converts better.</p>

<p>We put it in the body copy of every page that touches the subject,
because the alternative is that someone finds out later and is right to be
angry. A project that only tells you the good parts has told you something
about itself, and it is not the thing it meant to tell you.</p>

<h2>The joke is the thesis</h2>

<p>Everyone is going to the moon. We are landing. It reads as a gag, and it
is one, but it is also the whole operating principle. Landing is the part
of the flight where you admit gravity exists, pick somewhere realistic, and
accept that the exciting phase is over.</p>

<p>Most tokens never do that. They stay in launch posture until the fuel
runs out, and then they go quiet. We would rather start from the ground and
be judged on what is actually built on it.</p>

<p>Which means the only fair way to read this project is to check it. Not
to believe this essay. <a href="/transparency.html">The facts are
published</a>, the four wallets are named, and the numbers we cannot
currently fetch are labelled as missing instead of filled in. Go and
disagree with the evidence.</p>
</div>'''),

        cta('Check the claims.',
            'This essay is an opinion. The Transparency page is not.',
            [('Open Transparency', '/transparency.html', True),
             ('Back to News', '/news/', False)]),
    ]),
}

# ---- The three published write-ups -----------------------------------------
# The headline and standfirst are ours. The article itself is the project's
# original text, word for word, from news_originals.py. See that file for why.

POLONIEX_NEWS = _article(
    route='/news/landing-coin-poloniex-listing.html',
    title='LANDING Listed on Poloniex | LANDING/USDT',
    description='Published 21 September 2026. LANDING/USDT spot trading '
                'opened on Poloniex at 12:00 UTC. What the listing changes, '
                'and the much longer list of what it does not.',
    kicker='Markets', published='2026-09-21', read='2',
    heading='LANDING is <mark>on Poloniex</mark>.',
    standfirst='A second place to buy it. The same token, the same fixed '
               'supply, and the same refusal to tell you where the price '
               'is going.',
    body=f'<article class="article-prose">{originals.POLONIEX}</article>')


WALL_NEWS = _article(
    route='/news/landing-wall-and-future-merch-store.html',
    title='The LANDING Wall Is Live | And a Store That Is Not',
    description='Published 25 September 2026. The LANDING Wall is live on '
                'Solana at 5,000 LANDING per post. A merchandise store is a '
                'maybe, and is described as one.',
    kicker='Project', published='2026-09-25', read='4',
    heading='The Wall is live. <mark>The shop is not</mark>.',
    standfirst='One of these exists and you can use it today. The other is '
               'an idea, and we would rather say so than put it on a '
               'roadmap and let it harden into a promise.',
    body=f'<article class="article-prose">{originals.WALL}</article>')


DISCORD_NEWS = _article(
    route='/news/landing-coin-discord-community.html',
    title='The LANDING Discord Is Open | Community',
    description='Published 7 October 2026. A Discord server joins the '
                'existing LANDING channels, with room for topics that a '
                'fast-moving chat buries.',
    kicker='Community', published='2026-10-07', read='2',
    heading='The Discord is <mark>open</mark>.',
    standfirst='Not a replacement for anything. A room with more than one '
               'table in it, for the conversations the fast channels keep '
               'burying.',
    body=f'<article class="article-prose">{originals.DISCORD}</article>')
