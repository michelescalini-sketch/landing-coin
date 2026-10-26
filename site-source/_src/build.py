#!/usr/bin/env python3
"""
Site builder.

-----------------------------------------------------------------------
Design by Furqan, FOMNIX Studio (fomnix.studio). Code by Hassan.

Commissioned work. Michele Scalini has paid for this work and holds full
rights to the design and to everything in this source: he may use, change,
publish and distribute it without restriction or further permission.
-----------------------------------------------------------------------

Reads the page definitions in pages/, wraps each one in the shared chrome
and document head, and writes the result to the site folder.

    python3 _src/build.py              # site folder is the one above _src
    python3 _src/build.py --out docs   # or any folder you name

The site folder also holds the hand-written files the build reads and
checks: the stylesheets, ui.js and assets/. In the project repository the
source sits in site-source/ and the site is docs/, so from the repository
root that is:

    python3 site-source/_src/build.py --out docs

Every page is static HTML with no build-time dependencies beyond Python's
standard library, so the output folder is the whole deliverable.
"""

import json
import pathlib
import sys

SRC = pathlib.Path(__file__).resolve().parent


def _site_folder(argv):
    """The folder pages are written to: --out PATH, else the one above _src."""
    if '--out' in argv:
        i = argv.index('--out')
        if i + 1 >= len(argv):
            raise SystemExit('--out needs a folder, for example --out docs')
        return pathlib.Path(argv[i + 1]).resolve()
    return SRC.parent


ROOT = _site_folder(sys.argv[1:])
if not (ROOT / 'tokens.css').exists():
    raise SystemExit(f'{ROOT} does not look like the site folder '
                     '(no tokens.css). Pass the right one with --out.')
sys.path.insert(0, str(SRC))

import chrome  # noqa: E402
import scene   # noqa: E402

SITE = 'https://landingcoin.fun'

# Load order matters: tokens define the variables everything else reads,
# and page-specific sheets come last so they can override a shared rule.
BASE_CSS = ['tokens.css', 'base.css', 'motion.css', 'style.css',
            'chrome.css', 'scene.css', 'sections.css', 'mobile.css']

# Every stylesheet our pages load. In the project repository docs/ also
# holds the previous site's stylesheets, which no page of ours loads, so the
# checks below look at these and only these.
OUR_CSS = BASE_CSS + ['features.css', 'transparency.css']


# The project's own behaviour scripts, by the page that loads them. These
# are not ours and are not shipped by this build; the tags are emitted so
# that once this folder sits in the project the pages keep the behaviour
# they already had. Our file is ui.js, deliberately not site.js: every page
# in the project loads /site.js, and that file holds the Transparency
# dashboard's data fetching and the Wall's renderer. A file of ours at that
# path would replace it, and the dashboard would read "Awaiting source"
# forever.
#
# Each list is copied from the project's own page for that route, in the
# same order, because these scripts depend on each other: wall-live.js needs
# the Solana library and the wallet bridge already loaded, and lander-live.js
# needs the Jupiter plugin and html2canvas. A script missing from a list is
# a feature that silently stops working, so do not trim them by eye.
#
# An entry may be (src, 'module'). wallet-standard.js uses `import`, and as
# a classic script it throws before running a single line, which takes the
# wallet picker with it.
#
# The home page loads site.js only. The project's app.js and motion.js drive
# its old home page, a motion toggle and a manifesto toggle among other
# things, and find none of their twelve elements in this markup. Loaded
# here they did nothing except throw on every visit.
LEGACY_SCRIPTS = {
    '/': ['/site.js'],
    '/wall.html': ['/site.js',
                   'https://cdn.jsdelivr.net/npm/@solana/web3.js@1.98.4/lib/index.iife.min.js',
                   ('/wallet-standard.js', 'module'),
                   '/wall-live.js'],
    '/lander/': ['/site.js',
                 'https://plugin.jup.ag/plugin-v1.js',
                 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js',
                 '/lander-live.js'],
}
LEGACY_DEFAULT = ['/site.js']


