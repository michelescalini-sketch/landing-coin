"""
The illustrated furniture every page sits in.

Generated rather than hand-written because a star field is 90 near-identical
elements. The random seed is fixed, so the same sky is produced on every
build and a rebuild never shows up as noise in a diff.
"""

import random


def stars(count=90, seed=20260404):
    """A still star field, each star twinkling on its own offset."""
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        x = round(rng.uniform(0, 100), 2)
        y = round(rng.uniform(0, 92), 2)
        r = round(rng.choice([0.55, 0.7, 0.9, 1.2]), 2)
        o = round(rng.uniform(0.18, 0.62), 2)
        d = round(rng.uniform(0, 9), 1)
        out.append(
            f'<circle cx="{x}%" cy="{y}%" r="{r}" '
            f'style="--o:{o};animation-delay:{d}s"/>')
    return (f'<svg class="starfield" aria-hidden="true" preserveAspectRatio="none">'
            f'{"".join(out)}</svg>')


def sky():
    """The fixed backdrop. One per page, first thing in the body."""
    return f'<div class="sky" aria-hidden="true">{stars()}</div>'


def orbit():
    """The dashed orbital diagram from the home page hero, as a corner mark."""
    ticks = []
    for i in range(48):
        import math
        a = math.radians(i * 7.5)
        x1, y1 = 120 + 104 * math.cos(a), 120 + 104 * math.sin(a)
        x2, y2 = 120 + (112 if i % 4 == 0 else 108) * math.cos(a), \
                 120 + (112 if i % 4 == 0 else 108) * math.sin(a)
        ticks.append(f'<line class="radar-tick" x1="{x1:.1f}" y1="{y1:.1f}" '
                     f'x2="{x2:.1f}" y2="{y2:.1f}"/>')

    return f'''<svg class="radar" viewBox="0 0 240 240" aria-hidden="true">
{''.join(ticks)}
<circle class="radar-ring" cx="120" cy="120" r="96"/>
<circle class="radar-ring" cx="120" cy="120" r="62" opacity="0.6"/>
<circle class="radar-dash" cx="120" cy="120" r="79"/>
<circle class="radar-ring" cx="152" cy="96" r="13" opacity="0.5"/>
<g class="radar-blip"><circle cx="120" cy="41" r="5"/></g>
</svg>'''


# Two overlapping horizon profiles. Drawn once here so every page's skyline
# is literally the same landscape rather than a lookalike.
_FAR = ('M0 112 C 120 86, 190 104, 300 78 S 520 56, 660 84 '
        'S 880 118, 1040 88 S 1280 54, 1440 86 L1440 230 L0 230 Z')
_NEAR = ('M0 158 C 150 132, 250 170, 400 150 S 640 110, 790 146 '
         'S 1010 186, 1180 152 S 1360 120, 1440 140 L1440 230 L0 230 Z')


def ridge():
    """The horizon under a page hero, with hatching on the near slope."""
    hatch = ''.join(
        f'<line class="hatch" x1="{x}" y1="168" x2="{x - 26}" y2="230"/>'
        for x in range(40, 1480, 34))

    return f'''<svg class="ridge" viewBox="0 0 1440 230" preserveAspectRatio="none" aria-hidden="true">
<path class="far" d="{_FAR}"/>
<path class="rim" d="{_FAR.split(' L1440')[0]}" opacity="0.5"/>
<path class="near" d="{_NEAR}"/>
<g clip-path="url(#ridgeclip)">{hatch}</g>
<clipPath id="ridgeclip"><path d="{_NEAR}"/></clipPath>
<path class="rim" d="{_NEAR.split(' L1440')[0]}"/>
</svg>'''


_TRAIL = ('M-20 196 C 180 150, 330 214, 520 182 S 830 118, 1010 160 '
          'S 1300 206, 1460 164')


def trail(pod=True):
    """
    The dotted route that runs between landing sites. A pod rides it using
    offset-path, which takes the same path data as a custom property so the
    dots and the pod can never drift apart.
    """
    rider = (f'<circle class="pod" r="4.5" style="--path:path(\'{_TRAIL}\')"/>'
             if pod else '')
    return f'''<svg class="ridge" viewBox="0 0 1440 230" preserveAspectRatio="none" aria-hidden="true" style="z-index:-1">
<path class="trail" d="{_TRAIL}"/>
{rider}
</svg>'''


