"""
The LANDING Wall, Certified Lander and Community.

The Wall and Lander are driven by the project's existing wall-live.js and
lander-live.js. Those scripts find their elements by id, so every id they
look for is reproduced here exactly. The design changed; the contract did
not, which is what lets this drop in without rewiring the behaviour.
"""

from sections import hero, band, panels, facts, steps, callout, cta, qa
from chrome import SOCIAL, MINT

ICON_PIN = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
            '<path d="M9 16s5.5-5 5.5-9A5.5 5.5 0 003.5 7c0 4 5.5 9 5.5 9z" '
            'stroke="var(--accent)" stroke-width="1.5" stroke-linejoin="round"/>'
            '<circle cx="9" cy="7" r="1.8" stroke="var(--accent)" stroke-width="1.5"/></svg>')
ICON_BADGE = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
              '<path d="M9 2l2 1.6 2.5-.2.6 2.4 2 1.6-1.2 2.2 1.2 2.2-2 1.6'
              '-.6 2.4-2.5-.2L9 17l-2-1.6-2.5.2-.6-2.4-2-1.6L3.1 9.6 1.9 7.4'
              'l2-1.6.6-2.4L7 3.6 9 2z" stroke="var(--accent)" stroke-width="1.3" '
              'stroke-linejoin="round"/></svg>')
ICON_CHAT = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
             '<path d="M2 4h14v9H7l-5 3V4z" stroke="var(--accent)" '
             'stroke-width="1.5" stroke-linejoin="round"/></svg>')
ICON_NO = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
           '<circle cx="9" cy="9" r="6.5" stroke="var(--accent)" stroke-width="1.5"/>'
           '<path d="M4.5 4.5l9 9" stroke="var(--accent)" stroke-width="1.5"/></svg>')
ICON_KEY = ('<svg width="18" height="18" viewBox="0 0 18 18" fill="none">'
            '<circle cx="6" cy="9" r="3.4" stroke="var(--accent)" stroke-width="1.5"/>'
            '<path d="M9.4 9H16M13 9v3M15 9v2" stroke="var(--accent)" '
            'stroke-width="1.5" stroke-linecap="round"/></svg>')


# ================================================================ wall ======

