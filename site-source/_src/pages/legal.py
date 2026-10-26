"""Privacy, cookies, terms and the 404 page."""

from sections import hero, band, prose, p, h3, ul, callout, cta, panels

UPDATED = '26 October 2026'


def _legal_hero(title, lede, crumb):
    return hero(
        title=title,
        lede=lede,
        chips=[('Legal / CURRENT POLICY', False), (f'Updated {UPDATED}', True)],
        crumbs=[('LANDING', '/'), (crumb, None)],
        scene=True,
    )


# ============================================================= privacy ======

PRIVACY = {
    'route': '/privacy.html',
    'title': 'Privacy Policy | LANDING',
    'description': 'What LANDING collects, what it does not, and what '
                   'happens to a wallet address when you use the Wall or '
                   'Certified Lander.',
    'priority': '0.3',
    'changefreq': 'yearly',
    'body': ''.join([
        _legal_hero(
            'What we <mark>do not collect</mark>.',
            'Short, because there is not much. No accounts, no passwords, '
            'no advertising profile and nothing sold to anybody.',
            'Privacy'),

        band('01', 'Short version', 'In one paragraph.',
             body=callout([
                 'We do not ask for your name, email or password to browse '
                 'this site. If you use the Wall or Certified Lander you '
                 'provide a public Solana wallet address and, optionally, a '
                 'display name and a message, and those are published '
                 'because publishing them is the entire point of the '
                 'feature. We do not sell data and we do not run advertising '
                 'trackers.',
             ], mark='i')),

        band('02', 'Detail', 'What is actually processed.',
             body=prose(
                 h3('Browsing'),
                 p('The site is static. Our hosting provider records standard '
                   'server information such as the request, the time and a '
                   'truncated network address, which is how any web server '
                   'works and is used for availability and abuse prevention '
                   'rather than profiling.'),

                 h3('Wallet addresses'),
                 p('A Solana wallet address is already public information on '
                   'a public blockchain. When you connect a wallet to leave '
                   'a mark, or ask the registry for a Lander card, that '
                   'address and its LANDING balance are read and may be '
                   'shown alongside your mark or on your Certified Lander '
                   'card. Wallet addresses are not necessarily anonymous.'),
                 p('You approve every transaction in your own wallet. A '
                   'mark on the Wall is a payment of 5,000 LANDING with the '
                   'message attached. A Lander card follows a swap you make '
                   'through Jupiter. Neither asks for a token spending '
                   'allowance.'),
                 p('The Lander registry keeps the ID, the wallet address, '
                   'the qualifying transaction and the balance recorded at '
                   'issue. Anyone who enters a wallet address can look its '
                   'record up, without proving they own that wallet.'),

                 h3('What you type'),
                 p('A display name and a message on the Wall are published '
                   'publicly and are intended to be. Do not put anything in '
                   'them you would not want permanently associated with your '
                   'wallet address.'),

                 h3('Local storage'),
                 p('Only the Certified Lander page stores anything in your '
                   'browser, and only two entries: your public wallet '
                   'address once a card is confirmed or restored '
                   '(<strong>landing:lander-wallet</strong>), so the page can '
                   'show the same card on your next visit, and the '
                   'transaction signature of a swap while the registry checks '
                   'it (<strong>landing:pending-signature</strong>). Neither '
                   'is a cookie. The '
                   '<a href="/cookie-policy.html">cookie and local storage '
                   'policy</a> explains both in full.'),

                 h3('Third parties'),
                 p('Some pages link to block explorers, exchanges and social '
                   'platforms. Once you follow a link you are on their site '
                   'under their policy, and we have no control over or '
                   'visibility into what they collect.'),
                 p('The Wall and Certified Lander pages load code from '
                   'Jupiter and from public code libraries (jsDelivr and '
                   'esm.sh), and the Transparency, Wall and Lander pages read '
                   'from the project\'s own registry service. Those services '
                   'see each request, as any web server does. The Jupiter '
                   'swap window and your wallet app are run by their '
                   'providers and may keep their own data under their own '
                   'policies.'),

                 h3('Removal'),
                 p('To have a mark or a Certified Lander record removed, '
                   'email <a href="mailto:contact@landingcoin.fun">'
                   'contact@landingcoin.fun</a> from a channel you can '
                   'demonstrate control of, or ask in the public channels. '
                   'On-chain activity cannot be removed by anyone, including '
                   'us, because that is what a public blockchain is.'),
             )),

        band('03', 'Changes', 'If this changes.',
             body=prose(
                 p(f'This page was last updated on {UPDATED}. Material '
                   'changes will be noted in the public channels rather than '
                   'quietly edited in.'),
             )),

        cta('Questions about any of this?',
            'Email the project directly. It goes to a person.',
            [('contact@landingcoin.fun', 'mailto:contact@landingcoin.fun', True),
             ('Read the Terms', '/terms-of-service.html', False)]),
    ]),
}


