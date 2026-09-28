/* ── Marketplace: the shared price setter ────────────────────────────────────
 * Upgrades the server-rendered price setter (free/paid modes, preset chips,
 * the live "you receive" line). It never invents a value: everything it writes
 * the server re-validates. Upload, edit-resource, the library shelf and the
 * studio all load this file; only the studio also loads the editor scripts.
 *
 * Exposes `window.NebMarket` so `marketplace_studio*.js` can reuse the helpers
 * without a second copy.
 */
(function () {
  'use strict';

  function readJson(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return null;
    }
  }

  function money(value) {
    var amount = parseFloat(value || 0);
    if (isNaN(amount)) return '0';
    var fixed = Math.round(amount * 100) / 100;
    return (fixed % 1 === 0) ? String(fixed) : fixed.toFixed(2);
  }

  function groupThousands(text) {
    var parts = String(text).split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return parts.join('.');
  }

  /* ── Price setter ──────────────────────────────────────────────────────── */
  function initPriceSetter(root) {
    if (root.dataset.nebPriceReady) return;
    root.dataset.nebPriceReady = '1';

    var modes = root.querySelectorAll('[data-neb-price-mode]');
    var flag = root.querySelector('[data-neb-price-flag]');
    var amountWrap = root.querySelector('[data-neb-price-amount]');
    var field = root.querySelector('[data-neb-price-field]');
    var earnings = root.querySelector('[data-neb-price-earnings]');
    var presets = root.querySelectorAll('[data-neb-price-preset]');
    var commission = parseFloat(root.dataset.commission || '0') || 0;

    function isPaid() {
      var checked = root.querySelector('[data-neb-price-mode]:checked');
      return !!checked && checked.value === 'paid';
    }

    function refresh() {
      var paid = isPaid();
      if (flag) flag.value = paid ? '1' : '0';
      if (amountWrap) amountWrap.hidden = !paid;
      root.classList.toggle('is-unset', paid && !(parseFloat(field && field.value) > 0));
      if (field) field.required = paid;

      var price = parseFloat(field && field.value) || 0;
      if (earnings) {
        if (!paid) {
          earnings.textContent = 'Free for every Nebian.';
        } else if (price > 0) {
          var keeps = price - (price * commission) / 100;
          earnings.textContent =
            'You receive Rs. ' + groupThousands(money(keeps)) +
            ' per sale after the ' + commission + '% platform fee.';
        } else {
          earnings.textContent = '';
        }
      }
      presets.forEach(function (chip) {
        var chosen = paid && parseFloat(chip.dataset.nebPricePreset) === price;
        chip.classList.toggle('is-chosen', !!chosen);
      });
    }

    modes.forEach(function (input) {
      input.addEventListener('change', refresh);
    });

    if (field) {
      field.addEventListener('input', refresh);
    }

    presets.forEach(function (chip) {
      chip.addEventListener('click', function () {
        if (!field) return;
        field.value = chip.dataset.nebPricePreset;
        refresh();
      });
    });

    refresh();
  }

  window.NebMarket = {
    readJson: readJson,
    money: money,
    groupThousands: groupThousands,
    initPriceSetter: initPriceSetter
  };

  function bootPrices(scope) {
    (scope || document).querySelectorAll('[data-neb-price]').forEach(initPriceSetter);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { bootPrices(); });
  } else {
    bootPrices();
  }

  document.body.addEventListener('htmx:afterSwap', function (event) {
    if (!event.detail || !event.detail.target) return;
    bootPrices(event.detail.target);
  });
})();
