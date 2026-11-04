/* ForumEdit: edit a post or a reply where it is read.
 *
 * No dialog. The card's own content steps aside and an editor takes its place,
 * with the same writing tools a new reply gets (ForumComposer), the attachment
 * tray (NebAttach: add, replace, remove, drag to reorder) and Save / Cancel.
 * When it saves, the card is repainted from the server's markup, which stays the
 * single source of what a post looks like.
 *
 *   ForumEdit.post(postId)      host: [data-post-view]
 *   ForumEdit.reply(replyId)    host: #reply-card-<id> or .fp-thread-reply[data-reply-id]
 *
 * Markup contract (forum_post.html, _forum_post_replies.html):
 *   [data-post-view]   data-post-id, data-images='[url..]', data-media='[{...}]'
 *                      holds the title, body, images, attachments and two
 *                      <script type="text/plain"> carrying the raw title / text.
 *   reply host         data-raw-content | data-reply-content, data-media='[{...}]'
 *                      content is [.fp-reply-body] + [.fm-list], before .fp-reply-actions.
 */
(function () {
  'use strict';

  var TITLE_MAX = 200;
  var open = null;

  function csrf() {
    var m = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : (typeof window.CSRF_TOKEN === 'string' ? window.CSRF_TOKEN : '');
  }
  function say(msg) { if (window.showSnackbar) window.showSnackbar(msg); }
  function json(el, name, fallback) {
    try { return JSON.parse(el.getAttribute(name) || ''); } catch (e) { return fallback; }
  }
  function reduced() { return window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function icon(n) { return '<span class="material-symbols-outlined" aria-hidden="true">' + n + '</span>'; }

  function form(cfg) {
    var f = document.createElement('form');
    f.className = 'fe fe-' + cfg.kind;
    f.setAttribute('role', 'group');
    f.setAttribute('aria-label', cfg.kind === 'post' ? 'Edit post' : 'Edit reply');
    f.noValidate = true;
    f.innerHTML =
      (cfg.kind === 'post'
        ? '<label class="fe-title-wrap"><input class="fe-title" type="text" maxlength="' + TITLE_MAX + '" autocomplete="off" placeholder="Title" aria-label="Title">' +
          '<span class="fe-count" aria-hidden="true"></span></label>'
        : '') +
      '<div class="fe-body"><textarea class="fe-text" rows="' + (cfg.kind === 'post' ? 6 : 3) + '" data-fc="tools" data-fc-nodraft aria-label="' +
        (cfg.kind === 'post' ? 'Details' : 'Reply') + '"></textarea></div>' +
      '<div class="fe-tray"></div>' +
      '<div class="fe-bar">' +
        '<button type="button" class="fe-icon" data-fe="attach" aria-label="Add attachment" title="Add attachment">' + icon('attach_file') + '<b class="fe-badge" hidden></b></button>' +
        '<span class="fe-status" role="status" aria-live="polite"></span>' +
        '<button type="button" class="md-btn md-btn-text" data-fe="cancel">Cancel</button>' +
        '<button type="submit" class="md-btn md-btn-filled fe-save" data-fe="save">' + icon('check') + '<span>Save</span></button>' +
      '</div>';
    return f;
  }

  function start(cfg) {
    if (open && open.host === cfg.host) { open.focus(); return; }
    if (open) open.close(true);

    var f = form(cfg);
    var ta = f.querySelector('.fe-text');
    var titleEl = f.querySelector('.fe-title');
    var status = f.querySelector('.fe-status');
    var save = f.querySelector('.fe-save');
    var badge = f.querySelector('.fe-badge');
    var counter = f.querySelector('.fe-count');
    var attachBtn = f.querySelector('[data-fe="attach"]');

    ta.value = cfg.text || '';
    if (titleEl) titleEl.value = cfg.title || '';

    cfg.anchor.parentNode.insertBefore(f, cfg.anchor);
    cfg.view.forEach(function (n) { n.classList.add('fe-hidden'); });
    cfg.host.classList.add('is-editing');
    if (window.ForumComposer) ForumComposer.mount(ta, { kinds: false, noDraft: true, key: 'edit-' + cfg.id });
    if (window.InlineMedia && InlineMedia.enhanceTextarea) { try { InlineMedia.enhanceTextarea(ta); } catch (e) { /* optional */ } }

    var items = (cfg.images || []).map(function (u) { return { kind: 'image', url: u, name: decodeURIComponent((u.split('/').pop() || 'Image').split('?')[0]) }; })
      .concat(cfg.media || []);
    var tray = NebAttach.mount(f.querySelector('.fe-tray'), {
      items: items, images: cfg.kind === 'post', maxMedia: 4, maxImages: 3, onChange: refreshState
    });
    var initial = { text: ta.value, title: titleEl ? titleEl.value : '' };

    function dirty() {
      return ta.value !== initial.text || (titleEl && titleEl.value !== initial.title) || tray.dirty();
    }
    function refreshState() {
      var n = tray.count();
      badge.hidden = !n;
      badge.textContent = n;
      attachBtn.disabled = !tray.room();
      var busy = tray.busy();
      save.disabled = busy || state.saving;
      status.textContent = busy ? 'Uploading\u2026' : '';
      if (counter && titleEl) {
        var left = TITLE_MAX - titleEl.value.length;
        counter.textContent = left <= 40 ? left : '';
      }
    }
    var state = { saving: false };

    function body() { return ta.value.trim(); }

    function payload() {
      var p = { content: body(), attachments: tray.media() };
      if (cfg.kind === 'post') { p.title = titleEl.value.trim(); p.image_urls = tray.imageUrls(); }
      return p;
    }

    function close(silent) {
      f.classList.add('is-leaving');
      var done = function () {
        if (f.parentNode) f.parentNode.removeChild(f);
        cfg.view.forEach(function (n) { n.classList.remove('fe-hidden'); n.classList.add('fe-return'); });
        setTimeout(function () { cfg.view.forEach(function (n) { n.classList.remove('fe-return'); }); }, 450);
        cfg.host.classList.remove('is-editing');
        if (open && open.host === cfg.host) open = null;
      };
      if (silent || reduced()) done(); else setTimeout(done, 180);
    }

    function cancel() {
      if (!dirty() || !window.NebUI) { close(); return; }
      NebUI.confirm({ title: 'Discard your changes?', message: 'What you changed here has not been saved.',
        confirmLabel: 'Discard', cancelLabel: 'Keep editing', destructive: true, icon: 'edit' })
        .then(function (yes) { if (yes) close(); else ta.focus(); });
    }

    function submit() {
      if (state.saving) return;
      var p = payload();
      if (cfg.kind === 'post' && (!p.title || !p.content)) { say('A post needs a title and some details.'); (p.title ? ta : titleEl).focus(); return; }
      if (cfg.kind === 'reply' && !p.content && !p.attachments.length) { say('A reply needs some text or an attachment.'); ta.focus(); return; }
      if (tray.busy()) { say('Wait for the uploads to finish.'); return; }
      if (!dirty()) { close(); return; }
      state.saving = true;
      f.classList.add('is-saving');
      save.querySelector('span:last-child').textContent = 'Saving';
      refreshState();
      fetch(cfg.endpoint, {
        method: 'POST', credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify(p)
      }).then(function (r) { return r.json().catch(function () { return {}; }); }).then(function (d) {
        if (!d || !d.id) throw new Error((d && d.error) || 'Could not save your changes.');
        return cfg.repaint(d, p).then(function () { close(true); say(cfg.kind === 'post' ? 'Post updated' : 'Reply updated'); });
      }).catch(function (err) {
        state.saving = false;
        f.classList.remove('is-saving');
        save.querySelector('span:last-child').textContent = 'Save';
        refreshState();
        say(err.message || 'Could not save your changes.');
      });
    }

    f.addEventListener('submit', function (e) { e.preventDefault(); submit(); });
    f.addEventListener('click', function (e) {
      var b = e.target.closest('[data-fe]');
      if (!b) return;
      if (b.dataset.fe === 'cancel') cancel();
      else if (b.dataset.fe === 'attach') tray.pick();
    });
    f.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !e.defaultPrevented && !document.querySelector('.neb-menu[data-open]')) { e.stopPropagation(); cancel(); }
      else if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); submit(); }
    });
    ['dragenter', 'dragover'].forEach(function (t) {
      f.addEventListener(t, function (e) {
        if (e.dataTransfer && Array.prototype.indexOf.call(e.dataTransfer.types || [], 'Files') >= 0) { e.preventDefault(); f.classList.add('is-dropping'); }
      });
    });
    f.addEventListener('dragleave', function (e) { if (!f.contains(e.relatedTarget)) f.classList.remove('is-dropping'); });
    f.addEventListener('drop', function (e) {
      f.classList.remove('is-dropping');
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length) { e.preventDefault(); tray.add(e.dataTransfer.files); }
    });
    if (titleEl) titleEl.addEventListener('input', refreshState);
    ta.addEventListener('input', refreshState);

    refreshState();
    open = { host: cfg.host, close: close, focus: function () { (titleEl || ta).focus(); } };
    requestAnimationFrame(function () {
      var field = titleEl || ta;
      field.focus();
      if (!titleEl) { var n = ta.value.length; ta.setSelectionRange(n, n); }
      try { f.scrollIntoView({ block: 'nearest', behavior: reduced() ? 'auto' : 'smooth' }); } catch (e) { /* ignore */ }
    });
  }

  function repaintFrom(html, host, sel) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    var fresh = doc.querySelector(sel);
    return fresh || null;
  }
  function fetchPage() {
    return fetch(location.pathname + location.search, { credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch' } })
      .then(function (r) { return r.text(); });
  }
  function settle(root) {
    if (window.renderAllMath) { try { window.renderAllMath(root); } catch (e) { /* math is optional */ } }
    if (window.NebMedia) { try { window.NebMedia.mount(root); } catch (e) { /* players are optional */ } }
    if (window.ForumComposer) ForumComposer.scan(root);
    root.classList.add('fe-return');
    setTimeout(function () { root.classList.remove('fe-return'); }, 450);
  }

  function post(postId) {
    var host = document.querySelector('[data-post-view]');
    if (!host) return;
    var raw = function (id) { var s = document.getElementById(id); return s ? s.textContent : ''; };
    start({
      kind: 'post', id: postId, host: host, anchor: host, view: [host],
      title: raw('post-original-title'), text: raw('post-original-content'),
      images: json(host, 'data-images', []), media: json(host, 'data-media', []),
      endpoint: '/ajax/edit/post/' + encodeURIComponent(postId) + '/',
      repaint: function () {
        return fetchPage().then(function (html) {
          var fresh = repaintFrom(html, host, '[data-post-view]');
          if (!fresh) { location.reload(); return; }
          host.innerHTML = fresh.innerHTML;
          ['data-images', 'data-media'].forEach(function (a) { host.setAttribute(a, fresh.getAttribute(a) || '[]'); });
          settle(host);
        });
      }
    });
  }

  function reply(replyId) {
    var esc = window.CSS && CSS.escape ? CSS.escape(replyId) : replyId;
    var host = document.getElementById('reply-card-' + replyId) || document.querySelector('.fp-thread-reply[data-reply-id="' + esc + '"]');
    if (!host) return;
    var actions = host.querySelector('.fp-reply-actions');
    if (!actions) return;
    var view = [];
    for (var n = actions.previousElementSibling; n; n = n.previousElementSibling) {
      if (n.classList.contains('fp-reply-body') || n.classList.contains('fm-list')) view.push(n);
    }
    var text = host.getAttribute('data-raw-content');
    if (text == null) text = host.getAttribute('data-reply-content') || '';
    start({
      kind: 'reply', id: replyId, host: host, anchor: actions, view: view,
      text: text, media: json(host, 'data-media', []),
      endpoint: '/ajax/edit/reply/' + encodeURIComponent(replyId) + '/',
      repaint: function (d, p) {
        var isCard = host.id === 'reply-card-' + replyId;
        if (isCard) {
          return fetchPage().then(function (html) {
            var fresh = repaintFrom(html, host, '#reply-card-' + esc);
            if (!fresh) { location.reload(); return; }
            var next = document.importNode(fresh, true);
            host.replaceWith(next);
            settle(next);
          });
        }
        /* a thread item is drawn client-side: repaint its body from the saved reply */
        return fetch('/ajax/forum/preview/', {
          method: 'POST', credentials: 'same-origin',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify({ content: p.content })
        }).then(function (r) { return r.json(); }).then(function (pv) {
          var atts = window.renderAttachmentsHtml ? window.renderAttachmentsHtml(d.attachments || []) : '';
          view.forEach(function (n) { if (n.parentNode) n.parentNode.removeChild(n); });
          var html = (p.content ? '<div class="fp-reply-body">' + (pv.html || '') + '</div>' : '') + atts;
          actions.insertAdjacentHTML('beforebegin', html);
          host.setAttribute('data-reply-content', p.content);
          host.setAttribute('data-media', JSON.stringify(d.attachments || []));
          settle(host);
          var card = document.getElementById('reply-card-' + replyId);
          if (card) return fetchPage().then(function (h) {
            var fresh = repaintFrom(h, card, '#reply-card-' + esc);
            if (fresh) { var nx = document.importNode(fresh, true); card.replaceWith(nx); settle(nx); }
          });
        });
      }
    });
  }

  window.ForumEdit = { post: post, reply: reply };
})();