def hero_scene(with_orbit=True):
    """Everything that sits behind a page hero."""
    return (orbit() if with_orbit else '') + ridge() + trail()


# ------------------------------------------------------- portrait hero ----

def hero_portrait():
    """
    The hero backdrop, composed for a tall screen.

    The wide drawing is 1920x1080 and tells its story across the width: the
    moon at x=1200, a dashed descent arc curving down from it, and the
    lander touching down below. A phone crops that to roughly x=950..1250,
    which cuts the moon at its edge, cuts the lander in half, and leaves
    thirty units of the arc crossing the screen on its way to nothing.

    Re-cropping cannot fix it. The moon and the lander sit on the same
    column, so any window wide enough to hold them both lands them on top
    of the headline. So the phone gets its own arrangement of the same
    parts: moon above the text, the arc falling the length of the screen,
    the lander on the ground below. Same construction, same tokens, same
    lander drawing as the wide version, read top to bottom instead of
    left to right.

    Kept in step with the wide drawing by hand. If the moon or the lander
    changes there, change it here too.
    """
    import math

    # The moon, at 0.6 of the wide drawing's size, same three rings.
    mx, my = 250, 110
    ticks = []
    for i in range(72):
        a = i * math.pi / 36
        r0 = 76 if i % 6 else 72
        r1 = 86 if i % 6 else 92
        ticks.append(
            f'<line x1="{mx + r0 * math.cos(a):.1f}" y1="{my + r0 * math.sin(a):.1f}" '
            f'x2="{mx + r1 * math.cos(a):.1f}" y2="{my + r1 * math.sin(a):.1f}" '
            f'stroke="var(--text-3)" stroke-opacity="0.6" stroke-width="1.5"/>')

    stars = []
    rnd = random.Random(20261021)
    for _ in range(70):
        x = rnd.uniform(0, 400)
        y = 840 * (rnd.random() ** 1.6)
        r = rnd.choice([1, 1, 1.4, 1.8, 2.2])
        o = round(rnd.uniform(0.25, 0.85), 2)
        cls = ' class="tw"' if rnd.random() < 0.35 else ''
        d = f' style="animation-delay:{rnd.uniform(0, 3):.1f}s"' if cls else ''
        stars.append(f'<circle{cls} cx="{x:.1f}" cy="{y:.1f}" r="{r}" '
                     f'fill="var(--text)" opacity="{o}"{d}/>')

    hatch = ''.join(
        f'<path d="M-60 {y} Q140 {y - 26} 240 {y - 6} T460 {y - 18}"/>'
        for y in range(846, 1140, 13))

    return f'''<svg class="hero-portrait" viewBox="0 0 400 1080" \
preserveAspectRatio="xMidYMid slice" width="100%" height="100%" aria-hidden="true">
<defs>
<linearGradient id="pskyg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#080A0F"/><stop offset="1" stop-color="#151A26"/>
</linearGradient>
<radialGradient id="pglow" cx="262" cy="150" r="300" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="var(--accent)" stop-opacity="0.16"/>
<stop offset="1" stop-color="var(--accent)" stop-opacity="0"/>
</radialGradient>
<clipPath id="pground"><path d="M-60 858 Q120 820 250 852 T460 836 V1140 H-60 Z"/></clipPath>
</defs>

<g class="pl pl0">
<rect x="-60" y="-40" width="520" height="1180" fill="url(#pskyg)"/>
<rect x="-60" y="-40" width="520" height="1180" fill="url(#pglow)"/>
{''.join(stars)}
<!-- No transform-origin here. .spin-slow is transform-box:fill-box with
     transform-origin:center, which is already the centre of this ring.
     Setting an origin in viewBox units would be measured from the ring's
     own bounding box corner instead, putting the pivot ~158 units off and
     making the ticks orbit rather than spin. -->
<g class="spin-slow">{''.join(ticks)}</g>
<circle cx="{mx}" cy="{my}" r="50" fill="var(--surface-4)" stroke="var(--text)" stroke-width="2.4"/>
<circle cx="{mx}" cy="{my}" r="57" fill="none" stroke="var(--text-3)" stroke-opacity="0.7" stroke-width="1.5"/>
<circle cx="{mx}" cy="{my}" r="72" fill="none" stroke="var(--text)" stroke-opacity="0.35" stroke-width="1.3" stroke-dasharray="3 9"/>
<circle cx="{mx - 15}" cy="{my - 12}" r="13" fill="none" stroke="var(--text-3)" stroke-opacity="0.55" stroke-width="1.3"/>
<circle cx="{mx + 14}" cy="{my + 17}" r="8" fill="none" stroke="var(--text-3)" stroke-opacity="0.5" stroke-width="1.2"/>
<circle cx="{mx + 57}" cy="{my}" r="5" fill="var(--accent)"/>
</g>

<g class="pl pl2">
<path class="flow" d="M196 176 Q74 368 128 556 Q182 740 219 880"
      fill="none" stroke="var(--accent)" stroke-opacity="0.3"
      stroke-width="3" stroke-dasharray="14 13"/>
</g>

<g class="pl pl3" style="translate:0 58px">
<path d="M-60 886 Q130 852 250 880 T460 864 V1140 H-60 Z" fill="#0E1117" stroke="#262B33" stroke-width="1.2"/>
<path d="M-60 858 Q120 820 250 852 T460 836 V1140 H-60 Z" fill="var(--surface-2)" stroke="var(--text-3)" stroke-opacity="0.75" stroke-width="1.4"/>
<g clip-path="url(#pground)" stroke="var(--text-3)" stroke-opacity="0.28" stroke-width="0.8" fill="none">{hatch}</g>

<path d="M62 924 a44 44 0 0 1 88 0 Z" fill="var(--surface-2)" stroke="var(--text-3)" stroke-opacity="0.8" stroke-width="1.5"/>
<path d="M98 924 v-14 a8 8 0 0 1 16 0 v14 Z" fill="var(--ground)" stroke="var(--text-3)" stroke-opacity="0.7" stroke-width="1.2"/>
<path d="M338 902 v-46" stroke="var(--text-3)" stroke-width="2.4"/>
<path d="M340 858 l30 6 -3 24 -27 -6 Z" fill="var(--accent)"/>

<ellipse class="flow" cx="225" cy="898" rx="92" ry="17" fill="none"
         stroke="var(--accent)" stroke-width="3.4" stroke-dasharray="15 11"/>
<g transform="translate(225,894) scale(0.33)">
<ellipse cx="0" cy="6" rx="170" ry="14" fill="var(--well)" opacity="0.6"/>
<g stroke="var(--text)" stroke-linecap="round" fill="none">
<line x1="-52" y1="-95" x2="-112" y2="-4" stroke-width="9"/>
<line x1="52" y1="-95" x2="112" y2="-4" stroke-width="9"/>
<line x1="-72" y1="-150" x2="-104" y2="-40" stroke-width="5"/>
<line x1="72" y1="-150" x2="104" y2="-40" stroke-width="5"/>
<line x1="-140" y1="-4" x2="-84" y2="-4" stroke-width="9"/>
<line x1="140" y1="-4" x2="84" y2="-4" stroke-width="9"/>
</g>
<polygon points="-24,-96 24,-96 34,-60 -34,-60" fill="var(--text-3)"/>
<rect x="-80" y="-148" width="160" height="56" rx="6" fill="var(--text)"/>
<rect x="-80" y="-124" width="160" height="10" fill="var(--accent)"/>
<polygon points="-58,-148 58,-148 74,-186 74,-216 44,-250 -44,-250 -74,-216 -74,-186" fill="var(--text)"/>
<polygon points="44,-250 74,-216 74,-186 58,-148 36,-148 54,-190 54,-214" fill="var(--ground)" opacity="0.18"/>
<circle cx="0" cy="-206" r="24" fill="var(--ground)" stroke="var(--text-3)" stroke-width="5"/>
<circle class="visor" cx="0" cy="-206" r="16" fill="var(--accent)"/>
<line x1="36" y1="-250" x2="62" y2="-296" stroke="var(--text)" stroke-width="5" stroke-linecap="round"/>
<circle class="blink" cx="62" cy="-298" r="7" fill="var(--accent)"/>
</g>
</g>
</svg>
'''
