"""
The page list.

ALL is the single source of truth for what the site contains. The builder
writes one file per entry and derives the sitemap from the same list, so a
page can never exist without being indexed or be indexed without existing.
"""

from .home import HOME
from .core import ABOUT, TOKENOMICS, MARKETS, JUPITER_PAGE, POLONIEX_PAGE, BUY
from .transparency import TRANSPARENCY
from .features import WALL, LANDER, COMMUNITY
from .project import (FLIGHT_PLAN, TEAM, MEDIA_KIT, FAQ, NEWS_INDEX,
                      ARTICLE, POLONIEX_NEWS, WALL_NEWS, DISCORD_NEWS)
from .legal import PRIVACY, COOKIES, TERMS, NOT_FOUND

ALL = [
    HOME,
    ABOUT,
    TOKENOMICS,
    TRANSPARENCY,
    MARKETS,
    JUPITER_PAGE,
    POLONIEX_PAGE,
    BUY,
    WALL,
    LANDER,
    COMMUNITY,
    FLIGHT_PLAN,
    TEAM,
    MEDIA_KIT,
    FAQ,
    NEWS_INDEX,
    ARTICLE,
    DISCORD_NEWS,
    WALL_NEWS,
    POLONIEX_NEWS,
    PRIVACY,
    COOKIES,
    TERMS,
    NOT_FOUND,
]

# Compatibility redirects for URLs the project already serves, so no link
# that works today stops working. Each writes an index.html that forwards to
# the canonical page, carrying any query string and fragment across.
#
# This list matches the project's own redesign/qa/verify-migration.py, which
# asserts every one of these exists and points where it points. Do not add a
# real page at any of these paths: /why-landing-doesnt-promise-the-moon.html
# in particular is a retired essay URL the project folds into About, and the
# check fails if it stops being a redirect.
#
# /media/ and /team/ are deliberately absent. They look like page aliases but
# are asset directories in the project: /media/ holds lander.mp4 and
# landing-manifesto.mp4, /team/ holds the two portraits. Writing an
# index.html into either would drop a stray file into a folder of binaries.
REDIRECTS = {
    '/about/':            '/about.html',
    '/buy-token.html':    '/buy/',
    '/community/':        '/community.html',
    '/cookie/':           '/cookie-policy.html',
    '/faq/':              '/faq.html',
    '/lander.html':       '/lander/',
    '/markets/':          '/markets.html',
    '/privacy/':          '/privacy.html',
    '/terms/':            '/terms-of-service.html',
    '/tokenomics/':       '/tokenomics.html',
    '/why-landing-doesnt-promise-the-moon.html': '/about.html',
}

# Pages that pull in extra stylesheets beyond the shared set.
for _p in (WALL, LANDER):
    _p['css'] = ['features.css']
