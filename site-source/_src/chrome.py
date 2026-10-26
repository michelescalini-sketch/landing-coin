"""
Shared site chrome.

One definition of the navigation, used by every page. The header keeps the
four top-level items the home page uses; everything else hangs off them in
drop panels, so an eighteen-page site still presents a four-item nav.
"""

# ---------------------------------------------------------------- links -----

SOCIAL = {
    'Discord':  'https://discord.gg/UEGNHe9UG',
    'Telegram': 'https://t.me/LandingCoinCommunity',
    'Reddit':   'https://www.reddit.com/r/LandingCoin/',
    'X':        'https://x.com/LandingCoin2026',
    'LinkedIn': 'https://www.linkedin.com/company/146683351',
}

POLONIEX = 'https://www.poloniex.com/trade/LANDING_USDT'
JUPITER = 'https://jup.ag/'
MINT = 'DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ'
SOLSCAN_TOKEN = f'https://solscan.io/token/{MINT}'

# Each top-level item, and the routes that sit under it. The second field of
# a row is the one-line gloss shown under the link in the drop panel.
NAV = [
    ('About', '/about.html', [
        ('/about.html',      'About',          'What this is, plainly'),
        ('/flight-plan.html', 'Flight Plan',   'What is built and what is next'),
        ('/team.html',       'Team',           'Who is behind it'),
        ('/news/',           'News',           'Updates and write-ups'),
    ]),
    ('Token', '/tokenomics.html', [
        ('/tokenomics.html',  'Supply',        'Allocation and what it is for'),
        ('/transparency.html', 'Transparency', 'Facts you can check yourself'),
        ('/markets.html',     'Markets',       'Where LANDING trades'),
        None,
        ('/routes/jupiter.html',  'Jupiter route',  'Swap from a Solana wallet'),
        ('/routes/poloniex.html', 'Poloniex route', 'Buy on an exchange'),
    ]),
    ('Landers', '/lander/', [
        ('/lander/',    'Certified Lander', 'One permanent ID per wallet'),
        ('/wall.html',      'The LANDING Wall', 'Everyone who touched down'),
        ('/media-kit.html', 'Media Kit',        'Logos, colours and rules'),
    ]),
    ('Community', '/community.html', [
        ('/community.html', 'Community', 'Where everyone actually is'),
        ('/faq.html',       'FAQ',       'The questions we keep getting'),
    ]),
]

FOOTER = [
    ('The project', [
        ('/about.html', 'About'),
        ('/flight-plan.html', 'Flight Plan'),
        ('/team.html', 'Team'),
        ('/news/', 'News'),
        ('/faq.html', 'FAQ'),
    ]),
    ('Token', [
        ('/buy/', 'Buy LANDING'),
        ('/markets.html', 'Markets'),
        ('/tokenomics.html', 'Supply'),
        ('/transparency.html', 'Transparency'),
        ('/routes/jupiter.html', 'Jupiter route'),
        ('/routes/poloniex.html', 'Poloniex route'),
    ]),
    ('Explore', [
        ('/lander/', 'Certified Lander'),
        ('/wall.html', 'The LANDING Wall'),
        ('/community.html', 'Community'),
        ('/media-kit.html', 'Media Kit'),
    ]),
    ('Elsewhere', [
        (SOCIAL['Discord'], 'Discord'),
        (SOCIAL['Telegram'], 'Telegram'),
        (SOCIAL['Reddit'], 'Reddit'),
        (SOCIAL['X'], 'X'),
        (SOCIAL['LinkedIn'], 'LinkedIn'),
    ]),
    ('Legal', [
        ('/privacy.html', 'Privacy'),
        ('/cookie-policy.html', 'Cookie policy'),
        ('/terms-of-service.html', 'Terms of service'),
    ]),
]

LOGO_SVG = (
    '<svg class="lpad" width="42" height="36" viewBox="0 0 42 36" aria-hidden="true">'
    '<ellipse class="lp-r" cx="21" cy="29" rx="15" ry="3.6" fill="none" '
    'stroke="var(--accent)" stroke-width="1.6"/>'
    '<path d="M3 29 H39" stroke="var(--text)" stroke-width="2.4" stroke-linecap="round"/>'
    '<path d="M9 33 H33" stroke="var(--text)" stroke-width="1.4" stroke-linecap="round" opacity=".35"/>'
    '<circle class="lp-d hdr-pad-dot" cx="21" cy="22" r="5" fill="var(--accent)"/></svg>'
)

