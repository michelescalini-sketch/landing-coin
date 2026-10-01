const menuButton = document.querySelector('.menu-toggle');
const navigation = document.getElementById('navigation');
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
navigation.addEventListener('click', event => {
  if (event.target.closest('a')) {
    menuButton.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
  }
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    menuButton.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
    menuButton.focus();
  }
});
document.querySelector('[data-copy]')?.addEventListener('click', async event => {
  const button = event.currentTarget;
  const label = button.querySelector('span');
  const status = document.getElementById('copy-status');
  const address = document.getElementById('contract-address').textContent.trim();
  try {
    if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText(address);
    label.textContent = 'Copied';
    status.textContent = 'Contract address copied.';
    setTimeout(() => { label.textContent = 'Copy'; }, 2500);
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(document.getElementById('contract-address'));
    selection.removeAllRanges();
    selection.addRange(range);
    label.textContent = 'Select';
    status.textContent = 'Address selected. Use your device’s copy command.';
    setTimeout(() => { label.textContent = 'Copy'; }, 3500);
  }
});
document.querySelectorAll('[data-copy-value]').forEach(button => {
  button.addEventListener('click', async () => {
    const original = button.textContent;
    try {
      await navigator.clipboard.writeText(button.dataset.copyValue);
      button.textContent = 'Copied';
      button.setAttribute('aria-label', 'Address copied');
    } catch {
      const code = button.previousElementSibling;
      if (code) {
        const range = document.createRange();
        range.selectNodeContents(code);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
      }
      button.textContent = 'Selected';
      button.setAttribute('aria-label', 'Address selected. Use your device’s copy command.');
    }
    setTimeout(() => {
      button.textContent = original;
      button.setAttribute('aria-label', 'Copy address');
    }, 2500);
  });
});