def page_schema(page, route):
    """
    The structured data for a page, always as a @graph that includes a
    WebPage for this exact URL.

    A page may add its own entities (the home page its WebSite and
    Organization, an article its NewsArticle, the FAQ its FAQPage), but
    they are added alongside the WebPage, never instead of it. Pages that
    supplied their own schema used to replace the WebPage outright, which
    left the home page and every article without one; the project's
    redesign/qa/audit-final.py requires it on every route.
    """
    webpage = {
        '@type': 'WebPage',
        '@id': f'{SITE}{route}#webpage',
        'url': f'{SITE}{route}',
        'name': page['title'],
        'description': page['description'],
        'inLanguage': 'en',
        'isPartOf': {'@type': 'WebSite', 'name': 'Landing Coin', 'url': SITE + '/'},
    }
    custom = page.get('jsonld')
    if not custom:
        return {'@context': 'https://schema.org', '@graph': [webpage]}

    entities = []
    for e in custom.get('@graph', [custom]):
        e = {k: v for k, v in e.items() if k != '@context'}
        entities.append(e)

    def is_this_page(e):
        kinds = e.get('@type')
        kinds = kinds if isinstance(kinds, list) else [kinds]
        return 'WebPage' in kinds and e.get('url') == webpage['url']

    if not any(is_this_page(e) for e in entities):
        entities.insert(0, webpage)
    return {'@context': 'https://schema.org', '@graph': entities}


def script_tag(entry):
    """One <script> for a LEGACY_SCRIPTS entry. Modules are deferred by
    definition and run in document order with the defer scripts, so the
    order above holds either way."""
    if isinstance(entry, tuple):
        src, kind = entry
        if kind != 'module':
            raise SystemExit(f'Unknown script kind {kind!r} for {src}')
        return f'<script type="module" src="{src}"></script>\n'
    return f'<script src="{entry}" defer></script>\n'


def document(page):
    """Wrap one page definition in the shared head, chrome and scripts."""
    route = page['route']
    depth = route.count('/') - 1          # /routes/jupiter.html -> 1
    up = '../' * depth

    sheets = '\n'.join(
        f'<link rel="stylesheet" href="{up}{s}">'
        for s in BASE_CSS + list(page.get('css', ())))

    ld = page_schema(page, route)

    scripts = page.get('legacy_scripts',
                       LEGACY_SCRIPTS.get(route, LEGACY_DEFAULT))
    legacy = ''.join(script_tag(s) for s in scripts)

    noindex = ('<meta name="robots" content="noindex,follow">'
               if page.get('noindex') else
               '<meta name="robots" content="index,follow,max-image-preview:large">')

    return f'''<!doctype html>
<!--
  LANDING  |  landingcoin.fun

  Design by Furqan, FOMNIX Studio (fomnix.studio). Code by Hassan.

  Commissioned work. Michele Scalini has paid for this work and holds full
  rights to the design and to everything in this source.
-->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{page['title']}</title>
<meta name="description" content="{page['description']}">
{noindex}
<link rel="canonical" href="{SITE}{route}">

<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="Landing Coin">
<meta property="og:url" content="{SITE}{route}">
<meta property="og:title" content="{page['title']}">
<meta property="og:description" content="{page['description']}">
<meta property="og:image" content="{SITE}/landing-social.jpg">
<meta property="og:image:alt" content="Landing Coin. Everyone is going to the moon. We are landing.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@LandingCoin2026">
<meta name="theme-color" content="#0B0D12">

<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{up}favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">
<link rel="manifest" href="{up}site.webmanifest">

<link rel="preconnect" href="https://solscan.io">
<link rel="preload" href="{up}assets/fonts/space-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}assets/fonts/dm-sans.woff2" as="font" type="font/woff2" crossorigin>
{sheets}

<script type="application/ld+json">
{json.dumps(ld, separators=(',', ':'))}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{scene.sky()}
{chrome.header(route)}
<main id="main">
{page['body']}
</main>
{chrome.footer(route)}
{legacy}<script src="{up}ui.js" defer></script>
</body>
</html>
'''


