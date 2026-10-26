"""
Transparency.

Built as an inspection pass: a scanner tracks scroll down the page and each
section is a different instrument reading on the same subject. Only the data
is carried over from the project's earlier dashboard; the presentation is
new, and every reading declares its own confidence rather than filling a gap
with an estimate.
"""

from sections import hero, band, cta, panels
from chrome import MINT, SOLSCAN_TOKEN

WORKER = ('https://landing-lander-registry.michelescalini.workers.dev'
          '/api/transparency')

# ---------------------------------------------------------------- data ------

FACTS = [
    ('Network',          'Solana Mainnet', 'SOL',  'Mainnet beta, no sidechain'),
    ('Maximum supply',   None,             '404M', 'Fixed at deployment'),
    ('Decimals',         '6',              '6',    'Smallest unit 0.000001'),
    ('Mint authority',   'Disabled',       'OFF',  'No further tokens can exist'),
    ('Freeze authority', 'Disabled',       'OFF',  'No account can be frozen'),
]

# The third field in each row below is the key the project's own site.js
# writes the live figure to: it looks up [data-reading="<key>"] and sets its
# text. Those keys are the contract with the data layer. Rename one here and
# that reading silently stays at its placeholder forever, so they are spelled
# exactly as site.js spells them, including the two camelCase vault keys.
OWNERS = [
    ('Positive owners',        'Addresses holding a non-zero balance',                          'positive'),
    ('Independent holders',    'Excludes project, pool, founder-controlled and known exchange addresses', 'independent'),
    ('Project wallets',        'The four identified addresses listed in section 04',            'project'),
    ('Liquidity pools',        'Pool accounts, counted separately from holders',               'pool'),
    ('Founder controlled',     'Held under founder control, not distributed',                  'founder'),
    ('Other known / exchange', 'Operational and exchange addresses the backend can identify',  'other'),
]

ALLOC = [
    ('Community',         '202,000,000', '50%',      50.0,    'seg-1'),
    ('Treasury',          '141,400,000', '35%',      35.0,    'seg-2'),
    ('Liquidity reserve', '39,000,000',  '9.6535%',   9.6535, 'seg-3'),
    ('Creator',           '20,200,000',  '5%',        5.0,    'seg-4'),
    ('Initial liquidity', '≈1,400,000',  '≈0.3465%',  0.3465, 'seg-5'),
]

WALLETS = [
    ('Community',         'CBPwvUZrDQThyM6a54shKPpywvpTyYQQ2Ng7FWPZPM88',
     'Project controlled. The label says what it is set aside for, not who holds it today.'),
    ('Treasury',          '3JA9uuNqr5tqBxGP9sQTRTPtwmPAR2KxmJyXyietrQwS',
     'Project controlled. Operating reserve.'),
    ('Liquidity reserve', '34hUkC1XVGMHX64txhfTh7rDBMhtScK8cpCcP54u17vZ',
     'Project controlled. Held against future pool depth.'),
    ('Creator',           '4fUtkW2LEZxLt2tgPJ9BitViNBqR3AUy58hyG81Q41hg',
     'Project controlled. Creator allocation.'),
]

POOL = [
    ('Pool vault / LANDING', 'Token side of the pool', 'landingVault'),
    ('Pool vault / SOL',     'SOL side of the pool',   'solVault'),
]

MARKET = [
    ('Price / USD',      'Last traded price reported by the market source', 'price'),
    ('Liquidity / USD',  'Pool depth in dollar terms',                      'liquidity'),
    ('24h volume / USD', 'Traded value over the rolling day',               'volume'),
    ('24h transactions', 'Swap count over the rolling day',                 'transactions'),
    ('24h buys',         'Buy-side swaps',                                  'buys'),
    ('24h sells',        'Sell-side swaps',                                 'sells'),
]

# ------------------------------------------------------------- helpers ------

WAVE = ('M0 13 C 20 3, 40 23, 60 13 S 100 3, 120 13 '
        'S 160 23, 180 13 S 220 3, 240 13')
FLAT = 'M0 13 H240'


def _trace(shape):
    d = WAVE if shape == 'wave' else FLAT
    return (f'<svg class="trace" viewBox="0 0 240 26" preserveAspectRatio="none" '
            f'aria-hidden="true">'
            f'<path class="base" d="{d}"/><path class="pulse" d="{d}"/></svg>')


def _channel(label, note, reading, state='awaiting', value='Awaiting source',
             shape='wave'):
    return f'''<div class="channel" data-state="{state}">
<span class="channel-label">{label}</span>
{_trace(shape)}
<span class="channel-value" data-reading="{reading}">{value}</span>
<span class="channel-note">{note}</span>
</div>'''


