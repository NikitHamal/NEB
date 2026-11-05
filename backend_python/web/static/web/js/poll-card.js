/* m3x poll card + comment poll builder.
   Cards are drawn from the poll payload (`data-poll` JSON, same shape as the API), so a vote,
   a retracted vote and a member-added option all re-render from one function.
   Markup hooks: [data-poll] cards, [data-poll-builder] panels, [data-action="toggle-poll-builder"]. */
(function () {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function csrf() {
    if (typeof CSRF_TOKEN !== 'undefined') return CSRF_TOKEN;
    var m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }
  function toast(msg) {
    if (typeof showSnackbar === 'function') showSnackbar(msg);
  }
  function post(url, body, method) {
    return fetch(url, {
      method: method || 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify(body || {})
    }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, status: r.status, data: d }; }); });
  }
  function timeLeft(ms) {
    var s = Math.max(0, Math.floor((ms - Date.now()) / 1000));
    if (s < 60) return 'under a minute left';
    var m = Math.floor(s / 60);
    if (m < 60) return m + ' min left';
    var h = Math.floor(m / 60);
    if (h < 48) return h + ' h left';
    return Math.floor(h / 24) + ' days left';
  }
  function votesText(n) { return n + (n === 1 ? ' vote' : ' votes'); }

  var COMPACT_LIMIT = 4;

  function render(el) {
    var p = el._poll;
    if (!p) return;
    var compact = el.dataset.compact === '1';
    var mcq = p.pollType === 'mcq';
    var expired = !!p.isExpired;
    var showResults = p.hasVoted || expired || el._reveal;
    var picked = el._picked || (el._picked = {});
    var lead = p.leaderId;
    var opts = p.options.slice();
    var hidden = 0;
    if (compact && opts.length > COMPACT_LIMIT && !el._all) { hidden = opts.length - COMPACT_LIMIT; opts = opts.slice(0, COMPACT_LIMIT); }

    var head = '<div class="pc-head">' +
      '<span class="pc-chip"><span class="material-symbols-outlined">' + (mcq ? 'quiz' : 'poll') + '</span>' + (mcq ? 'Quiz' : 'Poll') + '</span>' +
      (p.allowMultiple ? '<span class="pc-chip">Pick several</span>' : '') +
      (p.allowAddOptions ? '<span class="pc-chip">Open options</span>' : '') +
      (expired ? '<span class="pc-chip pc-chip--end">Ended</span>' : (p.expiresAt ? '<span class="pc-chip pc-chip--live">' + esc(timeLeft(p.expiresAt)) + '</span>' : '')) +
      '</div>';
    var q = p.question ? '<h4 class="pc-q">' + esc(p.question) + '</h4>' : '';

    var rows = opts.map(function (o) {
      var pct = p.totalVotes ? Math.round(o.voteCount * 100 / p.totalVotes) : 0;
      var cls = 'pc-opt';
      var mine = !!o.isMine;
      var isPicked = !!picked[o.id];
      if (showResults) { cls += ' is-results'; if (mine) cls += ' is-mine'; if (lead === o.id && !mcq) cls += ' is-lead'; }
      if (isPicked && !p.hasVoted) cls += ' is-picked';
      if (mcq && p.hasVoted) {
        if (o.isCorrect) cls += ' is-correct';
        else if (mine) cls += ' is-wrong';
      }
      var disabled = (p.hasVoted && !p.allowMultiple) || expired ? ' disabled' : '';
      if (p.hasVoted) disabled = ' disabled';
      var indicator = showResults && !(isPicked && !p.hasVoted)
        ? ''
        : '<span class="pc-ind"><span class="material-symbols-outlined">check</span></span>';
      if (showResults && mine && !mcq) indicator = '<span class="pc-ind"><span class="material-symbols-outlined">check</span></span>';
      var mark = '';
      if (mcq && p.hasVoted) mark = o.isCorrect ? '<span class="material-symbols-outlined pc-mark">check_circle</span>' : (mine ? '<span class="material-symbols-outlined pc-mark">cancel</span>' : '');
      return '<li><button type="button" class="' + cls + '" data-pc-opt="' + esc(o.id) + '"' + disabled + '>' +
        (showResults ? '<span class="pc-fill" style="transform:scaleX(' + (pct / 100) + ')"></span>' : '') +
        indicator +
        '<span class="pc-label">' + esc(o.text) + (o.isAdded && !o.addedByMe ? '<span class="pc-added">Added by a member</span>' : (o.addedByMe ? '<span class="pc-added">Added by you</span>' : '')) + '</span>' +
        mark +
        (showResults ? '<span class="pc-votes">' + o.voteCount + '</span><span class="pc-pct">' + pct + '%</span>' : '') +
        '</button></li>';
    }).join('');

    var more = hidden ? '<button type="button" class="pc-btn pc-btn--text" data-pc="all">Show ' + hidden + ' more option' + (hidden > 1 ? 's' : '') + '</button>' : '';

    var add = '';
    if (p.canAddOption && IS_AUTH(el)) {
      add = '<div class="pc-add' + (el._adding ? ' is-open' : '') + '">' +
        '<button type="button" class="pc-add-open" data-pc="add-open"><span class="material-symbols-outlined">add</span>Add option</button>' +
        '<div class="pc-add-form"><input class="pc-add-input" maxlength="100" placeholder="Your option" aria-label="New option">' +
        '<button type="button" class="pc-icon-btn" data-pc="add-send" aria-label="Add option" disabled><span class="material-symbols-outlined">arrow_upward</span></button>' +
        '<button type="button" class="pc-icon-btn pc-icon-btn--ghost" data-pc="add-cancel" aria-label="Cancel"><span class="material-symbols-outlined">close</span></button></div></div>';
    }

    var actions = '';
    var n = Object.keys(picked).length;
    if (!p.hasVoted && !expired) {
      if (p.allowMultiple) actions += '<button type="button" class="pc-btn" data-pc="submit"' + (n ? '' : ' disabled') + '>Vote' + (n ? ' (' + n + ')' : '') + '</button>';
      if (!el._reveal && !compact) actions += '<button type="button" class="pc-btn pc-btn--text" data-pc="reveal">See results</button>';
      if (el._reveal && !p.hasVoted) actions += '<button type="button" class="pc-btn pc-btn--text" data-pc="hide">Hide results</button>';
    }
    if (p.canRetract) actions += '<button type="button" class="pc-btn pc-btn--text" data-pc="retract">Change vote</button>';

    var explain = (mcq && p.hasVoted && p.explanation) ? '<div class="pc-explain">' + esc(p.explanation) + '</div>' : '';
    var foot = '<div class="pc-foot"><span><b>' + votesText(p.totalVotes) + '</b></span>' +
      '<span class="pc-spacer"></span><div class="pc-actions">' + actions + '</div></div>';

    el.className = 'pc' + (compact ? ' pc--compact' : '');
    el.setAttribute('data-multi', p.allowMultiple ? '1' : '0');
    el.innerHTML = head + q + '<ul class="pc-opts">' + rows + '</ul>' + more + explain + add + foot;
    if (el._adding) {
      var inp = el.querySelector('.pc-add-input');
      if (inp) { if (el._addText) inp.value = el._addText; inp.focus(); }
    }
  }

  function IS_AUTH(el) { return el.dataset.auth === '1'; }

  function needLogin(el) {
    var url = el.dataset.loginUrl || '/login/';
    window.location.href = url + '?next=' + encodeURIComponent(location.pathname + location.search);
  }

  function setPoll(el, data) {
    el._poll = data;
    el._picked = {};
    el._adding = false;
    el._addText = '';
    el.classList.remove('is-busy');
    render(el);
  }

  function vote(el, ids) {
    var p = el._poll;
    el.classList.add('is-busy');
    post('/ajax/poll/' + p.id + '/vote/', { option_ids: ids }).then(function (r) {
      el.classList.remove('is-busy');
      if (r.ok) setPoll(el, r.data); else { toast(r.data.error || 'Could not record your vote.'); render(el); }
    }).catch(function () { el.classList.remove('is-busy'); toast('Could not record your vote.'); });
  }

  function onClick(e) {
    var el = e.target.closest('[data-poll]');
    if (!el || !el._poll) return;
    e.stopPropagation();
    var p = el._poll;
    var optBtn = e.target.closest('[data-pc-opt]');
    var act = e.target.closest('[data-pc]');
    if (optBtn) {
      if (!IS_AUTH(el)) return needLogin(el);
      if (p.hasVoted || p.isExpired) return;
      var id = optBtn.getAttribute('data-pc-opt');
      if (p.allowMultiple) {
        if (el._picked[id]) delete el._picked[id]; else el._picked[id] = true;
        render(el);
      } else {
        vote(el, [id]);
      }
      return;
    }
    if (!act) return;
    var a = act.getAttribute('data-pc');
    if (a === 'submit') vote(el, Object.keys(el._picked));
    else if (a === 'reveal') { el._reveal = true; render(el); }
    else if (a === 'hide') { el._reveal = false; render(el); }
    else if (a === 'all') { el._all = true; render(el); }
    else if (a === 'add-open') { if (!IS_AUTH(el)) return needLogin(el); el._adding = true; render(el); }
    else if (a === 'add-cancel') { el._adding = false; el._addText = ''; render(el); }
    else if (a === 'add-send') sendOption(el);
    else if (a === 'retract') {
      el.classList.add('is-busy');
      post('/ajax/poll/' + p.id + '/retract/', {}).then(function (r) {
        if (r.ok) { el._reveal = false; setPoll(el, r.data); } else { el.classList.remove('is-busy'); toast(r.data.error || 'Could not change your vote.'); }
      });
    }
  }

  function sendOption(el) {
    var inp = el.querySelector('.pc-add-input');
    var text = inp ? inp.value.trim() : '';
    if (!text) return;
    el.classList.add('is-busy');
    post('/ajax/poll/' + el._poll.id + '/option/', { text: text, vote: true }).then(function (r) {
      el.classList.remove('is-busy');
      if (r.ok) setPoll(el, r.data); else { el._addText = text; toast(r.data.error || 'Could not add that option.'); render(el); }
    }).catch(function () { el.classList.remove('is-busy'); toast('Could not add that option.'); });
  }

  function onInput(e) {
    var inp = e.target.closest('.pc-add-input');
    if (!inp) return;
    var el = inp.closest('[data-poll]');
    el._addText = inp.value;
    var send = el.querySelector('[data-pc="add-send"]');
    if (send) send.disabled = !inp.value.trim();
  }
  function onKey(e) {
    if (e.key === 'Enter' && e.target.classList && e.target.classList.contains('pc-add-input')) {
      e.preventDefault(); sendOption(e.target.closest('[data-poll]'));
    } else if (e.key === 'Escape' && e.target.classList && e.target.classList.contains('pc-add-input')) {
      var el = e.target.closest('[data-poll]'); el._adding = false; render(el);
    }
  }

  function mount(el) {
    if (el._poll) return;
    try { el._poll = JSON.parse(el.getAttribute('data-poll')); } catch (err) { return; }
    el.removeAttribute('data-poll-pending');
    render(el);
  }
  function mountAll(root) {
    (root || document).querySelectorAll('[data-poll]').forEach(mount);
  }

  document.addEventListener('click', onClick);
  document.addEventListener('input', onInput);
  document.addEventListener('keydown', onKey);
  document.addEventListener('DOMContentLoaded', function () { mountAll(); });
  document.addEventListener('htmx:afterSwap', function (e) { mountAll(e.target); });
  new MutationObserver(function (muts) {
    for (var i = 0; i < muts.length; i++) {
      if (muts[i].addedNodes.length) { mountAll(); return; }
    }
  }).observe(document.documentElement, { childList: true, subtree: true });

  /* ------------------------------------------------------------------ builder */
  var MAX_OPTS = 6;

  function builderRow(value) {
    return '<div class="pb-row"><input class="pb-field" data-pb="opt" maxlength="100" placeholder="Option" value="' + esc(value || '') + '">' +
      '<button type="button" class="pc-icon-btn pc-icon-btn--ghost" data-pb="rm" aria-label="Remove option"><span class="material-symbols-outlined">close</span></button></div>';
  }
  function builderHtml() {
    return '<div class="pb-head"><span class="material-symbols-outlined">poll</span>Poll</div>' +
      '<input class="pb-field" data-pb="q" maxlength="300" placeholder="Ask a question" aria-label="Poll question">' +
      '<div class="pb-opts" data-pb="opts">' + builderRow() + builderRow() + '</div>' +
      '<button type="button" class="pb-opts-add" data-pb="add"><span class="material-symbols-outlined">add</span>Add option</button>' +
      '<label class="pb-sw"><span>Allow several answers</span><input type="checkbox" data-pb="multi"><span class="pb-track"></span></label>' +
      '<label class="pb-sw"><span>Let people add options</span><input type="checkbox" data-pb="open"><span class="pb-track"></span></label>' +
      '<div class="pb-foot"><select class="pb-select" data-pb="dur" aria-label="Poll length">' +
      '<option value="0">No end</option><option value="3600000">1 hour</option><option value="86400000" selected>1 day</option>' +
      '<option value="259200000">3 days</option><option value="604800000">1 week</option></select>' +
      '<button type="button" class="pc-btn pc-btn--text pb-remove" data-pb="close">Remove poll</button></div>';
  }
  function syncAdd(root) {
    var n = root.querySelectorAll('[data-pb="opt"]').length;
    var add = root.querySelector('[data-pb="add"]');
    if (add) add.disabled = n >= MAX_OPTS;
    root.querySelectorAll('[data-pb="rm"]').forEach(function (b) { b.style.visibility = n > 2 ? 'visible' : 'hidden'; });
  }
  function notify(root) {
    root.dispatchEvent(new CustomEvent('pollchange', { bubbles: true }));
  }

  var Builder = {
    root: function (scope) { return scope && scope.querySelector ? scope.querySelector('[data-poll-builder]') : null; },
    open: function (root) {
      if (!root.dataset.ready) { root.innerHTML = builderHtml(); root.dataset.ready = '1'; syncAdd(root); }
      root.classList.add('is-open');
      var q = root.querySelector('[data-pb="q"]'); if (q) q.focus();
      notify(root);
    },
    close: function (root) { root.classList.remove('is-open'); notify(root); },
    reset: function (root) { if (!root) return; root.innerHTML = ''; delete root.dataset.ready; root.classList.remove('is-open'); notify(root); },
    isOpen: function (root) { return !!root && root.classList.contains('is-open'); },
    /* The poll object for the API, or null when the builder is closed. */
    collect: function (root) {
      if (!Builder.isOpen(root)) return null;
      var opts = [].map.call(root.querySelectorAll('[data-pb="opt"]'), function (i) { return i.value.trim(); }).filter(Boolean);
      return {
        question: root.querySelector('[data-pb="q"]').value.trim(),
        options: opts,
        allow_multiple: root.querySelector('[data-pb="multi"]').checked,
        allow_add_options: root.querySelector('[data-pb="open"]').checked,
        duration_ms: parseInt(root.querySelector('[data-pb="dur"]').value, 10) || 0
      };
    },
    valid: function (root) {
      var c = Builder.collect(root);
      return !!c && c.options.length >= 2 && new Set(c.options.map(function (o) { return o.toLowerCase(); })).size === c.options.length;
    }
  };
  window.NebPollBuilder = Builder;

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-action="toggle-poll-builder"]');
    if (t) {
      var scope = t.closest('[data-poll-scope]') || document;
      var root = Builder.root(scope);
      if (root) { Builder.isOpen(root) ? Builder.close(root) : Builder.open(root); t.classList.toggle('is-active', Builder.isOpen(root)); }
      return;
    }
    var b = e.target.closest('[data-pb]');
    if (!b) return;
    var panel = b.closest('[data-poll-builder]');
    if (!panel) return;
    var a = b.getAttribute('data-pb');
    if (a === 'add') {
      var wrap = panel.querySelector('[data-pb="opts"]');
      if (wrap.children.length < MAX_OPTS) {
        wrap.insertAdjacentHTML('beforeend', builderRow());
        wrap.lastElementChild.querySelector('input').focus();
      }
      syncAdd(panel); notify(panel);
    } else if (a === 'rm') {
      var row = b.closest('.pb-row'); if (row) row.remove();
      syncAdd(panel); notify(panel);
    } else if (a === 'close') {
      Builder.reset(panel);
      document.querySelectorAll('[data-action="toggle-poll-builder"].is-active').forEach(function (x) {
        if (x.closest('[data-poll-scope]') === panel.closest('[data-poll-scope]')) x.classList.remove('is-active');
      });
    }
  });
  document.addEventListener('input', function (e) {
    var panel = e.target.closest && e.target.closest('[data-poll-builder]');
    if (panel) notify(panel);
  });
  document.addEventListener('change', function (e) {
    var panel = e.target.closest && e.target.closest('[data-poll-builder]');
    if (panel) notify(panel);
  });
})();