WALL = {
    'route': '/wall.html',
    'title': 'The LANDING Wall | Everyone Who Touched Down',
    'description': 'A public message wall on Solana. One line of up to 140 '
                   'characters costs 5,000 LANDING plus the network fee. '
                   'Reading is free and nothing is ranked by balance.',
    'priority': '0.8',
    'body': ''.join([
        hero(
            title='Everyone who <mark>made it down</mark>.',
            lede='Pay 5,000 LANDING, leave one line, and it stays on Solana. '
                 'Reading is free. There is no ranking by balance and no way '
                 'to buy a better spot. It only records that you were here.',
            chips=[('The Wall', False), ('Free to read', True)],
            crumbs=[('LANDING', '/'), ('Wall', None)],
        ),

        # ---- The wall itself. Every id below is read by wall-live.js. -----
        band('01', 'Live', 'The wall',
             lede='Marks load from the project service. If it cannot be '
                  'reached the wall says so rather than showing you an empty '
                  'page and letting you assume nobody came.',
             anchor='wall-section',
             body='''<div class="console rise" style="margin-bottom:var(--space-6)">
<div class="console-bar">
<span class="pip" aria-hidden="true"></span>
<span>Marks on the wall</span>
<span class="bsep cbar-sep" aria-hidden="true"></span>
<span id="wall-count">Counting</span>
<span class="bsep cbar-sep" aria-hidden="true"></span>
<button type="button" class="vbtn" id="wall-reload" style="min-height:30px;padding:0 12px;font-size:11px">Reload <span aria-hidden="true">&#8635;</span></button>
</div>
<p id="wall-connection-note" class="channel-note" style="padding:var(--space-4) var(--space-6);margin:0">
Connecting to the wall service.
</p>
</div>

<div class="wall-grid" id="wall" aria-live="polite" aria-busy="true">
<p class="wall-empty">Waiting for the wall to answer.</p>
</div>

<div style="display:flex;justify-content:center;margin-top:var(--space-7)">
<button type="button" class="btn" id="load-more" hidden>Load more marks</button>
</div>''',
             ),

        # ---- Leaving a mark -----------------------------------------------
        band('02', 'Join', 'Leave your mark',
             lede='One line of up to 140 characters, text only. Kept short on '
                  'purpose: a wall of essays is a forum nobody reads.',
             body='''<div class="markbox rise">
<div class="markbox-head">
<span class="gauge-label">Your mark</span>
<span class="vlab" id="mark-status">Connect a wallet to post</span>
</div>

<label class="sr-only" for="mark-message">Your message</label>
<textarea id="mark-message" rows="3" maxlength="140"
  placeholder="Say something worth leaving behind."></textarea>

<div class="markbox-foot">
<span class="vlab"><span id="char-count">0</span> / 140</span>
<div class="srcbar">
<button type="button" class="vbtn" id="connect-wallet">Connect wallet</button>
<!-- Starts disabled: wall-live.js enables it once a wallet with enough
     LANDING is connected. Enabled from the start, it invited a mark with no
     wallet behind it. -->
<button type="button" class="btn btn-go" id="leave-mark" disabled style="min-height:44px;padding:0 var(--space-6);font-size:var(--step--1)">Leave a mark, 5,000 LANDING</button>
</div>
</div>
</div>''',
             note='A mark costs 5,000 LANDING plus a small SOL network fee. '
                  'The payment and your message go in one Solana transaction, '
                  'so read the wallet request before you approve it. LANDING '
                  'bought on an exchange has to be withdrawn to your own '
                  'Solana wallet first.'),

        band('03', 'Rules', 'What the wall is and is not.',
             body=facts([
                 (ICON_PIN, 'Not a leaderboard',
                  'Marks appear in the order they were left. A larger balance '
                  'does not move you up, because that would make the wall a '
                  'scoreboard and scoreboards attract a worse crowd.'),
                 (ICON_NO, 'Not a giveaway',
                  'There is nothing to win here. If someone tells you posting '
                  'on the wall qualifies you for an airdrop, they are lying '
                  'and probably about to ask for your seed phrase.'),
                 (ICON_KEY, 'One payment, no allowance',
                  'A mark is a single transfer of 5,000 LANDING with your '
                  'message attached. It never asks for a spending allowance, '
                  'and any prompt that does is not from us.'),
                 (ICON_CHAT, 'Public for good',
                  'Links are not allowed. A message with abuse or illegal '
                  'content can be hidden from this page, but the transaction '
                  'stays on-chain and cannot be deleted. Write something you '
                  'are happy to keep.'),
             ])),

        # ---- The wallet picker modal, as wall-live.js expects it ----------
        '''<div class="modal" id="wallet-modal" role="dialog" aria-modal="true"
     aria-labelledby="wallet-modal-title" hidden>
<div class="modal-card">
<div class="modal-head">
<h2 id="wallet-modal-title">Choose a wallet</h2>
<button type="button" class="vbtn" id="wallet-close" aria-label="Close">Close</button>
</div>
<div class="modal-body" id="wallet-options">
<p class="vlab">Looking for wallets in this browser.</p>
</div>
<div class="modal-foot">
<span class="vlab">Connected</span>
<span id="wallet-address" class="mono-addr">Not connected</span>
<span id="wallet-balance" class="vlab">Balance unknown</span>
</div>
</div>
</div>''',

        cta('Get the badge too.',
            'Certified Lander gives your wallet one permanent ID and a card '
            'you can actually show people.',
            [('Get certified', '/lander/', True),
             ('Back to About', '/about.html', False)]),
    ]),
}


# ============================================================== lander ======