def _console(title, rows, status=None, status_id=None, retry_id=None,
             box_id=None):
    extra = ''
    if status:
        sid = f' id="{status_id}" role="status"' if status_id else ''
        extra += (f'<span class="bsep cbar-sep" aria-hidden="true"></span>'
                  f'<span{sid}>{status}</span>')
    if retry_id:
        # site.js disables this button while a request is in flight and
        # binds its click without checking it exists, so on this page it
        # is required, not optional: without it the loader throws.
        extra += (f'<span class="bsep cbar-sep" aria-hidden="true"></span>'
                  f'<button type="button" class="vbtn" id="{retry_id}" '
                  f'style="min-height:30px;padding:0 12px;font-size:11px">'
                  f'Refresh <span aria-hidden="true">&#8635;</span></button>')
    bid = f' id="{box_id}"' if box_id else ''
    return f'''<div class="console rise"{bid}>
<div class="console-bar">
<span class="pip" aria-hidden="true"></span><span>{title}</span>{extra}
</div>
{''.join(rows)}
</div>'''


# -------------------------------------------------------------- sections ----

def _facts_cluster():
    cards = []
    for i, (label, value, core, foot) in enumerate(FACTS):
        if value is None:
            val = '<span class="odo" style="--to-count:404"></span>,000,000'
        elif value == 'Disabled':
            val = '<span class="lamp"><i></i>Disabled</span>'
        else:
            val = value
        lo, hi = i * 7, 55 + i * 7
        cards.append(f'''<article class="gauge" style="animation-range:entry {lo}% entry {hi}%">
<div class="gauge-ring" aria-hidden="true">
<span class="gauge-dial" style="--to:360deg"></span>
<span class="gauge-core">{core}</span>
</div>
<span class="gauge-label">{label}</span>
<span class="gauge-value">{val}</span>
<span class="gauge-foot">{foot}</span>
</article>''')

    chars = ''.join(f'<span style="--i:{i}">{c}</span>'
                    for i, c in enumerate(MINT))

    return f'''<div class="cluster">{''.join(cards)}</div>
<div class="verify" style="--ac:var(--accent);margin-top:var(--space-6)">
<span class="verify-beam" aria-hidden="true"></span>
<div class="verify-body">
<div class="verify-top">
<span class="gauge-label">Official LANDING mint</span>
<span class="stamp"><span aria-hidden="true">&#10003;</span>Immutable</span>
</div>
<div class="verify-code">{chars}</div>
</div>
<div class="srcbar">
<button type="button" class="vbtn" data-copy="{MINT}">Copy address</button>
<a class="vbtn" href="{SOLSCAN_TOKEN}" target="_blank" rel="noopener">Verify on Solscan <span aria-hidden="true">&#8599;</span></a>
</div>
</div>'''


def _supply_stack():
    segs = ''.join(
        f'<div class="stack-seg" style="--share:{share};--seg-colour:var(--{tok});'
        f'animation-range:entry {i * 9}% entry {58 + i * 9}%" '
        f'title="{name} &mdash; {pct}"></div>'
        for i, (name, amt, pct, share, tok) in enumerate(reversed(ALLOC)))

    rows = ''.join(f'''<div class="alloc-row" style="--seg-colour:var(--{tok})">
<span class="alloc-key" aria-hidden="true"></span>
<span>{name}</span>
<span class="alloc-amt">{amt}</span>
<span class="alloc-share">{pct}</span>
</div>''' for name, amt, pct, share, tok in ALLOC)

    return f'''<div class="stack-wrap rise">
<div class="stack" role="img" aria-label="Original allocation of 404,000,000 LANDING across five lines">
<span class="stack-total">404,000,000</span>
{segs}
</div>
<div class="alloc-rows">{rows}</div>
</div>'''


def _wallet_nodes():
    nodes = ''.join(f'''<article class="node">
<div class="node-id">
<span class="gauge-label">{name} / project controlled</span>
<div class="node-addr">{addr}</div>
</div>
<p class="gauge-foot" style="flex:1 1 240px;margin:0">{note}</p>
<div class="srcbar">
<button type="button" class="vbtn" data-copy="{addr}">Copy</button>
<a class="vbtn" href="https://solscan.io/account/{addr}" target="_blank" rel="noopener">Inspect <span aria-hidden="true">&#8599;</span></a>
</div>
</article>''' for name, addr, note in WALLETS)
    return f'<div class="nodes">{nodes}</div>'


