/* Reply labels. The author of a discussion (or an admin) says how a reply landed:
   accepted answer, correct, partly correct, incorrect, helpful, spam.

   Markup contract, so server-rendered and script-rendered replies share one path:
     [data-reply-card="<id>"]            the reply's card; carries data-label="<key>"
     [data-reply-tags="<id>"]            where the kind and label chips live
     [data-fl-open="<id>"]               a control that opens the picker
   Everything else is derived from the label meta embedded in the page. */
(function () {
  'use strict';

  var meta = { kinds: [], labels: [] };
  try {
    var node = document.getElementById('forum-label-meta');
    if (node) meta = JSON.parse(node.textContent);
  } catch (e) { /* the page still works without chips */ }

  function byKey(list, key) {
    for (var i = 0; i < list.length; i++) if (list[i].key === key) return list[i];
    return null;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function csrf() {
    var m = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    if (m) return decodeURIComponent(m[1]);
    return typeof window.CSRF_TOKEN === 'string' ? window.CSRF_TOKEN : '';
  }

  function chip(cls, icon, label) {
    return '<span class="fl-chip ' + cls + '"><span class="material-symbols-outlined" aria-hidden="true">' +
      esc(icon) + '</span>' + esc(label) + '</span>';
  }

  function tagsHTML(reply) {
    var out = '';
    var k = reply.kind && reply.kind !== 'comment' ? byKey(meta.kinds, reply.kind) : null;
    if (k) out += chip('fl-kind-chip fl-kind-' + k.key, k.icon, k.label);
    var l = reply.label ? byKey(meta.labels, reply.label) : null;
    if (l) out += chip('fl-label-chip fl-tone-' + l.tone, l.icon, l.label);
    return out;
  }

  function cards(id) {
    var sel = '[data-reply-card="' + (window.CSS && CSS.escape ? CSS.escape(id) : id) + '"]';
    return Array.prototype.slice.call(document.querySelectorAll(sel));
  }

  function paint(id, label) {
    cards(id).forEach(function (c) {
      c.setAttribute('data-label', label || '');
      c.classList.toggle('is-accepted', label === 'accepted');
      c.classList.toggle('is-spam', label === 'spam');
      c.classList.toggle('is-incorrect', label === 'incorrect');
      var tags = c.querySelector('[data-reply-tags]');
      if (tags) {
        tags.innerHTML = tagsHTML({ kind: c.getAttribute('data-kind') || 'comment', label: label });
        tags.hidden = !tags.innerHTML;
      }
      var opener = c.querySelector('[data-fl-open]');
      if (opener) opener.classList.toggle('is-set', !!label);
    });
  }

  function setSolved(resolved) {
    document.querySelectorAll('[data-solved-chip]').forEach(function (n) { n.hidden = !resolved; });
    var page = document.querySelector('.fp-center-panel, #replies-section');
    if (page) page.classList.toggle('is-solved', !!resolved);
  }

  function toast(msg) {
    if (typeof window.showSnackbar === 'function') window.showSnackbar(msg);
  }

  var scrim = null, current = null;

  function build() {
    if (scrim) return scrim;
    scrim = document.createElement('div');
    scrim.className = 'neb-scrim';
    scrim.id = 'labelDialog';
    scrim.hidden = true;
    scrim.innerHTML =
      '<div class="neb-dialog fl-dialog" role="dialog" aria-modal="true" aria-labelledby="flTitle">' +
        '<div class="neb-dialog-head"><h2 class="neb-dialog-title" id="flTitle">Mark this reply</h2></div>' +
        '<div class="fl-options" role="radiogroup" aria-labelledby="flTitle">' +
          meta.labels.map(function (l) {
            return '<button type="button" class="fl-option fl-tone-' + l.tone + '" role="radio" aria-checked="false" data-label="' + l.key + '">' +
              '<span class="fl-option-icon"><span class="material-symbols-outlined" aria-hidden="true">' + esc(l.icon) + '</span></span>' +
              '<span class="fl-option-text"><b>' + esc(l.label) + '</b><small>' + esc(l.hint) + '</small></span>' +
              '<span class="fl-option-check material-symbols-outlined" aria-hidden="true">check</span>' +
            '</button>';
          }).join('') +
        '</div>' +
        '<div class="neb-dialog-actions">' +
          '<button type="button" class="md-btn md-btn-text" data-fl-clear>Remove label</button>' +
          '<button type="button" class="md-btn md-btn-tonal" data-neb-close>Close</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(scrim);
    scrim.addEventListener('click', function (e) {
      if (e.target === scrim) { close(); return; }
      var opt = e.target.closest('.fl-option');
      if (opt) { choose(opt.getAttribute('data-label') === current.label ? '' : opt.getAttribute('data-label')); return; }
      if (e.target.closest('[data-fl-clear]')) choose('');
      else if (e.target.closest('[data-neb-close]')) close();
    });
    return scrim;
  }

  function close() {
    if (window.NebUI) window.NebUI.close(scrim);
    else scrim.hidden = true;
  }

  function open(id) {
    var c = cards(id)[0];
    if (!c) return;
    build();
    current = { id: id, label: c.getAttribute('data-label') || '' };
    scrim.querySelectorAll('.fl-option').forEach(function (o) {
      o.setAttribute('aria-checked', String(o.getAttribute('data-label') === current.label));
    });
    scrim.querySelector('[data-fl-clear]').hidden = !current.label;
    if (window.NebUI) window.NebUI.open(scrim);
    else scrim.hidden = false;
  }

  function choose(label) {
    var target = current;
    scrim.classList.add('is-busy');
    fetch('/ajax/reply/' + encodeURIComponent(target.id) + '/label/', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ label: label })
    }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (res) {
        scrim.classList.remove('is-busy');
        if (!res.ok) { toast(res.d.error || 'Could not update the label.'); return; }
        document.querySelectorAll('[data-reply-card].is-accepted').forEach(function (c) {
          if (c.getAttribute('data-reply-card') !== target.id) paint(c.getAttribute('data-reply-card'), '');
        });
        var hadAccepted = !!document.querySelector('[data-reply-card].is-accepted');
        paint(target.id, res.d.label);
        setSolved(res.d.postResolved);
        close();
        if ((res.d.label === 'accepted' || (current.label === 'accepted' && hadAccepted)) && typeof window.refreshReplies === 'function') {
          window.refreshReplies(target.id, false);
        }
        var info = res.d.labelInfo;
        toast(info ? 'Marked as ' + info.label.toLowerCase() : 'Label removed');
      })
      .catch(function () {
        scrim.classList.remove('is-busy');
        toast('Could not update the label.');
      });
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-fl-open]');
    if (!btn) return;
    e.preventDefault();
    open(btn.getAttribute('data-fl-open'));
  });

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-fl-reveal]');
    if (!t) return;
    var c = t.closest('[data-reply-card]');
    if (c) c.classList.add('is-revealed');
  });

  document.addEventListener('click', function (e) {
    var chip = e.target.closest('[data-solved-chip]');
    if (!chip) return;
    var card = document.querySelector('[data-reply-card].is-accepted');
    if (!card) return;
    card.scrollIntoView({ block: 'center', behavior: 'smooth' });
    card.classList.add('is-fresh');
    setTimeout(function () { card.classList.remove('is-fresh'); }, 2400);
  });

  window.ForumLabels = { meta: meta, tagsHTML: tagsHTML, open: open, paint: paint };
})();
