(function () {
  const REGISTRY_URL =
    'https://landing-lander-registry.michelescalini.workers.dev';
  const SOL_MINT =
    'So11111111111111111111111111111111111111112';
  const LANDING_MINT =
    'DLGLMB3imJqnAwKjxY8ZFXoF7CPfTbCNL3j3Ag5M5vGZ';
  const PENDING_SIGNATURE_KEY = 'landing:pending-signature';
  const LANDER_WALLET_KEY = 'landing:lander-wallet';

  const nameInput = document.getElementById('lander-name');
  const balanceInput = document.getElementById('lander-balance');
  const walletInput = document.getElementById('lander-wallet');
  const idInput = document.getElementById('lander-id');

  const cardName = document.getElementById('card-name');
  const cardBalance = document.getElementById('card-balance');
  const cardWallet = document.getElementById('card-wallet');
  const cardId = document.getElementById('card-id');
  const cardSlot = document.getElementById('card-slot');
  const cardIssued = document.getElementById('card-issued');
  const cardSignature = document.getElementById('card-signature');
  const cardState = document.getElementById('card-state');
  const cardProof = document.getElementById('card-proof');
  const cardBackId = document.getElementById('card-back-id');
  const cardBackProof = document.getElementById('card-back-proof');
  const cardReverseNote = document.getElementById('card-reverse-note');
  const proofLink = document.getElementById('card-proof-link');

  const downloadButton = document.getElementById('download-card');
  const buyButton = document.getElementById('buy-landing');
  const swapStatus = document.getElementById('swap-status');
  const card = document.getElementById('lander-card');

  let jupiterInitialized = false;
  let verificationInProgress = false;
  let confirmedLander = null;

  function setStatus(message, state) {
    swapStatus.textContent = message;
    swapStatus.dataset.state = state || 'idle';
  }

  function wait(milliseconds) {
    return new Promise(function (resolve) {
      window.setTimeout(resolve, milliseconds);
    });
  }

  function shortenWallet(value) {
    const wallet = value.trim();

    if (!wallet) return '—';
    if (wallet.length <= 12) return wallet;

    return wallet.slice(0, 4) + '...' + wallet.slice(-4);
  }

  function shortenSignature(value) {
    if (!value) return 'TX —';
    if (value.length <= 18) return 'TX ' + value;
    return 'TX ' + value.slice(0, 6) + '...' + value.slice(-6);
  }

  function formatBalance(value) {
    if (!value) return '— LANDING';

    const amount = Number(value);

    if (!Number.isFinite(amount)) return '— LANDING';

    return new Intl.NumberFormat('en-US', {
      maximumFractionDigits: 6
    }).format(amount) + ' LANDING';
  }

  function rawLandingToDecimal(rawValue) {
    try {
      const raw = BigInt(rawValue);
      const base = 1000000n;
      const whole = raw / base;
      const fraction = (raw % base)
        .toString()
        .padStart(6, '0')
        .replace(/0+$/, '');

      return fraction ? whole.toString() + '.' + fraction : whole.toString();
    } catch (error) {
      return '';
    }
  }

  function formatLanderId(value) {
    const id = Number(value);

    if (!Number.isInteger(id) || id < 1) return '';

    return String(id).padStart(4, '0');
  }

  function formatIssuedDate(value) {
    if (typeof value !== 'string' || !value.trim()) return '';

    const normalized =
      /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(value.trim())
        ? value.trim().replace(' ', 'T') + 'Z'
        : value.trim();
    const date = new Date(normalized);

    if (Number.isNaN(date.getTime())) return '';

    return new Intl.DateTimeFormat('en-GB', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      timeZone: 'UTC'
    }).format(date).toUpperCase();
  }

  function normalizeConfirmedLander(lander) {
    const id = formatLanderId(lander && lander.id);
    const wallet = lander && typeof lander.wallet === 'string'
      ? lander.wallet.trim()
      : '';
    const signature = lander && typeof lander.signature === 'string'
      ? lander.signature.trim()
      : '';
    const balanceRaw = lander && typeof lander.balanceRaw === 'string'
      ? lander.balanceRaw
      : '';
    const balance = rawLandingToDecimal(balanceRaw);
    const confirmedSlot = Number(lander && lander.confirmedSlot);
    const createdAt = lander && typeof lander.createdAt === 'string'
      ? lander.createdAt
      : '';
    const issued = formatIssuedDate(createdAt);

    if (
      !id ||
      !/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(wallet) ||
      !/^[1-9A-HJ-NP-Za-km-z]{64,100}$/.test(signature) ||
      !/^\d+$/.test(balanceRaw) ||
      BigInt(balanceRaw) <= 0n ||
      !balance ||
      !Number.isInteger(confirmedSlot) ||
      confirmedSlot < 1 ||
      !issued
    ) {
      throw new Error('The registry returned incomplete on-chain Lander proof.');
    }

    return Object.freeze({
      id: id,
      wallet: wallet,
      signature: signature,
      balanceRaw: balanceRaw,
      balance: balance,
      confirmedSlot: confirmedSlot,
      createdAt: createdAt,
      issued: issued
    });
  }

  function updateCard() {
    cardName.textContent =
      nameInput.value.trim() || 'LANDER';

    cardBalance.textContent =
      formatBalance(balanceInput.value);

    cardWallet.textContent =
      shortenWallet(walletInput.value);

    const id = idInput.value.trim();

    cardId.textContent =
      id ? id.replace(/^#+/, '') : '----';

    cardBackId.textContent = cardId.textContent;
  }

  function setDownloadUnlocked(unlocked) {
    downloadButton.disabled = !unlocked;
    downloadButton.setAttribute('aria-disabled', String(!unlocked));
    downloadButton.title = unlocked
      ? 'Download your registry-confirmed Certified Lander card'
      : 'A finalized qualifying LANDING swap must be confirmed on-chain first';
  }

  nameInput.addEventListener('input', updateCard);
  setDownloadUnlocked(false);

  function applyLander(lander) {
    const proof = normalizeConfirmedLander(lander);
    confirmedLander = proof;

    balanceInput.value = proof.balance;
    walletInput.value = proof.wallet;
    idInput.value = proof.id;

    card.dataset.certification = 'confirmed';
    cardState.innerHTML = '<i aria-hidden="true"></i><span>ON-CHAIN VERIFIED</span>';
    cardProof.textContent = 'FINALIZED / REGISTRY CONFIRMED';
    cardSignature.textContent = shortenSignature(proof.signature);
    cardSlot.textContent = new Intl.NumberFormat('en-US').format(proof.confirmedSlot);
    cardIssued.textContent = proof.issued;
    cardBackProof.textContent = 'FINALIZED SOLANA SWAP';
    cardReverseNote.textContent =
      'Registry-issued permanent ID backed by a finalized qualifying Jupiter swap on Solana. Balance shown on the front is the recorded balance at issuance.';

    proofLink.href =
      'https://solscan.io/tx/' + encodeURIComponent(proof.signature);
    proofLink.hidden = false;

    setDownloadUnlocked(true);
    localStorage.setItem(LANDER_WALLET_KEY, proof.wallet);
    localStorage.removeItem(PENDING_SIGNATURE_KEY);
    updateCard();
    setStatus(
      'Confirmed on-chain. Certified Lander ' + proof.id + ' is unlocked.',
      'success'
    );
  }

  async function verifyAndClaim(signature) {
    if (verificationInProgress) return;

    verificationInProgress = true;
    buyButton.disabled = true;
    localStorage.setItem(PENDING_SIGNATURE_KEY, signature);
    setStatus('Waiting for finalized on-chain confirmation…', 'waiting');

    try {
      for (let attempt = 1; attempt <= 60; attempt += 1) {
        try {
          const response = await fetch(REGISTRY_URL + '/api/claim', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ signature: signature }),
            cache: 'no-store'
          });
          const payload = await response.json();

          if (payload.status === 'confirmed' && payload.lander) {
            applyLander(payload.lander);
            document.getElementById('certified').scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
            return;
          }

          if (payload.status === 'invalid') {
            localStorage.removeItem(PENDING_SIGNATURE_KEY);
            throw new Error(payload.message || 'The swap could not be verified.');
          }

          if (payload.status !== 'waiting') {
            throw new Error(
              payload.message || 'The registry is temporarily unavailable.'
            );
          }

          setStatus(
            payload.message ||
              'Waiting for finalized on-chain confirmation…',
            'waiting'
          );
        } catch (error) {
          if (
            attempt === 60 ||
            (error instanceof Error &&
              /could not be verified|failed on-chain|did not deliver|not a finalized Jupiter/i.test(
                error.message
              ))
          ) {
            throw error;
          }

          setStatus(
            'Network check in progress. Waiting for confirmation…',
            'waiting'
          );
        }

        await wait(3000);
      }

      throw new Error(
        'Confirmation is taking longer than expected. Reload this page to continue.'
      );
    } catch (error) {
      console.error('Unable to verify LANDING swap:', error);
      setStatus(
        error instanceof Error
          ? error.message
          : 'Unable to verify the swap. Please try again.',
        'error'
      );
    } finally {
      verificationInProgress = false;
      buyButton.disabled = false;
    }
  }

  async function restoreLander() {
    const pendingSignature = localStorage.getItem(PENDING_SIGNATURE_KEY);

    if (pendingSignature) {
      verifyAndClaim(pendingSignature);
      return;
    }

    const savedWallet = localStorage.getItem(LANDER_WALLET_KEY);
    if (!savedWallet) return;

    try {
      const response = await fetch(
        REGISTRY_URL +
          '/api/lander?wallet=' +
          encodeURIComponent(savedWallet),
        { cache: 'no-store' }
      );
      const payload = await response.json();

      if (payload.status === 'confirmed' && payload.lander) {
        applyLander(payload.lander);
      }
    } catch (error) {
      console.warn(
        'Unable to restore the saved Lander card:',
        error
      );
    }
  }

  async function waitForJupiter() {
    for (let attempt = 0; attempt < 100; attempt += 1) {
      if (
        window.Jupiter &&
        typeof window.Jupiter.init === 'function'
      ) {
        return;
      }

      await wait(100);
    }

    throw new Error(
      'Jupiter did not load. Please refresh the page and try again.'
    );
  }

  buyButton.addEventListener('click', async function () {
    try {
      buyButton.disabled = true;
      setStatus('Loading the Jupiter swap…', 'waiting');
      await waitForJupiter();

      if (jupiterInitialized) {
        window.Jupiter.resume();
      } else {
        window.Jupiter.init({
          displayMode: 'modal',
          formProps: {
            initialInputMint: SOL_MINT,
            initialOutputMint: LANDING_MINT,
            fixedMint: LANDING_MINT
          },
          onSuccess: function (result) {
            if (!result || !result.txid) {
              setStatus(
                'The transaction signature was not returned.',
                'error'
              );
              return;
            }

            try {
              window.Jupiter.close();
            } catch (error) {
              console.warn(
                'Unable to close the Jupiter modal:',
                error
              );
            }

            verifyAndClaim(result.txid);
          },
          onSwapError: function () {
            setStatus(
              'Swap not completed. Your card remains locked until on-chain confirmation.',
              'error'
            );
          }
        });

        jupiterInitialized = true;
      }
    } catch (error) {
      console.error('Unable to open Jupiter:', error);
      setStatus(
        error instanceof Error
          ? error.message
          : 'Unable to open Jupiter. Please try again.',
        'error'
      );
    } finally {
      if (!verificationInProgress) buyButton.disabled = false;
    }
  });

  downloadButton.addEventListener('click', async function () {
    if (
      !confirmedLander ||
      card.dataset.certification !== 'confirmed'
    ) {
      setDownloadUnlocked(false);
      setStatus(
        'Download remains locked until the registry confirms a finalized qualifying swap on-chain.',
        'error'
      );
      return;
    }

    const originalText = downloadButton.textContent;
    const front = document.getElementById('registered-card-front');
    const back = document.getElementById('registered-card-back');
    const wasBack = front.hidden;

    front.hidden = false;
    back.hidden = true;

    try {
      downloadButton.disabled = true;
      downloadButton.textContent = 'Creating PNG...';

      const canvas = await html2canvas(front, {
        scale: 3,
        backgroundColor: null,
        useCORS: true
      });

      const link = document.createElement('a');
      const holder =
        (nameInput.value.trim() || 'lander')
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-+|-+$/g, '');

      link.download =
        'certified-lander-' +
        confirmedLander.id +
        '-' +
        (holder || 'card') +
        '.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
    } catch (error) {
      console.error('Unable to create card image:', error);
      alert('Unable to create the image. Please try again.');
    } finally {
      setDownloadUnlocked(Boolean(confirmedLander));
      downloadButton.textContent = originalText;
      front.hidden = wasBack;
      back.hidden = !wasBack;
    }
  });

  const restoreButton = document.getElementById('restore-card');

  restoreButton.addEventListener('click', async function () {
    if (verificationInProgress) return;

    const wallet =
      document.getElementById('restore-wallet').value.trim();

    if (!/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(wallet)) {
      setStatus(
        'Enter a valid Solana wallet address to look up its existing registry card.',
        'error'
      );
      return;
    }

    restoreButton.disabled = true;

    try {
      const response = await fetch(
        REGISTRY_URL +
          '/api/lander?wallet=' +
          encodeURIComponent(wallet),
        {
          cache: 'no-store',
          signal: AbortSignal.timeout(30000)
        }
      );
      const payload = await response.json();

      if (
        response.ok &&
        payload.status === 'confirmed' &&
        payload.lander &&
        payload.lander.wallet === wallet
      ) {
        applyLander(payload.lander);
        setStatus(
          'Existing registry-confirmed card restored. Its qualifying swap was finalized on-chain.',
          'success'
        );
      } else if (
        response.status === 404 ||
        payload.status === 'not_found'
      ) {
        setStatus(
          'No registered Lander card was found for this wallet. No ID has been issued here.',
          'idle'
        );
      } else {
        throw new Error(
          payload.message ||
            'The registry could not be reached. Try again.'
        );
      }
    } catch (error) {
      setStatus(
        error instanceof Error
          ? error.message
          : 'Unable to restore the card.',
        'error'
      );
    } finally {
      restoreButton.disabled = false;
    }
  });

  const flip = document.getElementById('live-card-flip');

  flip.addEventListener('click', function () {
    const back =
      flip.getAttribute('aria-pressed') !== 'true';

    flip.setAttribute('aria-pressed', String(back));
    document.getElementById('registered-card-front').hidden = back;
    document.getElementById('registered-card-back').hidden = !back;
    flip.textContent =
      back ? 'Show the front ↻' : 'Read the reverse ↻';
  });

  updateCard();
  restoreLander();
})();