def _liquidity():
    lock = '''<svg class="lock" width="64" height="72" viewBox="0 0 64 72" aria-hidden="true">
<g class="lock-shackle"><path d="M18 34 V22 a14 14 0 0 1 28 0 V28" fill="none" stroke="var(--accent)" stroke-width="4" stroke-linecap="round"/></g>
<rect x="10" y="34" width="44" height="32" rx="6" fill="none" stroke="var(--accent)" stroke-width="3"/>
<circle cx="32" cy="50" r="4" fill="var(--accent)"/>
</svg>'''

    rows = [_channel(l, n, k) for l, n, k in POOL]

    return f'''<div class="lockpanel rise">
{lock}
<div style="flex:1 1 360px">
<h3 class="gauge-value" style="margin:0 0 8px">Liquidity is not locked</h3>
<p class="gauge-foot" style="margin:0">We are saying it here rather than
letting you find out. The vault readings below describe what is in the pool
right now. They do not imply a lock, and they are not a guarantee the
liquidity will still be there later.</p>
</div>
</div>
<div style="margin-top:var(--space-6)">{_console('Pool vaults', rows)}</div>'''


# ------------------------------------------------------------------ page ----

TRANSPARENCY = {
    'route': '/transparency.html',
    'title': 'LANDING Transparency | Token Facts and On-Chain Sources',
    'description': 'Five fixed token facts, the original allocation, the '
                   'four project wallets and live readings that say so when '
                   'they fail. Nothing is estimated to fill a gap.',
    'priority': '0.9',
    'changefreq': 'daily',
    'css': ['transparency.css'],
    'body': ''.join([
        '<div class="scanrail" aria-hidden="true"></div>',
        '<span class="scanrail-pct" aria-hidden="true"></span>',

        hero(
            title='Every number here <mark>survives you checking it</mark>.',
            lede='Five things on this page are fixed forever and can be '
                 'checked without us. Everything else is a live reading from '
                 'a service that can fail, and when it fails it says so. '
                 'Nothing here is estimated to fill a gap.',
            chips=[('Transparency', False), ('Verify, do not trust', True)],
            crumbs=[('LANDING', '/'), ('Transparency', None)],
        ),

        band('01', 'Immutable', 'Set once, at deployment.',
             lede='These five values cannot be changed by us or by anyone '
                  'else. They are properties of the mint account, and the '
                  'link below reads them straight off the chain.',
             body=_facts_cluster()),

        band('02', 'Live', 'Who holds it, right now.',
             # #transparency-live is the gate: site.js runs none of its
             # loader unless an element with this id is on the page.
             body=_console(
                 'Owner classification',
                 [_channel(l, n, k) for l, n, k in OWNERS],
                 status='Connecting to data source',
                 status_id='snapshot-status',
                 retry_id='refresh-transparency',
                 box_id='transparency-live'),
             note_id='coverage-note',
             note='Readings refresh while this page is visible. They are not '
                  'a continuous chain feed, and the timestamp belongs to the '
                  'source snapshot rather than to the moment you are reading '
                  'it. A channel that cannot be reached stays labelled; it is '
                  'never filled with an estimate.'),

        band('03', 'At launch', 'How the supply was divided.',
             lede='This is the original allocation, not current balances. '
                  'Tokens have moved since launch, and the explorer links in '
                  'the next section are where you check where they are now.',
             body=_supply_stack()),

        band('04', 'Identified', 'The four wallets we control.',
             lede='Identified addresses, not balance statements. Each one '
                  'links to its full transfer history.',
             body=_wallet_nodes()),

        band('05', 'Unlocked', 'Liquidity, stated plainly.',
             body=_liquidity()),

        band('06', 'Third party', 'What the market source says.',
             body=_console(
                 'Third-party market source',
                 [_channel(l, n, k) for l, n, k in MARKET],
                 status='Waiting for the market source',
                 status_id='market-source'),
             note_id='market-state',
             note='A flat trace means the market source is not answering, '
                  'not that the figure is zero. Market data comes from a '
                  'different provider than the owner readings above, so one '
                  'can fail while the other works.'),

        band('07', 'Check it', "Don't take our word for it.",
             lede='Configuration is separate from live readings. Coverage '
                  'can be partial. Where a source is silent we leave the '
                  'field empty.',
             body=panels([
                 ('Chain', 'Solscan',
                  'Token configuration and account state, read directly from '
                  'the chain.', SOLSCAN_TOKEN),
                 ('Record', 'Deployment record',
                  'The mint, pool and project addresses as they were set at '
                  'launch.', '/tokenomics.html'),
                 ('Supply', 'Allocation table',
                  'The original allocation and what each line was set aside '
                  'for.', '/tokenomics.html'),
                 ('Raw', 'Backend readings',
                  'The read-only JSON this page requests, with its own '
                  'timestamps and coverage field.', WORKER),
             ])),

        cta('Found something wrong?',
            'Tell us publicly. A transparency page that quietly fixes its '
            'own mistakes is not a transparency page.',
            [('Email the project', 'mailto:contact@landingcoin.fun', True),
             ('Community channels', '/community.html', False)]),
    ]),
}
