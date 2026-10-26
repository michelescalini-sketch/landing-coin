# LANDING website source

> **Author and rights**
>
> Design by **Furqan**, FOMNIX Studio ([fomnix.studio](https://fomnix.studio)).
> Code by **Hassan**.
>
> This is commissioned work. **Michele Scalini has paid for it and holds full
> rights** to the design and to everything in this source: he may use, change,
> publish and distribute it without restriction or further permission, and
> does not owe any further payment for that use.


Static site for [landingcoin.fun](https://landingcoin.fun). Twenty-four pages
and eleven compatibility redirects, no framework, no build dependencies beyond
Python's standard library. The builder lives here in `site-source/`; the
site it writes is `docs/`, which GitHub Pages serves.

---

## Running it

From the repository root:

```bash
python3 -B site-source/_src/build.py --out docs   # rebuild every page
cd docs && python3 -m http.server 8000             # preview at localhost:8000
```

Page content is edited in `site-source/_src/`. The stylesheets, `ui.js` and
`assets/` are edited in place in `docs/`, because they are shipped exactly
as written; the build reads and checks them there.

There is no `npm install`, no bundler and no CI step. The build takes about a
second and writes plain HTML.

---

## How it fits together

```
site-source/_src/     everything that generates the site
  build.py            the builder: wraps each page in the shared document
  chrome.py           header, drawer and footer, defined once
  scene.py            the illustrated backdrop (sky, horizon, trail, radar)
  sections.py         markup helpers for the repeating section patterns
  pages/              page content, one module per group
    home.py           the illustrated home page
    core.py           about, supply, markets, the two buying routes, buy
    transparency.py   the dashboard
    features.py       Wall, Certified Lander, Community
    project.py        Flight Plan, Team, Media Kit, FAQ, News
    legal.py          privacy, cookies, terms, 404
  home-body.html      the home page's illustrated world, kept as markup
  pages/news_originals.py  the three news posts, word for word

docs/*.css            stylesheets, loaded in the order listed below
docs/ui.js            scroll position, clipboard, counters, nav panels, drawer,
                      live reading states, off-screen pause, mirrored text
docs/assets/fonts/    the two self-hosted typefaces (woff2, with ttf fallback)
docs/assets/team/     team portraits
docs/assets/brand/    the logo offered on the Media Kit page
docs/assets/banners/  the banner offered on the Media Kit page
docs/favicon.*        icon set, plus apple-touch-icon and the web manifest
```

A page is a dictionary: route, title, description and a `body` built from the
helpers in `sections.py`. `pages/__init__.py` lists them all, and the builder
derives `sitemap.xml` from that same list, so a page can never exist without
being indexed or be indexed without existing.

---

## Stylesheet order

Load order is deliberate and the builder enforces it:

| Sheet | What it owns |
|---|---|
| `tokens.css` | every colour, type step, space, easing and duration |
| `base.css` | element defaults: type, colour, focus ring, page width |
| `motion.css` | the home page's keyframes |
| `style.css` | the home page's components |
| `chrome.css` | header, drop panels, mobile drawer, footer |
| `scene.css` | sky, horizon ridge, trail, radar, page hero |
| `sections.css` | section patterns, plus shared instruments |
| `mobile.css` | responsive overrides for the home page's own classes |
| `features.css` | Wall and Certified Lander (those two pages only) |
| `transparency.css` | the dashboard (that page only) |

### Two things to know before editing CSS

`style.css` is the home page's original stylesheet and it defines around two
hundred very short class names. Reusing one of them in another sheet silently
inherits rules written for a different element. `.band` there is a 210px
display heading; a section wrapper by that name set every paragraph inside it
to 187px and pushed the document 17,000 pixels wide, with no warning from
anywhere.

`build.py` now checks for this and refuses to build if one of our sheets
redefines a class `style.css` already owns. If you add a class and the build
stops, rename it rather than removing the check.

`mobile.css` is the one deliberate exception and is excluded from that
check, because overriding the home page's classes at phone width is its
entire job. See below.

The second trap is that a stylesheet with one brace too many does not fail
loudly. The browser throws away everything from the error onward and renders
the rest, so the page still appears with some rules quietly missing, and a
screenshot will not necessarily show it. `build.py` counts braces in every
sheet and refuses to build on an imbalance.

The third is that keyframe names are global. Two sheets once both defined
`twinkle`, the later one won, and the home page's stars quietly stopped
twinkling. An animation that names keyframes nobody defined fails just as
quietly. `build.py` refuses to build on either.

`[hidden]` is forced to `display: none !important` in `base.css`. Without
it, any class that sets `display` beats the browser's own `hidden` rule, and
the project scripts hide and show things with `hidden` all the time.

---

## Design tokens

Everything visual is a custom property in `tokens.css`. Changing the accent
is one line; there are no hardcoded hex values in the component sheets.

```css
--accent: #FFC44F;    /* and --accent-soft, --accent-pale        */
--surface-0 … -11     /* the dark surface ladder                 */
--step--2 … --step-5  /* the type scale                          */
--space-1 … --space-12
--ease                /* cubic-bezier(0.2, 0.8, 0.2, 1), the house curve */
--dur-fast … --dur-ambient
```

---

## The phone

The home page was drawn at 1440px. Its illustrated scenes are absolutely
positioned SVGs filling a container sized by `aspect-ratio`, and several of
them carry their layout in an **inline** `style` attribute. An inline style
outranks any stylesheet rule, so the home page's own mobile rule
(`.scn.stk > svg { display: none }`) never took effect: on a phone each
scene stretched to fill a tall narrow box and the drawing inside shrank to
a thumbnail floating in empty space.

`mobile.css` takes those scenes out of the absolute-fill arrangement, lets
them keep the proportions of their own viewBox, and runs them full bleed
scaled past the screen edge with the container cropping the sides. Every
scene has its subject in the middle, so the crop costs nothing and the
detail roughly doubles. The cards that floated on top of each scene stack
underneath it instead.

It also unstacks three things the desktop layout builds by absolute
positioning, because in a narrow column they collapsed:

- the token-facts, markets and wall scenes, whose amber dashed lines
  (`path.flow`) are connectors running out to where an overlay card sits on
  a wide screen. Once those cards stack underneath, the lines would arrive
  at nothing, so below 900px each scene fades out on all four sides and the
  lines run off into the dark instead of stopping at an edge.
- the closing scene (`.scn.mt`), which holds two drawings. The nested one
  is the ground the lander comes down on and belongs in the flow as the
  closing image. The other is the sky behind the whole call to action: 16:9
  and mostly empty space, because on a wide screen nobody looks at it
  directly. Putting it in the flow left 300px of near-empty sky between the
  lander and the footer, so it stays a backdrop, pinned to the top of the
  section and fading out, which also puts the moon behind the line about
  not going to the moon.
- the touchdown block inside it, which collapsed to 127px, crushing the
  drawing, putting the confirmation pill on the astronauts, and hiding the
  three step cards even though the copy above promises "three steps to
  land".

The hero status badge is a fourth case. On a wide screen it is one row:
a live dot, "Independent memecoin on Solana", a hairline separator, then
the Mainnet live pill. Saying that needs 469px and a phone offers 350, so
it wrapped onto two or three rows and stranded the separator at the end of
a line. It now holds one row and scales with the viewport, and the
separator is dropped, since a divider only earns its place between two
things that are both comfortable on the same line.

`style.css` also hides `.fcard.hm` below 900px. On the hero that is right,
since those cards repeat the headline. In the About section it left a tall
empty column beside the text, so there they are brought back as a stack.

That file is the only place allowed to re-declare `style.css` classes, and
`!important` appears in it only where it is overriding an inline style or
an absolute position set for the desktop layout.

## Motion

Scroll-driven animation uses native CSS timelines (`animation-timeline:
view()`), so there is no scroll listener anywhere and nothing runs on the
main thread during scroll.

### The touchdown sequence

The lander's descent, the dust burst, the shockwave and the confirmation
are one set, keyed so the lander meets the ground at 62% of a shared
timeline. On a wide screen that timeline is the scroll position, which
hands the reader control of the landing.

A thumb cannot do that. A flick carries momentum, and on iOS the address
bar collapsing mid-scroll changes the viewport height, which moves the
range the animation is measured against, so the lander jumps up and down
rather than coming down. Below 900px it plays once on its own clock when
the scene arrives, keeping the same 62% touchdown so all four stay in
step. With JavaScript off nothing is hidden: the confirmation rests
visible rather than waiting for an animation that will never run.

### Counters

The numbers that count up (`.c404`, `.c50`, `.c6`, `.cu`) are **not**
scroll-linked, and should not be made so again. A scroll-linked counter
reads 0 until the scroll position reaches it, which meant a card sitting in
plain view on a phone showing "COMMUNITY SHARE 0%", and it moves in steps
with the scroll wheel rather than running smoothly.

The count is written by `ui.js`, a frame at a time, rather than done in
CSS. These counters work by feeding a registered custom property into
`counter-reset`, and engines do not agree on whether generated content
repaints while that property interpolates. WebKit does not, so on an
iPhone the number sat at its final value and never moved. While counting,
the script writes ordinary text and switches `::before` off, so no engine
has to agree with us about anything.

The observer's root is shrunk 42% from the bottom on purpose: firing the
moment a number clears the bottom edge meant the count was spent before
the card had been read, so the trigger waits until the card sits in the
upper part of the screen.

With JavaScript off, `counter()` renders the resting value, which is the
real figure. With reduced motion, the count is skipped and the final
number shows immediately. **The page must never display a wrong
number**, so the resting state is always the true one and the animation
is the thing that is optional. The resting value in CSS
is the real figure, so a browser that never runs the observer shows the
correct number rather than a zero that never resolves. That ordering is
deliberate: **the page must never display a wrong number**, animation or
not.

Two things to know if you edit the animation:

- **`animation-delay` does nothing on a scroll timeline.** To stagger
  elements, shift each one's `animation-range` instead. Several components
  set that inline for exactly this reason.
- **An element scaled to zero has a zero-height box, which collapses a
  `view()` timeline on itself.** The supply column's bands hit this: the two
  smallest allocations could never un-collapse. They read their timeline from
  the container (`view-timeline-name: --supply`) instead.

All motion respects `prefers-reduced-motion: reduce`, and when it is set
every animation resolves to its finished state rather than leaving the page
half-arrived. The one exception is SMIL (`<animateMotion>` and friends in
the home page's drawings), which ignores CSS entirely, so `ui.js` freezes
those on a fixed frame.

### Off-screen pause

The home page has a few hundred running animations. `ui.js` watches each
section and adds `.is-offscreen` when it is well out of view, which pauses
every CSS animation inside it and pauses its SMIL. On a throttled phone that
took the median frame from 33ms to 16.7ms. Nothing changes visually: a
section is unpaused before it scrolls into view. There are still no scroll
listeners; this is an IntersectionObserver.

---

## Integrating with the existing project

Three things in this folder are deliberate about how they meet the
project's own files.

**`ui.js`, not `site.js`.** Every page in the project loads `/site.js`,
and that file holds the Transparency dashboard's data fetching
(`getJSON`, `load`, `reading`, `feedState`) and the Wall's `markCard`
renderer. A file of ours at that path would replace it, and the dashboard
would read "Awaiting source" forever. Our behaviour lives in `ui.js` and
the pages load both. Do not rename it back.

**`style.css` and `motion.css` do replace theirs.** That is the redesign,
and it is the only reason `redesign/qa/verify-migration.py` fails. That
check hashes the project's non-HTML source against
`redesign/source-manifest.json`, which still describes the previous build.
Twenty-eight files are guarded that way and twenty-six of them stay
byte-identical; the two that do not are those stylesheets. The manifest
needs regenerating for them, or the check retiring. Either way it is a
decision for the project owner, not something to work around.

Every other assertion in that script passes: the eleven compatibility
redirects, the public-page manifest, the indexability rules, the JS syntax
check, `CNAME`, `.nojekyll` and the crawl policy.

**The redirect list is not a free list.** `verify-migration.py` asserts each
of the eleven exists and forwards where the manifest says, so a page must
never be added at one of those paths.
`/why-landing-doesnt-promise-the-moon.html` is the one to watch: it reads
like an article URL but the project retired it into `/about.html`, so the
essay lives at `/news/the-argument-behind-the-joke.html` instead.

Two paths that look like page aliases are not. `/media/` and `/team/` are
asset directories in the project, holding `lander.mp4` and
`landing-manifesto.mp4`, and the two portraits. Nothing in this build
writes to either.

**The project's own scripts are referenced but not shipped.** `build.py`
emits the `<script>` tags each page needs, listed in `LEGACY_SCRIPTS`:

| Page | Scripts, in order |
|---|---|
| every page | `/site.js` |
| `/wall.html` | `/site.js`, Solana web3 1.98.4 (jsDelivr), `/wallet-standard.js` as a module, `/wall-live.js` |
| `/lander/` | `/site.js`, the Jupiter plugin, html2canvas 1.4.1 (jsDelivr), `/lander-live.js` |

The home page no longer loads `/app.js` or `/motion.js`. They drove the old
home page and threw errors against the new one. Serving this folder on its
own gives 404s for the project scripts, which is expected.

**`site.js` reads more than ids.** It also checks for `#hero-title` to
decide whether a page is the home page (without it, it runs code meant for
the old header and throws), and fills the Transparency dashboard by
`data-reading` keys (`positive`, `independent`, `price`, `liquidity` and so
on), gated on `#transparency-live`. `ui.js` watches those values and sets
each channel to live or unavailable, so the trace goes flat when a source
is down.

## The two interactive pages

`wall.html` and `lander/` are driven by the project's existing
`wall-live.js` and `lander-live.js`. The contract with those scripts is more
than the ids, and all of it is kept:

- **Every id** they look for exists on the page.
- **Element types.** `#lander-balance`, `#lander-wallet` and `#lander-id`
  are inputs, because the script reads and writes them with `.value`.
- **Starting states.** `#leave-mark` and `#download-card` start
  `disabled`, `#load-more` and `#registered-card-back` start `hidden`,
  `#live-card-flip` starts `aria-pressed="false"`, and `#lander-card`
  starts `data-certification="preview"`. The scripts flip these; they do
  not set them first.
- **Both versions of `lander-live.js`.** The Lander page works with the
  version on `sites-redesign` and with the newer one on `main`, which adds
  the confirmed slot, issue date, proof, signature and Solscan link
  (`#card-slot`, `#card-issued`, `#card-proof`, `#card-signature`,
  `#card-back-proof`, `#card-proof-link`). `#card-slot` is that text
  field, so the element that turns the card in 3D is `#card-turn`. The
  newer script unlocks Download itself; for the older one `ui.js` unlocks
  it, and hides any proof field still at its placeholder, once the card is
  confirmed. Both were tested end to end: restore, confirm, flip,
  download, reload and a pending swap resuming.
- **Starting text.** The card fields start with exactly what the newer
  `lander-live.js` expects before a card exists. The back repeats the
  Lander ID through `data-mirror`, copied by `ui.js`.
- **Input limits** match: 140 characters for a mark, 40 for a card name,
  44 for a wallet address.

The card turns in 3D, keyed off which face the script has `hidden`, so the
script did not have to change for the design to.

The project's offline tests (`redesign/qa/test-live-flows.cjs`) pass
against this markup, as do `verify-content.py` and every check in
`audit-final.py` except one line: it still expects Furqan's old title,
"Growth & Community Manager". The Team page uses the role Michele gave,
"Brand Designer & Senior Community Manager", so that line needs the new
title. `browser-qa.cjs` passes at all six widths apart from
two steps written for the previous layout: the motion on/off button, which
this design does not have, and the menu button's old name and id
(`.menu-toggle`, `#mobile-nav`; here `.hdr-burger` and `#drawer`).
`preproduction-dom-smoke.cjs` checks the previous home page's structure in
the same way. Those tests need updating to the new layout, the same as the
source manifest.

## Text that is quoted, not written

Some text is the project's own, kept word for word, because the project's
QA compares it against the original and fails on any difference:

- **The three news posts.** Their bodies live in
  `_src/pages/news_originals.py` with their original markup and class
  names (`article-body`, `cta`, `button`, `future`, `contract`, `risk`),
  inside `<article class="article-prose">`. Restyle them in CSS; do not
  edit the text. The headline and standfirst above each one are ours.
- **The five Flight Plan phases.** Status, title, summary and every item
  are the originals. Each phase is `<article class="flight-phase">` with
  exactly that class, an `h2` title and a `status-pill` printed in
  capitals, which is what the check selects on.
- **The FAQ** has 17 questions and each answer renders as one paragraph,
  because the check looks for every structured-data answer as one
  unbroken string in the page source.

The essay at `/news/the-argument-behind-the-joke.html` is public and
linked from News, but it is left out of `sitemap.xml` (`'sitemap': False`
on the page) because the check requires the sitemap to list exactly the
core pages and the three posts.

### Wording on these pages

The Wall and the Lander involve real transactions, and the copy says so.
A mark costs 5,000 LANDING plus the network fee, in one transaction the
visitor approves. A Lander card follows a swap made through Jupiter on
that page. Neither asks for a token allowance. If either flow changes,
change the copy on `wall.html`, `lander/`, the FAQ, the buy page and the
privacy policy with it.

---

## Accessibility

- Pages open at the top on a fresh navigation; back and forward still
  restore the previous position, and in-page anchors still work
- One `<h1>` per page, headings in order
- Skip link, visible focus ring on everything focusable, never removed
- Drop panels and the drawer work by keyboard: Enter opens, Escape closes
  and returns focus, tabbing out closes
- The FAQ uses native `<details>`, so it works with JavaScript off
- No image without `alt`, no button without an accessible name
- Text contrast meets WCAG AA on every page, desktop and phone, including
  live readings, failed sources and form placeholders
- Disabled buttons look disabled
- Verified at ten widths from 320 to 1920 with no horizontal scroll on any
  page

---

## Deploying

GitHub Pages, serving `docs/` from `main`. Four files are generated on
every build and are load-bearing:

- `.nojekyll`: stops Jekyll rewriting the output
- `CNAME`: the custom domain, `landingcoin.fun`
- `sitemap.xml` and `robots.txt`: the crawl policy
- `page-manifest.json`: the list of public routes with title and
  description, derived from the same page list as the sitemap

Nothing here needs adding by hand after a build. Run `build.py` and `docs/`
is deployable as it stands.

---

## What is not in here

- **Liquidity is not locked**, and the copy says so on every page that
  touches the subject. That is deliberate. Do not quietly soften it.
- No cookies, analytics, tag manager or advertising pixels. Nothing of
  ours is stored in a visitor's browser. The project's Lander script keeps
  two entries in local storage, `landing:lander-wallet` and
  `landing:pending-signature`, and the Cookie and Privacy pages describe
  exactly those two.
- No invented numbers. Where a reading cannot be fetched the interface says
  "unavailable" rather than showing the last value it saw.
