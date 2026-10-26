/* ==========================================================================
   LANDING: site behaviour

   Four small things, in this order: open every page at the top, copy to
   clipboard, the header's drop panels, and the mobile drawer.

   Motion is handled entirely in CSS through prefers-reduced-motion, so
   there is nothing here that touches animation. This file adds no scroll
   listeners and no observers; the scroll-driven animation is native CSS.
   ========================================================================== */

(function () {
  'use strict';

  var root = document.documentElement;

  /* ---- Start at the top --------------------------------------------------
     Following a link should land you at the top of the new page. Browsers
     usually do that, but they also restore the previous scroll position
     when a page is served from the back/forward cache, which on a fast
     return looks like the new page opened halfway down.

     So: force the top on a normal navigation, and leave back and forward
     alone, because restoring the position is exactly what those should do.
     The hash is also respected, otherwise an in-page link would be undone
     the moment it worked.                                                 */

  function navigationType() {
    try {
      var entry = performance.getEntriesByType('navigation')[0];
      if (entry && entry.type) return entry.type;
      // Older browsers only expose the legacy numeric API.
      if (performance.navigation) {
        return performance.navigation.type === 2 ? 'back_forward' : 'navigate';
      }
    } catch (e) {
      /* fall through to the safe default */
    }
    return 'navigate';
  }

  function startAtTop() {
    if (window.location.hash) return;
    if (navigationType() === 'back_forward') return;
    window.scrollTo(0, 0);
  }

  function bindPageShow() {
    // Restoring from the back/forward cache does not re-run the page, so
    // the check above never sees it. persisted tells us that happened.
    window.addEventListener('pageshow', function (event) {
      if (!event.persisted && !window.location.hash) window.scrollTo(0, 0);
    });
  }

  /* ---- Counters ----------------------------------------------------------
     Numbers that count up are started by an observer when they arrive, and
     run on time rather than being tied to scroll position. Scroll-linked
     counting reads 0 until you reach it and then moves in steps with the
     scroll wheel.

     The count is written here, a frame at a time, rather than done as a
     CSS animation. These counters work by feeding a registered custom
     property into counter-reset, and engines do not agree on whether the
     generated content repaints while that property interpolates: WebKit
     does not, so on an iPhone the number sat at its final value and never
     moved. Setting the property from script is an ordinary style change,
     which every engine repaints.

     The resting value in CSS is the real figure, so if none of this runs,
     the correct number is still what shows.                              */

  var COUNT_MS = 2000;

  function easeOut(t) {
    // Quickly away, gently in. Matches the house curve closely enough that
    // a counter and a panel arriving together feel like one movement.
    return 1 - Math.pow(1 - t, 3);
  }

  function runCount(el) {
    // The resting value is the target: CSS already holds the real figure
    // in --n, which is what the page shows when none of this runs.
    var target = parseInt(
      getComputedStyle(el).getPropertyValue('--n'), 10);

    if (!isFinite(target) || target <= 0) return;
    if (prefersReducedMotion()) return;   // leave the number as it is

    // Take the digits over from CSS. Until this class is added the number
    // comes from counter(), which is the correct no-JavaScript result;
    // from here it is ordinary text, so no engine has to agree with us
    // about when generated content repaints.
    el.classList.add('counted');

    var started = null;

    function frame(now) {
      if (started === null) started = now;
      var progress = Math.min((now - started) / COUNT_MS, 1);
      el.textContent = String(Math.round(easeOut(progress) * target));
      if (progress < 1) {
        window.requestAnimationFrame(frame);
      } else {
        // Land exactly on the real number, never a rounding artefact.
        el.textContent = String(target);
      }
    }

    el.textContent = '0';
    window.requestAnimationFrame(frame);
  }

  function prefersReducedMotion() {
    try {
      return window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (e) {
      return false;
    }
  }

  /* Adds `className` to everything matching `selector` the first time it
     comes into view, then stops watching it. Without IntersectionObserver
     the class is applied immediately, so the thing happens early rather
     than never. */
  function playOnceInView(selector, className, options) {
    var targets = document.querySelectorAll(selector);
    if (!targets.length) return;

    if (!('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(targets, function (el) {
        el.classList.add(className);
      });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add(className);
        observer.unobserve(entry.target);
      });
    }, options);

    Array.prototype.forEach.call(targets, function (el) {
      observer.observe(el);
    });
  }

  /* ---- The touchdown sequence --------------------------------------------
     The lander's descent, the dust burst, the shockwave and the
     confirmation are one synchronised set, driven by scroll position on a
     wide screen. On a phone that reads badly: a thumb flick carries
     momentum, and the browser's address bar collapsing mid-scroll changes
     the viewport height, which moves the range the animation is measured
     against. The lander ends up jumping up and down rather than landing.

     On a phone it plays once, on its own clock, when the scene arrives.  */

  function bindTouchdown() {
    playOnceInView('.scn.mt', 'played',
      { rootMargin: '0px 0px -20% 0px', threshold: 0.1 });
  }

  function bindCounters() {
    var counters = document.querySelectorAll('.c404, .c6, .c50, .cu');
    if (!counters.length) return;

    if (!('IntersectionObserver' in window) ||
        !window.requestAnimationFrame) {
      return;   // the resting values are already correct
    }

    // Firing as soon as a number clears the bottom edge means the count is
    // spent before the card has been read. Shrinking the root's bottom by
    // 42% holds the trigger until the card sits in the upper part of the
    // screen, where the count is watched rather than missed.
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        runCount(entry.target);
      });
    }, { rootMargin: '0px 0px -42% 0px', threshold: 0.2 });

    Array.prototype.forEach.call(counters, function (el) {
      observer.observe(el);
    });
  }

  /* ---- Copy to clipboard -------------------------------------------------
     Any element carrying data-copy copies that value, and reports the
     result in its own label before returning to rest. Contract addresses
     are long and easy to mistype, so a failed copy says so rather than
     silently doing nothing.                                               */

  var RESET_MS = 1800;

  function reportCopy(button, message) {
    if (button.dataset.restingLabel === undefined) {
      button.dataset.restingLabel = button.textContent;
    }
    button.textContent = message;

    window.clearTimeout(button._copyTimer);
    button._copyTimer = window.setTimeout(function () {
      button.textContent = button.dataset.restingLabel;
    }, RESET_MS);
  }

  function copy(button) {
    var value = button.getAttribute('data-copy');
    if (!value) return;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(value).then(
        function () { reportCopy(button, 'Copied'); },
        function () { reportCopy(button, 'Select and copy'); }
      );
      return;
    }

    // No clipboard API, which is the case on insecure origins and in older
    // browsers. Tell the visitor to copy it themselves rather than failing
    // silently and leaving them to wonder whether it worked.
    reportCopy(button, 'Select and copy');
  }

  function bindCopyControls() {
    document.addEventListener('click', function (event) {
      var button = event.target.closest('[data-copy]');
      if (button) copy(button);
    });
  }

  /* ---- Header drop panels ------------------------------------------------
     Four top-level items carry the whole site between them. A panel opens
     on hover for a mouse and on click or Enter for a keyboard, and closes
     on Escape, on a click elsewhere, or when focus leaves the item.
     Pointer and keyboard share one open/close path, so the two can never
     disagree about what is currently open.                                */

  var HOVER_CLOSE_MS = 140;

  function closeItem(item) {
    if (!item) return;
    delete item.dataset.open;
    item._openedByHover = false;
    var button = item.querySelector('.hdr-link');
    if (button) button.setAttribute('aria-expanded', 'false');
  }

  function closeAllItems(except) {
    Array.prototype.forEach.call(
      document.querySelectorAll('.hdr-item'),
      function (item) { if (item !== except) closeItem(item); }
    );
  }

  function openItem(item) {
    closeAllItems(item);
    item.dataset.open = '';
    var button = item.querySelector('.hdr-link');
    if (button) button.setAttribute('aria-expanded', 'true');
  }

  function bindNavPanels() {
    var items = document.querySelectorAll('.hdr-item');
    if (!items.length) return;

    Array.prototype.forEach.call(items, function (item) {
      var button = item.querySelector('.hdr-link');
      if (!button) return;

      button.addEventListener('click', function (event) {
        event.preventDefault();

        // With a mouse, hovering has already opened this panel by the time
        // the click lands. Treating that click as a toggle would shut the
        // panel the moment the visitor reached for it, so the first click
        // after a hover just pins it open; the next one closes it.
        if ('open' in item.dataset) {
          if (item._openedByHover) {
            item._openedByHover = false;
            return;
          }
          closeItem(item);
        } else {
          openItem(item);
        }
      });

      item.addEventListener('mouseenter', function () {
        window.clearTimeout(item._navTimer);
        if (!('open' in item.dataset)) item._openedByHover = true;
        openItem(item);
      });

      item.addEventListener('mouseleave', function () {
        item._navTimer = window.setTimeout(function () {
          closeItem(item);
        }, HOVER_CLOSE_MS);
      });

      // Tabbing past the last link in a panel should close it.
      item.addEventListener('focusout', function (event) {
        if (!item.contains(event.relatedTarget)) closeItem(item);
      });
    });

    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape') return;
      var open = document.querySelector('.hdr-item[data-open]');
      if (!open) return;
      var button = open.querySelector('.hdr-link');
      closeItem(open);
      if (button) button.focus();
    });

    document.addEventListener('click', function (event) {
      if (!event.target.closest('.hdr-item')) closeAllItems();
    });
  }

  /* ---- Mobile drawer -----------------------------------------------------
     Below 900px the nav becomes a full-screen drawer. While it is open the
     page behind it does not scroll, and widening the window past the
     breakpoint closes it, so the two navs are never both live.            */

  var DESKTOP_MIN = 901;

  function setDrawer(open) {
    if (open) root.setAttribute('data-drawer-open', '');
    else root.removeAttribute('data-drawer-open');

    Array.prototype.forEach.call(
      document.querySelectorAll('[data-drawer-toggle]'),
      function (control) {
        control.setAttribute('aria-expanded', String(open));
        control.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      }
    );
  }

  function bindDrawer() {
    var toggles = document.querySelectorAll('[data-drawer-toggle]');
    if (!toggles.length) return;

    Array.prototype.forEach.call(toggles, function (control) {
      control.addEventListener('click', function () {
        setDrawer(!root.hasAttribute('data-drawer-open'));
      });
    });

    // Following a link inside the drawer closes it, which matters on the
    // in-page anchors where no navigation happens to close it for us.
    var drawer = document.getElementById('drawer');
    if (drawer) {
      drawer.addEventListener('click', function (event) {
        if (event.target.closest('a')) setDrawer(false);
      });
    }

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && root.hasAttribute('data-drawer-open')) {
        setDrawer(false);
        var button = document.querySelector('[data-drawer-toggle]');
        if (button) button.focus();
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth >= DESKTOP_MIN) setDrawer(false);
    });
  }

  /* ---- Live readings --------------------------------------------------- */

  /* The Transparency page's figures are fetched and written by the
     project's own site.js, not by this file. It finds each figure by
     [data-reading="<key>"], sets the text, and toggles .unavailable when
     the source returned nothing. That is all it does: it knows nothing
     about the channel around the figure.

     The channel carries the visible state, though: a hunting pulse while
     awaiting, a steady line when live, a flat line when the source is
     silent. So this watches each figure and moves its channel to match
     whatever site.js last wrote. Without it the numbers would arrive while
     every channel went on looking as if it were still waiting.

     The flat line is literal. The design promises that a flat trace means
     the source is not answering, so an unavailable channel swaps its wave
     for a straight line, and gets the wave back if a later refresh
     succeeds. */
  var FLAT_TRACE = 'M0 13 H240';

  function setChannelState(value) {
    var channel = value.closest('.channel');
    if (!channel) return;

    var state = value.classList.contains('unavailable') ? 'unavailable' : 'live';
    if (channel.getAttribute('data-state') === state) return;
    channel.setAttribute('data-state', state);

    var paths = channel.querySelectorAll('.trace path');
    for (var i = 0; i < paths.length; i++) {
      var path = paths[i];
      if (!path.hasAttribute('data-wave')) {
        path.setAttribute('data-wave', path.getAttribute('d'));
      }
      path.setAttribute('d', state === 'unavailable'
        ? FLAT_TRACE : path.getAttribute('data-wave'));
    }
  }

  function bindReadings() {
    var values = document.querySelectorAll('[data-reading]');
    if (!values.length || !('MutationObserver' in window)) return;

    var observer = new MutationObserver(function (records) {
      for (var i = 0; i < records.length; i++) {
        var node = records[i].target;
        var value = node.nodeType === 1 ? node : node.parentElement;
        if (value && value.hasAttribute('data-reading')) setChannelState(value);
      }
    });

    for (var i = 0; i < values.length; i++) {
      observer.observe(values[i], {
        childList: true,
        characterData: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['class']
      });
    }
  }

  /* ---- Off-screen sections ---------------------------------------------- */

  /* The home page runs close to 700 time-based animations at once: stars
     twinkling, dashed lines flowing, craft bobbing, in every scene from the
     hero to the footer. Only one or two sections are ever on screen, but
     the browser keeps ticking all of them, and on a phone that is the
     difference between a smooth scroll and a stuttering one.

     So each top-level block of the page is watched, and while it is well
     outside the viewport its animations are paused (.is-offscreen, in
     base.css). They resume a quarter of a screen before the block scrolls
     in, so nothing is ever seen starting up, and nothing on screen changes
     at all. Scroll-linked animations in a paused block pick up from the
     current scroll position the moment they resume.

     Without IntersectionObserver nothing is paused, which is simply the
     old behaviour.

     The craft on the home page fly on SVG's own animation elements
     (<animateMotion>), not on CSS. Those answer to neither
     prefers-reduced-motion nor animation-play-state, so they used to keep
     moving for visitors who had asked for no motion, and keep running off
     screen. They are driven here through the SVG's own timeline instead:
     paused with their section, and with reduced motion on, frozen at a
     still frame REST_FRAME seconds in, where every craft is mid-path rather
     than parked at a start point. */
  var REDUCE = window.matchMedia
    ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var REST_FRAME = 5;

  function smilRoots(scope) {
    var roots = [];
    var anims = scope.querySelectorAll('animateMotion, animateTransform, animate, set');
    for (var i = 0; i < anims.length; i++) {
      // The timeline belongs to the outermost <svg>, not to a nested one.
      var svg = anims[i].ownerSVGElement;
      while (svg && svg.ownerSVGElement) svg = svg.ownerSVGElement;
      if (svg && roots.indexOf(svg) < 0 && typeof svg.pauseAnimations === 'function') {
        roots.push(svg);
      }
    }
    return roots;
  }

  function setSmil(svg, run) {
    if (REDUCE && REDUCE.matches) {
      svg.setCurrentTime(REST_FRAME);
      svg.pauseAnimations();
    } else if (run) {
      svg.unpauseAnimations();
    } else {
      svg.pauseAnimations();
    }
  }

  function bindOffscreenPause() {
    var main = document.getElementById('main');
    if (!main) return;

    var blocks = [];
    for (var i = 0; i < main.children.length; i++) blocks.push(main.children[i]);
    var roots = blocks.map(smilRoots);
    var onScreen = blocks.map(function () { return true; });

    function apply(n) {
      blocks[n].classList.toggle('is-offscreen', !onScreen[n]);
      for (var j = 0; j < roots[n].length; j++) setSmil(roots[n][j], onScreen[n]);
    }

    // Applied once straight away, so reduced motion freezes the craft even
    // where IntersectionObserver is missing, and again if the setting
    // changes while the page is open.
    for (var k = 0; k < blocks.length; k++) apply(k);
    if (REDUCE && REDUCE.addEventListener) {
      REDUCE.addEventListener('change', function () {
        for (var c = 0; c < blocks.length; c++) apply(c);
      });
    }

    if (!('IntersectionObserver' in window)) return;

    var observer = new IntersectionObserver(function (entries) {
      for (var e = 0; e < entries.length; e++) {
        var n = blocks.indexOf(entries[e].target);
        if (n < 0) continue;
        onScreen[n] = entries[e].isIntersecting;
        apply(n);
      }
    }, { rootMargin: '25% 0px 25% 0px' });

    for (var m = 0; m < blocks.length; m++) observer.observe(blocks[m]);
  }

  /* ---- Mirrored text ----------------------------------------------------
     lander-live.js writes the Lander ID to #card-id only. The back of the
     card shows the same ID, so any element with data-mirror="<id>" copies
     that element's text whenever it changes. */

  function bindMirrors() {
    var copies = document.querySelectorAll('[data-mirror]');
    if (!copies.length || !('MutationObserver' in window)) return;

    Array.prototype.forEach.call(copies, function (copy) {
      var source = document.getElementById(copy.getAttribute('data-mirror'));
      if (!source) return;
      var sync = function () { copy.textContent = source.textContent; };
      sync();
      new MutationObserver(sync).observe(source, {
        childList: true, characterData: true, subtree: true
      });
    });
  }

  /* ---- Lander download lock --------------------------------------------
     Download starts locked. The project's newer lander-live.js unlocks it
     itself once the registry confirms a card. The older version only
     un-hides it, so for that one the button is unlocked here when the card
     is marked confirmed. Both scripts refuse a download without a
     confirmed card, so this never unlocks anything early. */

  function bindLanderUnlock() {
    var card = document.getElementById('lander-card');
    var button = document.getElementById('download-card');
    if (!card || !button || !('MutationObserver' in window)) return;

    // The older script also leaves the proof fields at their placeholders,
    // which would read "Finalized swap required" on a confirmed card. Any
    // field still at its placeholder once the card is confirmed is hidden.
    // The newer script fills them before this runs, so they stay.
    var placeholders = [
      ['card-slot', '\u2014'], ['card-issued', '\u2014'],
      ['card-signature', 'TX \u2014'], ['card-back-proof', 'On-chain proof required']
    ];

    new MutationObserver(function () {
      if (card.getAttribute('data-certification') !== 'confirmed') return;
      if (button.disabled) {
        button.disabled = false;
        button.setAttribute('aria-disabled', 'false');
      }
      placeholders.forEach(function (pair) {
        var field = document.getElementById(pair[0]);
        if (!field || field.textContent.trim() !== pair[1]) return;
        var holder = pair[0] === 'card-signature' ? field.parentNode
          : pair[0] === 'card-back-proof' ? field : field.parentNode;
        holder.hidden = true;
      });
    }).observe(card, { attributes: true, attributeFilter: ['data-certification'] });
  }

  /* ---- Start ------------------------------------------------------------ */

  function init() {
    startAtTop();
    bindPageShow();
    bindCopyControls();
    bindCounters();
    bindTouchdown();
    bindNavPanels();
    bindDrawer();
    bindReadings();
    bindMirrors();
    bindLanderUnlock();
    bindOffscreenPause();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