LANDER = {
    'route': '/lander/',
    'title': 'Certified Lander | One Permanent ID Per Wallet',
    'description': 'Swap for LANDING through Jupiter on this page and get one '
                   'permanent Lander ID per wallet and a card you can '
                   'download. Not an NFT. No promised utility.',
    'priority': '0.8',
    'body': ''.join([
        hero(
            title='Proof you <mark>actually landed</mark>.',
            lede='Swap for LANDING through Jupiter right here and the registry '
                 'gives your wallet one permanent Lander ID and a card to '
                 'download. It ends the argument about whether you hold.',
            chips=[('Certified Lander', False), ('One ID per wallet', True)],
            crumbs=[('LANDING', '/'), ('Lander', None)],
            actions=[('Swap and qualify', '#certify', True),
                     ('See the Wall', '/wall.html', False)],
        ),

        # ---- The card. Every id below is read by lander-live.js. ----------
        band('01', 'Card', 'Your card',
             lede='You choose the name. The registry fills in the wallet, the '
                  'balance recorded when the ID was issued, and the ID itself. '
                  'None of it is a live feed.',
             anchor='certify',
             body='''<div class="lander-layout">

<div class="lander-card-area">
<div class="lander-card" id="lander-card" data-certification="preview">
<!-- The turning container is #card-turn, not #card-slot: the project's
     newer lander-live.js writes the confirmed Solana slot number into
     #card-slot, which would have replaced the whole card. -->
<div class="card-slot" id="card-turn">

<!-- Every field below is written by lander-live.js. This markup works with
     both versions of that script: the one on sites-redesign and the newer
     one on main, which adds the slot, issue date, proof and signature
     fields. The starting text is what the newer script expects before a
     card exists. -->
<div class="card-face card-front" id="registered-card-front">
<div class="card-top">
<span class="card-brand">LANDING</span>
<span class="card-state" id="card-state"><i aria-hidden="true"></i> Locked</span>
</div>
<div class="card-main">
<span class="gauge-label">Certified lander</span>
<b class="card-name" id="card-name">LANDER</b>
<span class="card-wallet mono-addr" id="card-wallet">&mdash;</span>
</div>
<div class="card-foot">
<span><i class="gauge-label">Holding</i><b id="card-balance">&mdash; LANDING</b></span>
<span><i class="gauge-label">Lander ID</i><b id="card-id">----</b></span>
<span><i class="gauge-label">Confirmed slot</i><b id="card-slot">&mdash;</b></span>
<span><i class="gauge-label">Issued</i><b id="card-issued">&mdash;</b></span>
</div>
<div class="card-proof">
<span id="card-proof">Finalized swap required</span>
<span id="card-signature">TX &mdash;</span>
</div>
<p class="card-preview" id="card-preview-label">Preview / not issued</p>
</div>

<div class="card-face card-back" id="registered-card-back" hidden>
<div class="card-top">
<span class="card-brand">LANDING</span>
<span class="card-state">Gravity: active</span>
</div>
<div class="card-main">
<span class="gauge-label">Lander ID</span>
<b class="card-name" id="card-back-id" data-mirror="card-id">----</b>
<span class="card-back-proof" id="card-back-proof">On-chain proof required</span>
<p class="card-motto">A holder owns a token.<br>A Lander belongs.</p>
</div>
<p class="card-note" id="card-reverse-note">This card stays locked until the LANDING registry confirms a finalized qualifying swap on Solana.</p>
</div>

</div>
</div>

<!-- Download starts visible and locked, as on the live site. The newer
     script unlocks it itself; for the older one, ui.js unlocks it when the
     card is confirmed. Either script refuses a download without a
     confirmed card. -->
<div class="srcbar" style="justify-content:center;margin-top:var(--space-6)">
<button type="button" class="vbtn" id="live-card-flip" aria-pressed="false">Read the reverse &#8635;</button>
<button type="button" class="vbtn" id="download-card" disabled aria-disabled="true">Download card</button>
</div>
<p class="card-lock-note card-lock-locked">Download unlocks once the registry confirms a finalized swap.</p>
<p class="card-lock-note card-lock-proof"><a id="card-proof-link" target="_blank" rel="noopener noreferrer" hidden>View the verified swap on Solscan <span aria-hidden="true">&#8599;</span></a></p>
</div>

<div class="lander-form" id="certified">
<div class="markbox">
<div class="markbox-head">
<span class="gauge-label">Swap and qualify</span>
<span class="vlab" id="swap-status" role="status" aria-live="polite">Swap here or restore a card. No ID issued yet.</span>
</div>

<label class="field">
<span class="gauge-label">Display name</span>
<input type="text" id="lander-name" maxlength="40" autocomplete="nickname" placeholder="What should the card say?">
</label>

<label class="field">
<span class="gauge-label">Wallet address</span>
<input type="text" id="lander-wallet" placeholder="Returned by the registry" spellcheck="false" readonly>
</label>

<!-- These two are inputs on purpose. lander-live.js reads them with
     .value and writes the verified result back with .value, so as plain
     text elements the read came back undefined and the script threw on
     .trim(). They start empty, with the state in the placeholder, because
     whatever is in the value is treated as data. -->
<div class="field-row">
<label class="vlab" for="lander-balance">Holding</label>
<input class="mono-addr" id="lander-balance" type="text" placeholder="Unknown" readonly>
</div>

<div class="field-row">
<label class="vlab" for="lander-id">Lander ID</label>
<input class="mono-addr" id="lander-id" type="text" placeholder="Not issued" readonly>
</div>

<div class="srcbar" style="margin-top:var(--space-5)">
<button type="button" class="btn btn-go" id="buy-landing" style="min-height:44px;padding:0 var(--space-6);font-size:var(--step--1)">Swap and qualify</button>
<button type="button" class="vbtn" id="restore-card">Restore a card</button>
</div>

<label class="field" style="margin-top:var(--space-4)">
<span class="gauge-label">Restore from wallet address</span>
<input type="text" id="restore-wallet" maxlength="44" autocomplete="off" placeholder="Paste the address the card was issued to" spellcheck="false">
</label>
<p class="card-note" style="margin-top:var(--space-3)">Restoring reads a public registry record. It does not connect a wallet or issue a new ID. A swap on an exchange or in another app does not qualify through this page.</p>
</div>
</div>

</div>''',
             ),

        band('02', 'Safety', 'What qualifying does, exactly.',
             lede='Worth spelling out, because "connect your wallet" is also '
                  'the first sentence of most crypto theft.',
             body=steps([
                 ('You swap through Jupiter', [
                     'The swap opens inside this page with LANDING fixed as '
                     'the output. It is a real transaction from your wallet, '
                     'so check the quote, the fees and any token warnings '
                     'before you approve it. You can lose what you spend.',
                 ]),
                 ('The registry checks it', [
                     'Once the swap is finalized on Solana, the registry '
                     'confirms it and records your LANDING balance at that '
                     'moment. That number is a snapshot, not a live feed.',
                 ]),
                 ('You get one permanent ID', [
                     'One ID per wallet, for good. Come back on any device '
                     'and restore the same card with the wallet address. The '
                     'record is public, so anyone with the address can look '
                     'it up.',
                 ]),
                 ('Nothing else happens', [
                     'No email, no password, no seed phrase, ever. If any '
                     'page, bot or person claiming to be LANDING asks for a '
                     'recovery phrase, it is a theft attempt. There is no '
                     'exception to this and no support case that needs it.',
                 ]),
             ])),

        band('03', 'Badge', 'What it is worth.',
             body=callout([
                 '<b>Nothing, financially.</b> A Certified Lander card is not '
                 'an NFT, it is not tradeable, it does not entitle you to an '
                 'airdrop, and it will never be a claim on anything.',
                 'It is a badge. Anyone offering to buy yours is running a '
                 'different kind of operation.',
             ])),

        cta('Card issued?',
            'Go and put a line on the Wall. It is the other half of the same '
            'idea and it takes ten seconds.',
            [('Leave a mark', '/wall.html', True),
             ('Read the FAQ', '/faq.html', False)]),
    ]),
}