# A compatibility redirect, in the shape redesign/qa/verify-migration.py
# requires: noindex,nofollow so the duplicate never gets indexed, and a
# script that carries any query string and fragment across so a shared
# link such as /lander.html?ref=x#certify still arrives intact. The meta
# refresh is the fallback for anything with scripting off.
REDIRECT = '''<!doctype html><html lang="en"><head><meta charset="utf-8">\
<meta name="viewport" content="width=device-width,initial-scale=1">\
<meta name="robots" content="noindex,nofollow">\
<meta http-equiv="refresh" content="0;url={target}">\
<title>LANDING &mdash; page moved</title>\
<link rel="canonical" href="{site}{target}">\
<script>location.replace("{target}"+location.search+location.hash);</script>\
</head><body><p>This LANDING page has moved. \
<a href="{target}">Continue to LANDING</a>.</p></body></html>
'''


def write(path, text):
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')
    return len(text)


def check_class_collisions():
    """
    The home page ships its own stylesheet with around two hundred very short
    class names. A new sheet that reuses one of them silently inherits rules
    written for a completely different element: .band in the home page sheet
    is a 210px display heading, so a section wrapper by that name set every
    paragraph inside it to 187px and pushed the document 17,000px wide.

    Nothing in CSS warns about that, so the build does. If a sheet of ours
    defines a selector the home page already owns, the build stops here
    rather than shipping a page that silently renders wrong.
    """
    import re

    def defined_classes(name):
        text = (ROOT / name).read_text(encoding='utf-8')
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
        # Only names this sheet actually defines rules for, not ones it
        # merely references inside a descendant selector.
        return {m.group(1) for m in re.finditer(
            r'\.([a-zA-Z][\w-]*)(?=[^{}]*\{)', text)}

    inherited = defined_classes('style.css') | defined_classes('motion.css')
    # mobile.css is the one sheet allowed to re-declare the home page's own
    # classes, because overriding them at phone width is its whole job.
    ours = ['base.css', 'chrome.css', 'scene.css', 'sections.css',
            'features.css', 'transparency.css']

    clashes = []
    for sheet in ours:
        for name in sorted(defined_classes(sheet) & inherited):
            clashes.append(f'  .{name} redefined in {sheet}')

    if clashes:
        raise SystemExit(
            'Class name collision with the home page stylesheet:\n'
            + '\n'.join(clashes)
            + '\n\nRename the class in our sheet. Reusing a name from '
              'style.css inherits its rules.')


def check_stylesheets():
    """
    Catch a structurally broken stylesheet before it ships.

    A CSS file with one brace too many does not fail loudly: the browser
    discards everything from the error onward and renders the rest, so the
    page still appears, just with some rules silently missing. Nothing in a
    screenshot test necessarily shows it either. Counting braces takes a
    millisecond and turns that into a build failure.
    """
    problems = []
    for sheet in [ROOT / name for name in OUR_CSS]:
        text = sheet.read_text(encoding='utf-8')

        depth = 0
        for char in text:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth < 0:
                    problems.append(f'  {sheet.name}: closing brace with '
                                    f'nothing open')
                    break
        else:
            if depth:
                problems.append(f'  {sheet.name}: {depth} unclosed '
                                f'{"block" if depth == 1 else "blocks"}')

    if problems:
        raise SystemExit('Malformed stylesheet:\n' + '\n'.join(problems))