# ============================================================== cookies =====

COOKIES = {
    'route': '/cookie-policy.html',
    'title': 'Cookie &amp; Local Storage Policy | LANDING',
    'description': 'LANDING sets no cookies. The only things stored in '
                   'your browser are two entries the Certified Lander page '
                   'uses to find your card again.',
    'priority': '0.3',
    'changefreq': 'yearly',
    'body': ''.join([
        _legal_hero(
            'Two entries. <mark>No trackers</mark>.',
            'There is no cookie banner on this site because there is nothing '
            'to consent to. Here is the full list of what gets stored, and '
            'why.',
            'Cookies'),

        band('01', 'The list', 'Everything stored in your browser.',
             body=prose(
                 p('LANDING sets no cookies. Only the Certified Lander page '
                   'keeps anything, in your browser\'s local storage, and '
                   'only these two entries.'),
                 h3('Your Lander wallet'),
                 p('Stored under <strong>landing:lander-wallet</strong> once '
                   'the registry confirms or restores your Certified Lander '
                   'card. It holds your public Solana wallet address, so the '
                   'next time you open the Lander page it can look up and '
                   'show the same card.'),
                 h3('A swap being checked'),
                 p('Stored under <strong>landing:pending-signature</strong> '
                   'after you swap through Jupiter on the Lander page, while '
                   'the registry checks that the swap was finalized on '
                   'Solana. It holds the transaction signature. It is deleted '
                   'as soon as the registry confirms or rejects the swap. If '
                   'the check runs out of time, it stays so the page can try '
                   'again on your next visit.'),
                 p('Both are public on-chain values rather than personal '
                   'identifiers. They are only ever sent to the project\'s '
                   'own registry, to look up or confirm your card, and no '
                   'other site can read them.'),

                 h3('That is the complete list'),
                 ul([
                     'No cookies of any kind',
                     'No analytics or advertising trackers',
                     'No session identifiers or logins, because there are no '
                     'accounts',
                     'No third-party tag managers',
                 ]),
                 p('The Jupiter swap window and your wallet app are run by '
                   'their providers and may keep their own data under their '
                   'own policies.'),
             )),

        band('02', 'Control', 'Removing it.',
             body=prose(
                 p('Clearing site data for landingcoin.fun in your browser '
                   'removes both entries. Nothing is lost: the Lander page '
                   'simply will not remember your card, and you can restore '
                   'it any time with your wallet address.'),
                 p('Blocking local storage does not break the rest of the '
                   'site. The Lander page still works; it just cannot '
                   'remember your card between visits.'),
             )),

        cta('Read the rest.',
            'The privacy policy covers wallet addresses and anything you '
            'post publicly.',
            [('Privacy policy', '/privacy.html', True),
             ('Terms of service', '/terms-of-service.html', False)]),
    ]),
}


# ================================================================ terms =====

