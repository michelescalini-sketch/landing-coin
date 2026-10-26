"""
Markup helpers for the section patterns in sections.css.

Pages are written as a list of these calls, so a page file is content and
nothing else. Any change to how a pattern is marked up happens once, here.
"""

ARROW = ('<svg width="16" height="14" viewBox="0 0 16 14" fill="none" aria-hidden="true">'
         '<path d="M1 7h13M9 2l5 5-5 5" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def _attrs(url):
    return ' target="_blank" rel="noopener"' if url.startswith('http') else ''


# ---------------------------------------------------------------- hero ------

def hero(title, lede, chips=None, actions=None, note=None, crumbs=None,
         scene=True):
    """
    The opening block. `title` carries inline markup, so a page marks its
    own key phrase with <mark> the way the home page does.
    """
    from scene import hero_scene

    bits = []
    if crumbs:
        trail = '<span aria-hidden="true">/</span>'.join(
            (f'<a href="{h}">{t}</a>' if h else f'<span>{t}</span>')
            for t, h in crumbs)
        bits.append(f'<nav class="crumbs" aria-label="Breadcrumb">{trail}</nav>')

    if chips:
        pills = ''.join(
            f'<span class="pill">{c}</span>' if bold else f'<span>{c}</span>'
            for c, bold in chips)
        bits.append(f'<div class="chips"><span class="chips-dot" aria-hidden="true">'
                    f'</span>{pills}</div>')

    # id="hero-title" is read by the project's site.js. It splits on this
    # id: with it, the script skips a block written for the old header,
    # which looks up a .menu-toggle and #mobile-nav that this design does not
    # have and throws on the first one, taking the Transparency loader and
    # the Wall feed down with it. Everything in that block is handled here
    # already: the drawer and the copy buttons both live in ui.js.
    bits.append(f'<h1 id="hero-title">{title}</h1>')
    bits.append(f'<p class="hero-lede">{lede}</p>')

    if actions:
        bits.append(f'<div class="hero-actions">{buttons(actions)}</div>')
    if note:
        bits.append(f'<p class="sec-note" style="margin-top:var(--space-6)">{note}</p>')

    return f'''<section class="hero">
{hero_scene() if scene else ''}
<div class="page-wrap"><div class="hero-inner">
{''.join(bits)}
</div></div>
</section>'''


def buttons(actions):
    out = []
    for label, href, primary in actions:
        cls = 'btn btn-go' if primary else 'btn'
        tail = ARROW if primary else ''
        out.append(f'<a class="{cls}" href="{href}"{_attrs(href)}>{label}{tail}</a>')
    return ''.join(out)


# --------------------------------------------------------------- bands ------

def band(num, kicker, title, body, lede=None, note=None, anchor=None,
         note_id=None):
    head = [f'<span class="sec-num">{num} / {kicker}</span>', f'<h2>{title}</h2>']
    if lede:
        head.append(f'<p class="sec-lede">{lede}</p>')

    nid = f' id="{note_id}"' if note_id else ''
    tail = f'<p class="sec-note"{nid}>{note}</p>' if note else ''
    page_id = f' id="{anchor}"' if anchor else ''

    return f'''<section class="sec"{page_id}>
<div class="page-wrap">
<div class="sec-head">{''.join(head)}</div>
{body}
{tail}
</div>
</section>'''


def prose(*blocks):
    return f'<div class="prose rise">{"".join(blocks)}</div>'


def p(text):
    return f'<p>{text}</p>'


def h3(text):
    return f'<h3>{text}</h3>'


def ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


# --------------------------------------------------------------- panels -----

def panels(rows, cols=3):
    """rows: (kicker, title, body, href or None)"""
    out = []
    for kicker, title, body, href in rows:
        head = (f'<h3>{title}{ARROW if href else ""}</h3>')
        inner = (f'<span class="panel-k">{kicker}</span>{head}<p>{body}</p>')
        if href:
            out.append(f'<a class="panel" href="{href}"{_attrs(href)}>{inner}</a>')
        else:
            out.append(f'<div class="panel">{inner}</div>')
    return f'<div class="grid-{cols}">{"".join(out)}</div>'


def facts(rows):
    """The dark bordered fact cards from the home page. rows: (icon, title, body)"""
    out = []
    for icon, title, body in rows:
        out.append(f'''<div class="fact rise">
<span class="fico" aria-hidden="true">{icon}</span>
<div><b style="font-family:var(--font-display);font-size:var(--step-0)">{title}</b>
<p style="margin:6px 0 0;font-size:var(--step--1);color:var(--text-3);line-height:var(--leading-body)">{body}</p></div>
</div>''')
    return f'<div class="fgrid">{"".join(out)}</div>'


def cards(rows):
    """The white cards with the amber offset shadow. rows: (label, value, note)"""
    out = []
    for label, value, note in rows:
        out.append(f'''<div class="lcard rise">
<span style="font-family:var(--font-mono);font-size:11px;letter-spacing:0.16em;text-transform:uppercase;opacity:0.62">{label}</span>
<b style="font-family:var(--font-display);font-size:clamp(22px,2.4vw,30px);line-height:1.1">{value}</b>
<span style="font-size:13px;opacity:0.66">{note}</span>
</div>''')
    return (f'<div style="--ac:var(--accent);display:flex;flex-wrap:wrap;'
            f'gap:var(--space-5)">{"".join(out)}</div>')


# --------------------------------------------------------------- steps ------

def steps(rows):
    """rows: (title, [paragraphs])"""
    out = []
    for i, (title, paras) in enumerate(rows, 1):
        body = ''.join(f'<p>{t}</p>' for t in paras)
        out.append(f'<div class="step"><span class="step-n">{i:02d}</span>'
                   f'<h3>{title}</h3>{body}</div>')
    return f'<div class="steps">{"".join(out)}</div>'


# ------------------------------------------------------------ accordion -----

def qa(rows, open_first=False, one_paragraph=False):
    """
    rows: (question, [answer paragraphs])

    one_paragraph runs each answer together as a single paragraph. The FAQ
    page needs it: the project's QA looks for every structured-data answer
    as one unbroken string in the page source, and a paragraph break puts
    tags in the middle of it. faq_schema() joins the same way.
    """
    out = []
    for i, (q, answer) in enumerate(rows):
        if one_paragraph:
            body = f'<p>{" ".join(answer)}</p>'
        else:
            body = '\n'.join(f'<p>{a}</p>' for a in answer)
        is_open = ' open' if (open_first and i == 0) else ''
        out.append(f'<details{is_open}><summary>{q}</summary>'
                   f'<div class="qa-body">{body}</div></details>')
    return f'<div class="qa">{"".join(out)}</div>'


def _plain(fragment):
    """Text exactly as a browser reads it out of a fragment of markup."""
    import html, re
    return html.unescape(re.sub(r'<[^>]+>', '', fragment))


def faq_schema(rows):
    """
    The FAQPage entity for the same rows qa(one_paragraph=True) renders.

    Built from those rows rather than written twice, so a question can never
    be edited on the page and left stale in the search result. Each answer
    is the answer's text exactly as it reads on the page: search engines
    expect that, and the project's QA checks every one is visible verbatim.
    """
    return {
        '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question',
             'name': _plain(q),
             'acceptedAnswer': {'@type': 'Answer',
                                'text': _plain(' '.join(answer))}}
            for q, answer in rows
        ],
    }


# --------------------------------------------------------------- table ------

def table(headers, rows, caption=None):
    head = ''.join(f'<th scope="col">{h}</th>' for h in headers)
    body = []
    for r in rows:
        cells = ''.join(
            f'<td class="{cls}">{val}</td>' if cls else f'<td>{val}</td>'
            for val, cls in r)
        body.append(f'<tr>{cells}</tr>')
    label = f' aria-label="{caption}"' if caption else ''
    return f'''<div class="tbl-wrap rise"><table class="tbl"{label}>
<thead><tr>{head}</tr></thead>
<tbody>{''.join(body)}</tbody>
</table></div>'''


# ------------------------------------------------------------- callout ------

def callout(paras, mark='!'):
    body = ''.join(f'<p>{t}</p>' for t in paras)
    return (f'<div class="callout rise"><span class="callout-mark" aria-hidden="true">'
            f'{mark}</span><div>{body}</div></div>')


# ----------------------------------------------------------------- cta ------

def cta(title, body, actions):
    return f'''<section class="sec"><div class="page-wrap">
<div class="cta rise">
<h2>{title}</h2>
<p>{body}</p>
<div class="hero-actions">{buttons(actions)}</div>
</div>
</div></section>'''