CARET = ('<svg class="hdr-caret" viewBox="0 0 10 6" fill="none" aria-hidden="true">'
         '<path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def _ext(url):
    """External links open in a new tab and say so to assistive tech."""
    return ' target="_blank" rel="noopener"' if url.startswith('http') else ''


def _owns(group, route):
    """True when the current route lives under this top-level item."""
    return any(r and r[0] == route for r in group)


def header(route='/'):
    items = []
    for label, top, group in NAV:
        rows = []
        for r in group:
            if r is None:
                rows.append('<hr>')
                continue
            href, name, gloss = r
            cur = ' aria-current="page"' if href == route else ''
            rows.append(
                f'<a href="{href}"{cur}><b>{name}</b><span>{gloss}</span></a>')

        current = ' data-current' if _owns(group, route) else ''
        panel_id = f'nav-{label.lower()}'
        items.append(f'''<div class="hdr-item"{current}>
<button type="button" class="hdr-link" aria-expanded="false" aria-controls="{panel_id}">{label}{CARET}</button>
<div class="hdr-panel" id="{panel_id}">{''.join(rows)}</div>
</div>''')

    home = ' aria-current="page"' if route == '/' else ''
    return f'''<header class="hdr">
<div class="hdr-bar">
<a class="hdr-logo" href="/"{home}>{LOGO_SVG}<span>LANDING</span></a>
<nav class="hdr-nav" aria-label="Main">
{''.join(items)}
<a class="hdr-cta" href="/buy/">Buy token</a>
</nav>
<button type="button" class="hdr-burger" data-drawer-toggle aria-expanded="false" aria-controls="drawer" aria-label="Open menu">
<span></span><span></span><span></span>
</button>
</div>
</header>
{drawer(route)}'''


def drawer(route='/'):
    groups = []
    i = 0
    for label, top, group in NAV:
        rows = []
        for r in group:
            if r is None:
                continue
            href, name, _ = r
            cur = ' aria-current="page"' if href == route else ''
            rows.append(f'<a href="{href}" style="--i:{i}"{cur}>{name}</a>')
            i += 1
        groups.append(
            f'<div class="drawer-group"><h2>{label}</h2>{"".join(rows)}</div>')

    socials = ''.join(
        f'<a href="{u}" style="--i:{i + n}" target="_blank" rel="noopener">{n_}</a>'
        for n, (n_, u) in enumerate(SOCIAL.items()))

    return f'''<div class="drawer" id="drawer">
{''.join(groups)}
<div class="drawer-group"><h2>Elsewhere</h2>{socials}</div>
<a class="drawer-cta" href="/buy/">Buy token</a>
</div>'''


def footer(route='/'):
    cols = []
    for title, rows in FOOTER:
        links = ''.join(
            f'<li><a href="{href}"{_ext(href)}'
            f'{" aria-current=\"page\"" if href == route else ""}>{name}</a></li>'
            for href, name in rows)
        cols.append(f'<div class="ftr-col"><h2>{title}</h2><ul>{links}</ul></div>')

    return f'''<footer class="ftr">
<div class="page-wrap">
<div class="ftr-top">
<div class="ftr-mark">
<span class="hdr-logo">{LOGO_SVG}<span>LANDING</span></span>
<p>Gravity still works. No moon, no promises, no rocket emojis. Just a
token you can check and a community that can take a joke.</p>
<p><a href="mailto:contact@landingcoin.fun">contact@landingcoin.fun</a></p>
</div>
<div class="ftr-links">{''.join(cols)}</div>
</div>
<p class="ftr-risk">LANDING is a speculative memecoin with no intrinsic
value and no team promising you a return. You can lose everything you put
in. Nothing on this site is financial advice, and liquidity is not locked.</p>
<div class="ftr-base">
<span>&#169; 2026 Landing Coin &#183; Independent &#183; Solana Mainnet</span>
<span>Built to be checked, not believed</span>
</div>
</div>
</footer>'''