TERMS = {
    'route': '/terms-of-service.html',
    'title': 'Terms of Service | LANDING',
    'description': 'The terms covering use of the LANDING site and features, '
                   'and a plain statement of what LANDING is not.',
    'priority': '0.3',
    'changefreq': 'yearly',
    'body': ''.join([
        _legal_hero(
            'The terms, <mark>in readable English</mark>.',
            'Written to be understood rather than to be impenetrable. The '
            'important part is the first section and it is not hidden.',
            'Terms'),

        band('01', 'The important part', 'What LANDING is not.',
             body=callout([
                 '<b>LANDING is a speculative memecoin with no intrinsic '
                 'value.</b> It is not an investment, not a security, not a '
                 'share in anything, and carries no claim on any asset, '
                 'revenue or person.',
                 'Nothing on this site is financial, legal or tax advice. No '
                 'statement here is a prediction or guarantee of value. '
                 'Liquidity is not locked and project wallets hold a '
                 'meaningful share of supply, both of which are published '
                 'rather than buried.',
                 'You can lose the entire amount you spend. Do not spend '
                 'money you need.',
             ], mark='!')),

        band('02', 'Using the site', 'What you agree to.',
             body=prose(
                 p('By using this site you accept these terms. If you do not '
                   'accept them, the remedy is simply not to use it.'),
                 h3('You are responsible for your own wallet'),
                 p('You hold your own keys. We cannot recover a lost '
                   'recovery phrase, reverse a transaction, or retrieve '
                   'funds sent to a wrong address. Nobody from this project '
                   'will ever ask for a recovery phrase, and any request for '
                   'one is theft regardless of who appears to be asking.'),
                 h3('Verify the mint address'),
                 p('Tokens acquired from any address other than the official '
                   'mint published on this site are not LANDING. Checking '
                   'the address is your responsibility and it takes ten '
                   'seconds.'),
                 h3('Public features are public'),
                 p('Marks on the Wall and Certified Lander cards are '
                   'published deliberately, together with the wallet address '
                   'they are tied to. Do not post anything you want kept '
                   'private.'),
                 h3('Acceptable use'),
                 ul([
                     'Do not post scam links, impersonate the project, or '
                     'publish addresses presented as official',
                     'Do not attempt to disrupt or overload the site or its '
                     'services',
                     'Do not use project branding to suggest an endorsement '
                     'that does not exist',
                 ]),
                 p('We can remove content and restrict access to features '
                   'where these are breached. Criticism of the project is '
                   'not a breach and is never removed on that basis.'),
             )),

        band('03', 'The rest', 'Availability, liability and changes.',
             body=prose(
                 h3('Availability'),
                 p('The site and its features are provided as they are, '
                   'without warranty. Readings depend on third-party '
                   'services that can fail, and when they do the interface '
                   'says so rather than substituting an estimate. We do not '
                   'guarantee uptime or uninterrupted access.'),
                 h3('Third-party services'),
                 p('Exchanges, wallets, explorers and swap interfaces linked '
                   'from this site are operated by other people. We are not '
                   'responsible for them and we do not control them. A link '
                   'is a convenience, not an endorsement.'),
                 h3('Limitation of liability'),
                 p('To the fullest extent the law allows, the project and '
                   'those operating it are not liable for losses arising '
                   'from use of this site, acquisition or disposal of '
                   'LANDING, reliance on any information published here, or '
                   'the failure of any third-party service.'),
                 h3('Changes'),
                 p(f'These terms were last updated on {UPDATED}. Continued '
                   'use after a change means acceptance of the updated '
                   'terms.'),
                 h3('Contact'),
                 p('<a href="mailto:contact@landingcoin.fun">'
                   'contact@landingcoin.fun</a> for anything that needs a '
                   'written record.'),
             )),

        cta('Read before you buy, not after.',
            'The risk section on the buy page says the same thing in fewer '
            'words.',
            [('Before you buy', '/buy/', True),
             ('Privacy policy', '/privacy.html', False)]),
    ]),
}


# ================================================================== 404 =====

NOT_FOUND = {
    'route': '/404.html',
    'title': 'Page Not Found | LANDING',
    'description': 'That page does not exist. Which, for a project with a '
                   'supply of 404,000,000, is at least on brand.',
    'noindex': True,
    'body': ''.join([
        hero(
            title='404. <mark>Nothing found here</mark>.',
            lede='Which is the joke the supply is named after, so at least '
                 'the branding is consistent. The page you wanted is not '
                 'here. These ones are.',
            chips=[('Error 404', False), ('Supply: 404,000,000', True)],
        ),

        band('01', 'Try these', 'The pages people actually want.',
             body=panels([
                 ('Start', 'About the project',
                  'What LANDING is, in plain terms.', '/about.html'),
                 ('Check', 'Transparency',
                  'Token facts, wallets and live readings.', '/transparency.html'),
                 ('Buy', 'Markets and routes',
                  'Where it trades and how to get there safely.', '/markets.html'),
                 ('Supply', 'Tokenomics',
                  'All 404,000,000 and where each line went.', '/tokenomics.html'),
                 ('Join', 'Community',
                  'Discord, Telegram, Reddit and X.', '/community.html'),
                 ('Ask', 'FAQ',
                  'The questions that keep coming up.', '/faq.html'),
             ])),

        cta('Or go back to the start.',
            'The home page has the short version of everything.',
            [('Home', '/', True), ('Site FAQ', '/faq.html', False)]),
    ]),
}