def check_keyframes(built):
    """
    Two keyframe failures that CSS never reports.

    A keyframe name is global, and when two sheets declare the same one the
    later sheet wins everywhere. scene.css once declared `twinkle`, which
    the home page's motion.css already owned, and quietly replaced the home
    page's star twinkle with a dimmer one.

    And an animation that names a keyframe nobody declared does nothing:
    no error, no warning, the element just never moves. The rule under each
    section head pointed at a `ruledraw` that did not exist.

    Both are checked here, across our stylesheets and the pages this build
    writes, since several pieces of artwork set their animation inline.
    """
    import re

    def strip(t):
        return re.sub(r'/\*.*?\*/', '', t, flags=re.S)

    owners = {}
    for sheet in [ROOT / name for name in OUR_CSS]:
        for name in re.findall(r'@keyframes\s+([\w-]+)',
                               strip(sheet.read_text(encoding='utf-8'))):
            owners.setdefault(name, []).append(sheet.name)
    clashes = [f'  @keyframes {n} declared in {", ".join(s)}'
               for n, s in sorted(owners.items()) if len(s) > 1]

    # Words that can appear in an animation shorthand and are not names.
    keywords = {
        'none', 'infinite', 'linear', 'ease', 'ease-in', 'ease-out',
        'ease-in-out', 'step-start', 'step-end', 'both', 'forwards',
        'backwards', 'normal', 'reverse', 'alternate', 'alternate-reverse',
        'running', 'paused', 'auto', 'initial', 'inherit', 'unset', 'var',
        'cubic-bezier', 'steps', 'calc', 'jump-start', 'jump-end',
        'jump-none', 'jump-both', 'start', 'end', 'important',
    }
    sources = [strip((ROOT / s).read_text(encoding='utf-8')) for s in OUR_CSS]
    sources += [(ROOT / rel).read_text(encoding='utf-8') for rel in built]
    missing = set()
    for text in sources:
        for value in re.findall(r'animation(?:-name)?\s*:\s*([^;}"]+)', text):
            for word in re.findall(r'(?<![\w-])[a-zA-Z][\w-]*', value):
                if (word not in keywords and not word.startswith('--')
                        and word not in owners):
                    missing.add(word)
    gaps = [f'  animation "{n}" has no @keyframes' for n in sorted(missing)]

    if clashes or gaps:
        raise SystemExit('Keyframe problem:\n' + '\n'.join(clashes + gaps))


def main():
    import pages

    check_class_collisions()
    check_stylesheets()

    built = []
    for page in pages.ALL:
        rel = page['route'].lstrip('/')
        if rel.endswith('/') or rel == '':
            rel += 'index.html'
        size = write(rel, document(page))
        built.append((rel, size))

    for alias, target in pages.REDIRECTS.items():
        # A directory alias needs an index.html inside it; a file alias is
        # written at its own path.
        rel = alias.lstrip('/')
        if alias.endswith('/'):
            rel += 'index.html'
        write(rel, REDIRECT.format(site=SITE, target=target))

    # Machine-readable site index, kept in step with the page list so it can
    # never describe pages that no longer exist.
    urls = ''.join(
        f'<url><loc>{SITE}{p["route"]}</loc>'
        f'<changefreq>{p.get("changefreq", "monthly")}</changefreq>'
        f'<priority>{p.get("priority", "0.6")}</priority></url>'
        for p in pages.ALL
        if not p.get('noindex') and p.get('sitemap', True))
    write('sitemap.xml',
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          f'{urls}</urlset>\n')

    write('robots.txt',
          f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')

    # The list of public pages, in the shape the project's QA reads it:
    # every indexable route with its title and description. Derived from
    # the same page list as the sitemap, so the two cannot disagree.
    import html as _html
    manifest = [
        {'path': p['route'],
         'title': _html.unescape(p['title']),
         'description': _html.unescape(p['description'])}
        for p in pages.ALL if not p.get('noindex')
    ]
    manifest.sort(key=lambda e: e['path'])
    write('page-manifest.json', json.dumps(manifest, indent=2) + '\n')

    # GitHub Pages reads this to serve the site on its own domain. Without
    # it the site falls back to the github.io address.
    write('CNAME', 'landingcoin.fun\n')

    # GitHub Pages serves this folder as-is and must not run Jekyll over it.
    write('.nojekyll', '')

    # Runs last because it reads the pages just written: several drawings
    # set their animation inline rather than in a stylesheet.
    check_keyframes([rel for rel, _ in built])

    total = sum(s for _, s in built)
    for name, size in built:
        print(f'  {name:<42} {size // 1024:>4} KB')
    print(f'\n{len(built)} pages, {len(pages.REDIRECTS)} redirects, '
          f'{total // 1024} KB of HTML')


if __name__ == '__main__':
    main()
