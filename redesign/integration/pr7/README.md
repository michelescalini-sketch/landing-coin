# Controlled integration of PR #7

Local branch: `integration/landing-redesign-pr7`.

Base main: `65507832e0711bde023331341ef22b641a4d221e`.
Historic redesign: `f6b9f7662c6f4792750d6f4c55179dac97f2ea61`.
Reviewed PR head: `99754e7859824463df99b382a160e88b1109adf3`.

The integration starts at current main, merges PR #7 locally, selects the
approved redesign presentation and generator, and explicitly reconciles
the newer behavior and tests. Neither production main nor the original PR
is changed remotely. Push, remote merge and deployment remain unauthorized.

## Main behavior retained

- Latest Certified Lander proof validation, disabled download until complete
  registry confirmation, permanent ID, slot, date, signature, restore,
  pending recovery and PNG export. The only controller delta from main wraps
  the verified status text in a span for correct html2canvas layout.
- Wall and Wallet Standard controllers are byte-identical to main. Recipient,
  mint, amount, transaction construction and confirmation behavior survive.
- Transparency/Wall data-rendering code in site.js is byte-identical to main.
  Guards outside that section support the removed legacy header; ui.js owns
  the new drawer and copy controls, traps drawer focus and synchronizes fast
  Transparency responses.
- Card faces retain the physical card ratio and proof fields within the new
  design, including small viewports, long display names and downloaded PNGs.
- Nova's responsibilities and no-custody/signing disclosure, founder contact,
  and all four future collaborator areas survive. Furqan is included with the
  requested new role, superseding main's older removal of his card.
- Backend/Orca sources and production CNAME, robots, .nojekyll and docs README
  are unchanged. No backend or hosting configuration is altered.

## Provenance

- `source-manifest-before.json`: complete manifest before reconciliation.
- `hash-history.json`: old/current SHA-256 values and reasons for each change.
- `main-runtime-inventory.json`: main byte hashes and runtime-section hashes.
- `security-audit.json`: external scripts, public endpoints and static review.
- `redesign/source-manifest.json`: exact integrated docs/generator hashes;
  both CSS fingerprints declared in PR #7 were verified before updating it.

Generator fixes live in site-source and reproduce docs on repeated builds.
Privacy/Cookie wording reflects the two storage keys, public records,
third-party execution, potentially identifiable wallet addresses and the
actual effects of blocked storage. The public essay has Article schema and
is included in sitemap; the three original dated articles remain intact.

## Local verification

Set WEB3_IIFE to @solana/web3.js@1.98.4's index.iife.min.js, and PYTHON_BIN
when Python is not on PATH. Run `npm test` for all offline QA. Browser QA:

```text
node redesign/qa/browser-qa.cjs
node redesign/qa/browser-data-qa.cjs
```

Browser scripts require PLAYWRIGHT_MODULE and, for the six-width suite,
WEB3_IIFE and HTML2CANVAS_FILE (@1.4.1). They intercept external requests;
registry claims and Jupiter success are fixtures, never real operations.

The workflow also accepts PRs into sites-redesign and retains production
settings. It runs the generator and data-state checks in addition to the
existing suites. Remote Actions have not been triggered by this work.

The delivery report records the final commit SHA, exact results, limitations
and working-tree state. This directory contains no wallet or secret material.