# =========================================================== community ======

COMMUNITY = {
    'route': '/community.html',
    'title': 'LANDING Community | Where Everyone Actually Is',
    'description': 'Discord, Telegram, Reddit and X. What each one is for, '
                   'what gets you removed, and how to spot someone '
                   'impersonating the project.',
    'priority': '0.8',
    'body': ''.join([
        hero(
            title='Four rooms. <mark>Different jobs</mark>.',
            lede='We did not spread across every platform to look bigger. '
                 'Each of these is for something specific, and knowing which '
                 'is which saves you reading all four.',
            chips=[('Community', False), ('Open', True)],
            crumbs=[('LANDING', '/'), ('Community', None)],
        ),

        band('01', 'Rooms', 'Pick the right one.',
             body=panels([
                 ('Day to day', 'Discord',
                  'The main room. Where announcements land first and where '
                  'anyone actually building something ends up.',
                  SOCIAL['Discord']),
                 ('Fast and loud', 'Telegram',
                  'Shorter, quicker, messier. Good for a question you want '
                  'answered in the next few minutes.',
                  SOCIAL['Telegram']),
                 ('Longer form', 'Reddit',
                  'For things worth more than one paragraph. Criticism of the '
                  'project included, and it stays up.',
                  SOCIAL['Reddit']),
                 ('Public face', 'X',
                  'Announcements and the jokes. Lowest signal, highest reach, '
                  'and the account most likely to be impersonated.',
                  SOCIAL['X']),
                 ('Formal', 'LinkedIn',
                  'The company page. Mostly there so the project is findable '
                  'by people who check these things before participating.',
                  SOCIAL['LinkedIn']),
                 ('Direct', 'Email',
                  'contact@landingcoin.fun. Slower than all of the above and '
                  'the right channel for anything that needs a record.',
                  'mailto:contact@landingcoin.fun'),
             ])),

        band('02', 'Rules', 'Short list, applied evenly.',
             lede='Most communities publish rules nobody reads. These are the '
                  'four that actually get used.',
             body=facts([
                 (ICON_NO, 'No price promises, from anyone',
                  'Including from people with a role colour. Nobody here '
                  'knows where it is going, and anyone who says they do is '
                  'either guessing or selling.'),
                 (ICON_NO, 'No DMing people a contract address',
                  'We never do it, so anyone doing it is not us. This is the '
                  'single most common way holders get drained.'),
                 (ICON_CHAT, 'Criticism stays',
                  'Saying the project is going to fail is allowed. It might. '
                  'Deleting that would make every other message worthless.'),
                 (ICON_NO, 'No seed phrases. Not ever, for any reason',
                  'No moderator, admin or support account will ask for one. '
                  'There is no legitimate process that needs it.'),
             ])),

        band('03', 'Safety', 'How to tell it is really us.',
             body=qa([
                 ('We will never message you first', [
                     'Not on Discord, Telegram, X or anywhere else. If an '
                     'account claiming to be the team opens a conversation '
                     'with you, that is the signal, regardless of how '
                     'convincing the profile looks.',
                 ]),
                 ('There is one mint address and it never changes', [
                     f'It is <span style="font-family:var(--font-mono);'
                     f'word-break:break-all;color:var(--accent)">{MINT}</span> '
                     'and it is printed on several pages of this site. There '
                     'is no migration, no v2, and no new contract.',
                 ]),
                 ('Support does not exist as a DM', [
                     'There is no support team that handles wallet problems '
                     'privately. Ask in the open channel, where other people '
                     'can see the answer and correct it if it is wrong.',
                 ]),
                 ('Links on this site are the real ones', [
                     'If you are not sure whether a server or account is '
                     'genuine, come back here and use the link rather than '
                     'the one you were sent.',
                 ]),
             ], open_first=True)),

        cta('Come in, then.',
            'Discord is where most of it happens. The rest is optional.',
            [('Open Discord', SOCIAL['Discord'], True),
             ('Read the FAQ first', '/faq.html', False)]),
    ]),
}
