"""
The home page.

The illustrated world is the one piece of this site that is drawn rather
than assembled from section patterns, so its markup is kept as a file and
loaded here rather than rebuilt in Python. The in-page anchors it uses
(#about, #token, #landers, #community) are the ones the header links to.
"""

import pathlib

import scene

_BODY = (pathlib.Path(__file__).resolve().parent.parent /
         'home-body.html').read_text(encoding='utf-8')

# The hero carries two backdrops: the wide drawing the page was designed
# around, and a portrait arrangement of the same parts for phones. Only one
# is ever shown; mobile.css picks. The portrait one is injected here rather
# than pasted into the markup file so it stays generated code, with the
# star field and the moon's tick ring built by loop instead of by hand.
_WIDE = '<svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice"'
if _BODY.count(_WIDE) != 1:
    raise SystemExit('home-body.html: expected exactly one wide hero svg to '
                     'anchor the portrait backdrop against')
_BODY = _BODY.replace(_WIDE, scene.hero_portrait() + _WIDE, 1)


def _share_paint_servers(body):
    """
    Hoist the repeated hatch patterns and fade gradient into one shared
    definition.

    Every illustrated scene on this page carries its own copy of the same
    three paint servers: #hD (diagonal hatch), #hH (horizontal hatch) and
    #bfade. That is 31 elements sharing three ids, which is invalid, and it
    has a practical cost too. A url(#hD) reference resolves to the first
    element in the document with that id, and the first copy lives inside
    the wide hero drawing, which is display:none on a phone. Engines that
    will not paint from a display:none subtree then lose every hatched fill
    on the page at once.

    So the copies are removed and a single set is placed in a zero-size
    sprite at the top of the page. It is sized to nothing rather than
    hidden, because hiding it would reintroduce the problem it solves.
    Every copy was identical, so nothing renders differently.
    """
    import re
    shared = []
    for pid, tag in (('hD', 'pattern'), ('hH', 'pattern'),
                     ('bfade', 'linearGradient')):
        rx = re.compile(r'<%s\b[^>]*\bid="%s"[^>]*>.*?</%s>' % (tag, pid, tag),
                        re.S)
        found = rx.findall(body)
        if not found:
            raise SystemExit(f'home-body.html: no #{pid} definition found')
        if len(set(found)) != 1:
            # Hoisting is only safe while every copy is the same. If one is
            # edited on its own, stop rather than silently pick a winner.
            raise SystemExit(f'home-body.html: copies of #{pid} have diverged; '
                             f'give the edited one its own id')
        shared.append(found[0])
        body = rx.sub('', body)
    sprite = ('<svg class="paint-servers" width="0" height="0" '
              'aria-hidden="true" focusable="false" '
              'style="position:absolute;width:0;height:0;overflow:hidden">'
              '<defs>' + ''.join(shared) + '</defs></svg>\n')
    return sprite + body


_BODY = _share_paint_servers(_BODY)

HOME = {
    'route': '/',
    'title': 'Landing Coin (LANDING) | Everyone Is Going to the Moon. We Are Landing.',
    'description': 'An independent Solana memecoin with a fixed 404,000,000 '
                   'supply, mint and freeze disabled, and every project '
                   'wallet published. No price targets. No rocket emojis.',
    'priority': '1.0',
    'changefreq': 'weekly',
    'jsonld': {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebSite',
                '@id': 'https://landingcoin.fun/#website',
                'url': 'https://landingcoin.fun/',
                'name': 'Landing Coin',
                'description': 'Independent Solana memecoin. '
                               'Everyone is going to the moon. We are landing.',
                'inLanguage': 'en',
            },
            {
                '@type': 'Organization',
                '@id': 'https://landingcoin.fun/#org',
                'name': 'Landing Coin',
                'url': 'https://landingcoin.fun/',
                'email': 'contact@landingcoin.fun',
                'sameAs': [
                    'https://x.com/LandingCoin2026',
                    'https://www.linkedin.com/company/146683351',
                    'https://www.reddit.com/r/LandingCoin/',
                    'https://t.me/LandingCoinCommunity',
                ],
            },
        ],
    },
    'body': _BODY,
}
