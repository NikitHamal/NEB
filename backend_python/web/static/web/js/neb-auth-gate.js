/* One door for guest actions on the web (same idea as the Android AuthGate).
   NebAuth.require('like') opens a sheet; Sign in goes to /login/?next=<this page>, so the person returns
   to exactly this screen. Styles are injected on first use, so pages that never gate pay nothing. */
(function () {
  'use strict';
  var COPY = {
    like: ['favorite', 'Sign in to like', 'Likes are saved to your account.'],
    save: ['bookmark', 'Sign in to save', 'Saved items stay with your account on every device.'],
    reply: ['chat_bubble', 'Sign in to reply', 'Join the discussion from this post.'],
    follow: ['person_add', 'Sign in to follow', 'Follow people to see their posts first.'],
    post: ['edit_note', 'Sign in to post', 'Share a question or a note with the community.'],
    vote: ['how_to_vote', 'Sign in to vote', 'Your vote counts once per poll.'],
    upload: ['upload', 'Sign in to upload', 'Add notes and resources under your name.'],
    default: ['lock', 'Sign in to continue', 'You will come back to this page.']
  };
  var CSS = '.ng-scrim{position:fixed;inset:0;z-index:2147483000;background:rgba(0,0,0,.4);opacity:0;transition:opacity .25s}' +
    '.ng-scrim[data-on]{opacity:1}' +
    '.ng-sheet{position:fixed;left:50%;bottom:0;z-index:2147483001;width:min(440px,100%);box-sizing:border-box;padding:12px 24px calc(24px + env(safe-area-inset-bottom));' +
    'background:var(--md-surface-container-lowest,#fff);color:var(--md-on-surface,#111);border:1px solid var(--md-outline-variant,#ddd);border-bottom:0;border-radius:28px 28px 0 0;' +
    'transform:translate(-50%,100%);transition:transform .45s cubic-bezier(.2,1.1,.3,1);text-align:center}' +
    '.ng-sheet[data-on]{transform:translate(-50%,0)}' +
    '@media(min-width:640px){.ng-sheet{bottom:auto;top:50%;border-bottom:1px solid var(--md-outline-variant,#ddd);border-radius:28px;transform:translate(-50%,-44%) scale(.96);opacity:0;transition:transform .4s cubic-bezier(.2,1.1,.3,1),opacity .2s}.ng-sheet[data-on]{transform:translate(-50%,-50%) scale(1);opacity:1}}' +
    '.ng-grip{width:36px;height:4px;border-radius:2px;background:var(--md-outline-variant,#ccc);margin:0 auto 18px}' +
    '@media(min-width:640px){.ng-grip{display:none}}' +
    '.ng-ic{width:56px;height:56px;border-radius:20px;margin:0 auto 14px;display:grid;place-items:center;background:var(--md-primary-container,#dde);color:var(--md-on-primary-container,#113)}' +
    '.ng-ic .material-symbols-outlined{font-size:28px}' +
    '.ng-t{margin:0 0 6px;font:600 1.25rem/1.25 var(--display,inherit)}.ng-p{margin:0 0 20px;color:var(--md-on-surface-variant,#555);font-size:.95rem;line-height:1.45}' +
    '.ng-row{display:grid;gap:8px}' +
    '.ng-b{display:flex;align-items:center;justify-content:center;min-height:48px;border-radius:24px;border:0;font:600 .95rem/1 var(--body,inherit);cursor:pointer;text-decoration:none;transition:transform .35s cubic-bezier(.2,1.1,.3,1)}' +
    '.ng-b:active{transform:scale(.97)}' +
    '.ng-b--f{background:var(--md-primary,#1a56db);color:var(--md-on-primary,#fff)}' +
    '.ng-b--t{background:var(--md-secondary-container,#e3e8f0);color:var(--md-on-secondary-container,#123)}' +
    '.ng-b--x{background:transparent;color:var(--md-on-surface-variant,#555)}';
  var root = null, prev = null;

  function here() { return location.pathname + location.search + location.hash; }
  function loginUrl(mode) {
    return '/login/?next=' + encodeURIComponent(here()) + (mode ? '&panel=' + mode : '');
  }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }
  function close() {
    if (!root) return;
    var r = root; root = null;
    r.sheet.removeAttribute('data-on'); r.scrim.removeAttribute('data-on');
    document.removeEventListener('keydown', r.key);
    setTimeout(function () { r.sheet.remove(); r.scrim.remove(); }, 320);
    if (prev && prev.focus) prev.focus();
  }
  function open(reason) {
    if (root) return;
    if (!document.getElementById('ng-css')) {
      var st = el('style'); st.id = 'ng-css'; st.textContent = CSS;
      var n = document.querySelector('script[nonce]'); if (n && n.nonce) st.setAttribute('nonce', n.nonce);
      document.head.appendChild(st);
    }
    var c = COPY[reason] || COPY.default;
    prev = document.activeElement;
    var scrim = el('div', 'ng-scrim');
    var sheet = el('div', 'ng-sheet');
    sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-modal', 'true'); sheet.setAttribute('aria-label', c[1]);
    var ic = el('div', 'ng-ic'); var g = el('span', 'material-symbols-outlined', c[0]); g.setAttribute('aria-hidden', 'true'); ic.appendChild(g);
    var go = el('a', 'ng-b ng-b--f', 'Sign in'); go.href = loginUrl('');
    var up = el('a', 'ng-b ng-b--t', 'Create account'); up.href = loginUrl('signup');
    var no = el('button', 'ng-b ng-b--x', 'Not now'); no.type = 'button';
    var row = el('div', 'ng-row'); row.appendChild(go); row.appendChild(up); row.appendChild(no);
    sheet.appendChild(el('div', 'ng-grip')); sheet.appendChild(ic);
    sheet.appendChild(el('h2', 'ng-t', c[1])); sheet.appendChild(el('p', 'ng-p', c[2])); sheet.appendChild(row);
    document.body.appendChild(scrim); document.body.appendChild(sheet);
    var key = function (e) { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', key);
    scrim.addEventListener('click', close); no.addEventListener('click', close);
    root = { sheet: sheet, scrim: scrim, key: key };
    requestAnimationFrame(function () { requestAnimationFrame(function () { scrim.setAttribute('data-on', ''); sheet.setAttribute('data-on', ''); go.focus(); }); });
  }

  window.NebAuth = { require: open, close: close, loginUrl: loginUrl };
  /* Any htmx call that comes back 401 opens the sheet instead of leaving a dead button. */
  document.addEventListener('htmx:responseError', function (e) {
    if (e.detail && e.detail.xhr && e.detail.xhr.status === 401) open('default');
  });
  /* Markup hook: <button data-auth-gate="reply"> is intercepted for guests when the page sets NEB_GUEST. */
  document.addEventListener('click', function (e) {
    if (!window.NEB_GUEST) return;
    var t = e.target.closest && e.target.closest('[data-auth-gate]');
    if (!t) return;
    e.preventDefault(); e.stopPropagation();
    open(t.getAttribute('data-auth-gate'));
  }, true);
})();
