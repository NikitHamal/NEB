(function () {
  function readJson(id, fallback) {
    var el = document.getElementById(id);
    if (!el) return fallback;
    try { return JSON.parse(el.textContent); } catch (e) { return fallback; }
  }

  var ownedList = readJson('store-owned-ids', []);
  var equipped = readJson('store-equipped', {}) || {};
  var points = readJson('store-points', null);
  var isAuthed = readJson('store-authed', false) === true;
  var owned = {};
  (ownedList || []).forEach(function (id) { owned[id] = true; });

  var pendingConfirm = null;
  var tryState = null;

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : '';
  }

  function csrfToken() {
    return getCookie('csrftoken') || (typeof CSRF_TOKEN !== 'undefined' ? CSRF_TOKEN : '');
  }

  function toast(msg) {
    if (typeof showSnackbar === 'function') { showSnackbar(msg); return; }
    var el = document.createElement('div');
    el.className = 'store-toast';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(function () { el.remove(); }, 3200);
  }

  function postJson(url, body) {
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken() },
      credentials: 'same-origin',
      body: JSON.stringify(body)
    }).then(function (resp) {
      return resp.json().catch(function () { return {}; }).then(function (data) {
        return { ok: resp.ok && data && data.ok === true, data: data || {} };
      });
    });
  }

  function allCards() {
    return Array.prototype.slice.call(document.querySelectorAll('.store-card'));
  }

  function cardById(id) {
    return allCards().filter(function (c) { return c.dataset.itemId === id; })[0] || null;
  }

  function setBalance(value) {
    if (value == null || isNaN(value)) return;
    points = Math.max(0, parseInt(value, 10));
    var el = document.getElementById('store-balance-value');
    if (el) el.textContent = points;
  }

  function renderButton(card) {
    if (!isAuthed || !card) return;
    var btn = card.querySelector('.store-action-btn');
    if (!btn || btn.tagName !== 'BUTTON') return;
    var id = card.dataset.itemId;
    var type = card.dataset.itemType;
    var price = parseInt(card.dataset.price, 10) || 0;
    var isOwned = owned[id] === true;
    var isEquipped = (equipped[type] || '') === id;
    card.classList.toggle('is-owned', isOwned);
    card.classList.toggle('is-equipped-card', isEquipped);
    btn.disabled = false;
    btn.classList.remove('is-confirm', 'is-equipped');
    btn.title = '';
    if (pendingConfirm && pendingConfirm.id === id) {
      btn.textContent = 'Confirm ' + price + ' pts?';
      btn.classList.add('is-confirm');
      return;
    }
    if (!isOwned) {
      if (price > 0) {
        btn.textContent = 'Buy · ' + price + ' pts';
        if (points != null && points < price) {
          btn.disabled = true;
          btn.title = 'Not enough points';
        }
      } else {
        btn.textContent = 'Claim';
      }
      return;
    }
    if (isEquipped) {
      btn.textContent = 'Equipped ✓';
      btn.classList.add('is-equipped');
    } else {
      btn.textContent = 'Equip';
    }
  }

  function refreshAll() {
    allCards().forEach(renderButton);
  }

  function pulse(card) {
    if (!card) return;
    card.classList.remove('store-pulse');
    void card.offsetWidth;
    card.classList.add('store-pulse');
    setTimeout(function () { card.classList.remove('store-pulse'); }, 900);
  }

  function clearConfirm() {
    if (!pendingConfirm) return;
    clearTimeout(pendingConfirm.timer);
    var prevId = pendingConfirm.id;
    pendingConfirm = null;
    renderButton(cardById(prevId));
  }

  function startConfirm(card) {
    clearConfirm();
    pendingConfirm = {
      id: card.dataset.itemId,
      timer: setTimeout(clearConfirm, 4000)
    };
    renderButton(card);
  }

  function setBusy(card, busy) {
    var btn = card.querySelector('.store-action-btn');
    if (!btn || btn.tagName !== 'BUTTON') return;
    if (busy) {
      btn.disabled = true;
      btn.dataset.busy = '1';
      btn.textContent = '…';
    } else {
      delete btn.dataset.busy;
      renderButton(card);
    }
  }

  function applyEquippedTheme() {
    var html = document.documentElement;
    if (equipped.theme) html.setAttribute('data-app-theme', equipped.theme);
    else html.removeAttribute('data-app-theme');
  }

  function endTry() {
    if (!tryState) return;
    clearInterval(tryState.interval);
    var btn = tryState.btn;
    tryState = null;
    if (btn) {
      btn.classList.remove('trying');
      var lbl = btn.querySelector('.store-try-label');
      if (lbl) lbl.textContent = 'Try';
    }
    applyEquippedTheme();
  }

  function updateTryLabel() {
    if (!tryState || !tryState.btn) return;
    var lbl = tryState.btn.querySelector('.store-try-label');
    if (lbl) lbl.textContent = tryState.remaining + 's';
  }

  function tryTheme(btn) {
    var id = btn.dataset.themeId;
    if (tryState && tryState.id === id) { endTry(); return; }
    endTry();
    tryState = { id: id, btn: btn, remaining: 8, interval: null };
    document.documentElement.setAttribute('data-app-theme', id);
    btn.classList.add('trying');
    updateTryLabel();
    tryState.interval = setInterval(function () {
      if (!tryState) return;
      tryState.remaining -= 1;
      if (tryState.remaining <= 0) endTry();
      else updateTryLabel();
    }, 1000);
  }

  function purchase(card) {
    var id = card.dataset.itemId;
    var name = card.dataset.itemName || 'Item';
    clearConfirm();
    setBusy(card, true);
    postJson('/ajax/store/purchase/', { item_id: id }).then(function (res) {
      setBusy(card, false);
      if (!res.ok) {
        toast(res.data.error || 'Purchase failed. Please try again.');
        return;
      }
      owned[id] = true;
      setBalance(res.data.points_balance);
      refreshAll();
      pulse(card);
      toast(name + ' added to your collection');
    }).catch(function () {
      setBusy(card, false);
      toast('Network error. Please try again.');
    });
  }

  function equip(card, unequip) {
    var id = card.dataset.itemId;
    var type = card.dataset.itemType;
    var body = unequip ? { item_type: type, item_id: '' } : { item_id: id };
    setBusy(card, true);
    postJson('/ajax/store/equip/', body).then(function (res) {
      setBusy(card, false);
      if (!res.ok) {
        toast(res.data.error || 'Could not update. Please try again.');
        return;
      }
      equipped = res.data.equipped || equipped;
      if (tryState) endTry();
      else applyEquippedTheme();
      refreshAll();
      if (!unequip) pulse(card);
    }).catch(function () {
      setBusy(card, false);
      toast('Network error. Please try again.');
    });
  }

  function handleAction(btn) {
    if (btn.disabled || btn.dataset.busy) return;
    var card = btn.closest('.store-card');
    if (!card) return;
    var id = card.dataset.itemId;
    var type = card.dataset.itemType;
    var price = parseInt(card.dataset.price, 10) || 0;
    if (!owned[id]) {
      if (price > 0 && !(pendingConfirm && pendingConfirm.id === id)) {
        startConfirm(card);
        return;
      }
      purchase(card);
      return;
    }
    var isEquipped = (equipped[type] || '') === id;
    equip(card, isEquipped);
  }

  function switchTab(btn) {
    var tab = btn.dataset.tab;
    document.querySelectorAll('.store-tab').forEach(function (t) {
      var active = t === btn;
      t.classList.toggle('active', active);
      t.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    document.querySelectorAll('.store-panel').forEach(function (p) {
      p.hidden = p.dataset.panel !== tab;
    });
  }

  if (typeof registerActions === 'function') {
    registerActions({
      'store-tab': function (el) { switchTab(el); },
      'store-try-theme': function (el) { tryTheme(el); },
      'store-card-action': function (el) { handleAction(el); }
    });
  }

  refreshAll();
})();
