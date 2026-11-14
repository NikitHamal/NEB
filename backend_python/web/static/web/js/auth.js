/* Sign in, create account, verify, reset. One page, four panels, same JSON endpoints as ever.
   Role is not asked here: the welcome flow asks it once, for everybody, and saves it. */
(function () {
  'use strict';

  var root = document.getElementById('ax');
  var panels = ['login', 'signup', 'verify', 'forgot'];
  var seg = document.getElementById('ax-seg');
  var pill = seg.querySelector('.ax-seg-pill');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mode = 'login';
  var pendingEmail = '';
  var params = new URLSearchParams(window.location.search);

  function $(id) { return document.getElementById(id); }
  function csrf() { return (typeof CSRF_TOKEN !== 'undefined') ? CSRF_TOKEN : ''; }
  function nextUrl() {
    var n = params.get('next');
    return (n && n.charAt(0) === '/' && n.charAt(1) !== '/') ? n : '';
  }
  function api(path, body) {
    return fetch(path, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); });
  }
  function err(id, msg) { var e = $(id); e.textContent = msg || ''; e.classList.toggle('on', !!msg); }
  function busy(btn, on, text) {
    btn.disabled = on;
    if (on) { btn.dataset.label = btn.textContent; btn.innerHTML = '<span class="ax-spin"></span><span>' + text + '</span>'; }
    else { btn.innerHTML = '<span>' + (btn.dataset.label || '') + '</span>'; }
  }
  function mark(id, on) { var el = $(id); if (el) el.classList.toggle('has-error', !!on); }
  function rate(res) { return res.status === 429 ? 'Too many attempts. Wait a moment and try again.' : ''; }

  /* ---- panel switching ---- */
  function movePill() {
    var tab = seg.querySelector('[aria-selected="true"]') || seg.querySelector('button');
    if (!tab) return;
    pill.style.width = tab.offsetWidth + 'px';
    pill.style.transform = 'translateX(' + tab.offsetLeft + 'px)';
  }
  function go(name) {
    if (panels.indexOf(name) === -1) name = 'login';
    var prev = mode;
    mode = name;
    root.dataset.mode = name;
    var order = panels.indexOf(name) - panels.indexOf(prev);
    panels.forEach(function (p) {
      var el = $('panel-' + p);
      var on = p === name;
      el.classList.remove('is-on', 'from-right', 'from-left');
      if (on) {
        el.classList.add('is-on');
        if (prev !== name && !reduce) el.classList.add(order >= 0 ? 'from-right' : 'from-left');
      }
    });
    seg.classList.toggle('is-hidden', name === 'verify' || name === 'forgot');
    seg.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.go === name ? 'true' : 'false'); });
    movePill();
    document.querySelectorAll('.ax-error').forEach(function (e) { e.textContent = ''; e.classList.remove('on'); });
    document.querySelectorAll('.has-error').forEach(function (e) { e.classList.remove('has-error'); });
    var h = $('panel-' + name).querySelector('.ax-title');
    if (h) { try { h.focus({ preventScroll: true }); } catch (e) { /* noop */ } }
    if (name === 'verify') setTimeout(function () { $('verify-otp').querySelector('input').focus(); }, 60);
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-go]');
    if (t) { e.preventDefault(); go(t.dataset.go); }
    var eye = e.target.closest('[data-eye]');
    if (eye) {
      var input = $(eye.dataset.eye), show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      eye.querySelector('.material-symbols-outlined').textContent = show ? 'visibility_off' : 'visibility';
      eye.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
    }
  });
  window.addEventListener('resize', movePill);

  /* ---- after any successful email auth: sync the session, then route ---- */
  function finish(data) {
    var dest = nextUrl();
    var needsWelcome = !!(data.profileIncomplete || data.isNewUser);
    function route() {
      if (needsWelcome) window.location.href = root.dataset.welcome + (dest ? '?next=' + encodeURIComponent(dest) : '');
      else window.location.href = dest || root.dataset.home;
    }
    if (!data.authToken || !data.user) { route(); return; }
    fetch(root.dataset.session, {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ emailAuthToken: data.authToken, emailUser: data })
    }).then(function (r) { return r.json(); }).then(function (s) {
      needsWelcome = !!(s.profileIncomplete || s.isNewUser);
      route();
    }).catch(route);
  }

  /* ---- sign in ---- */
  $('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var id = $('login-email').value.trim(), pw = $('login-password').value, btn = $('login-btn');
    err('login-error', '');
    mark('login-email', !id); mark('login-password', !pw);
    if (!id) return err('login-error', 'Enter your username or email.');
    if (!pw) return err('login-error', 'Enter your password.');
    busy(btn, true, 'Signing in');
    api('/api/auth/email/login/', { email: id, password: pw }).then(function (res) {
      var d = res.data;
      if (rate(res)) { err('login-error', rate(res)); }
      else if (d.status === 'success' && d.authToken) { finish(d); return; }
      else if (d.needsVerification && d.email) { startVerify(d.email); }
      else if (d.needsSetPassword && d.email) { $('forgot-email').value = d.email; go('forgot'); $('forgot-form').requestSubmit(); }
      else { err('login-error', d.error || 'Could not sign in.'); mark('login-password', true); }
      busy(btn, false);
    }).catch(function () { err('login-error', 'Network error. Try again.'); busy(btn, false); });
  });

  /* ---- create account ---- */
  var nameTimer = null, nameSeq = 0;
  var nameStatus = $('signup-username-status');
  $('signup-username').addEventListener('input', function (e) {
    var v = e.target.value.trim();
    nameStatus.className = 'ax-status';
    nameStatus.textContent = '';
    clearTimeout(nameTimer);
    if (v.length < 3 || !/^[A-Za-z0-9_]+$/.test(v)) return;
    var seq = ++nameSeq;
    nameTimer = setTimeout(function () {
      fetch('/api/users/check-username/?username=' + encodeURIComponent(v), { credentials: 'same-origin' })
        .then(function (r) { return r.json(); }).then(function (d) {
          if (seq !== nameSeq) return;
          nameStatus.className = 'ax-status ' + (d.available ? 'ok' : 'bad');
          nameStatus.textContent = d.available ? 'Available' : 'Taken';
        }).catch(function () { /* the server checks again on submit */ });
    }, 350);
  });
  $('signup-password').addEventListener('input', function (e) {
    var p = e.target.value, n = 0;
    if (p.length >= 8) n++;
    if (p.length >= 12) n++;
    if (/[A-Z]/.test(p) && /[a-z]/.test(p)) n++;
    if (/\d/.test(p) && /[^A-Za-z0-9]/.test(p)) n++;
    $('signup-meter').dataset.level = p ? Math.max(1, n) : 0;
    var lab = $('signup-meter-label');
    if (lab) {
      var lvl = p ? Math.max(1, n) : 0;
      lab.textContent = !p ? '8 or more characters' : p.length < 8 ? 'Too short' : ['', 'Weak', 'Fair', 'Good', 'Strong'][lvl];
      lab.dataset.level = p.length < 8 ? 0 : lvl;
    }
  });
  $('signup-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var u = $('signup-username').value.trim(), em = $('signup-email').value.trim(), pw = $('signup-password').value, btn = $('signup-btn');
    err('signup-error', '');
    var bad = !u ? ['signup-username', 'Choose a username.'] :
      (u.length < 3 || !/^[A-Za-z0-9_]+$/.test(u)) ? ['signup-username', 'Username: 3+ letters, numbers or underscores.'] :
      (em.indexOf('@') < 1 || em.indexOf('.') < 0) ? ['signup-email', 'Enter a valid email address.'] :
      pw.length < 8 ? ['signup-password', 'Password needs at least 8 characters.'] : null;
    ['signup-username', 'signup-email', 'signup-password'].forEach(function (id) { mark(id, bad && bad[0] === id); });
    if (bad) return err('signup-error', bad[1]);
    busy(btn, true, 'Creating account');
    api('/api/auth/email/signup/', { email: em, password: pw, username: u }).then(function (res) {
      if (rate(res)) err('signup-error', rate(res));
      else if (res.data.status === 'success') { startVerify(em); }
      else err('signup-error', res.data.error || 'Could not create the account.');
      busy(btn, false);
    }).catch(function () { err('signup-error', 'Network error. Try again.'); busy(btn, false); });
  });

  /* ---- verify: six boxes, paste-friendly, submits itself ---- */
  var boxes = Array.prototype.slice.call($('verify-otp').querySelectorAll('input'));
  function code() { return boxes.map(function (b) { return b.value; }).join(''); }
  boxes.forEach(function (b, i) {
    b.addEventListener('input', function () {
      b.value = b.value.replace(/\D/g, '').slice(-1);
      b.classList.toggle('filled', !!b.value);
      err('verify-error', '');
      if (b.value && i < boxes.length - 1) boxes[i + 1].focus();
      if (code().length === 6) $('verify-form').requestSubmit();
    });
    b.addEventListener('keydown', function (e) {
      if (e.key === 'Backspace' && !b.value && i > 0) { boxes[i - 1].focus(); boxes[i - 1].value = ''; boxes[i - 1].classList.remove('filled'); }
      if (e.key === 'ArrowLeft' && i > 0) boxes[i - 1].focus();
      if (e.key === 'ArrowRight' && i < boxes.length - 1) boxes[i + 1].focus();
    });
    b.addEventListener('paste', function (e) {
      var text = (e.clipboardData || window.clipboardData).getData('text').replace(/\D/g, '').slice(0, 6);
      if (!text) return;
      e.preventDefault();
      boxes.forEach(function (x, k) { x.value = text.charAt(k) || ''; x.classList.toggle('filled', !!x.value); });
      (boxes[Math.min(text.length, 5)]).focus();
      if (text.length === 6) $('verify-form').requestSubmit();
    });
    b.addEventListener('focus', function () { b.select(); });
  });
  function cooldown(btn, label) {
    var s = 60;
    btn.disabled = true; btn.textContent = label + ' in ' + s + 's';
    var t = setInterval(function () {
      s--;
      if (s <= 0) { clearInterval(t); btn.disabled = false; btn.textContent = label; }
      else btn.textContent = label + ' in ' + s + 's';
    }, 1000);
  }
  function startVerify(email) {
    pendingEmail = email;
    $('verify-email-display').textContent = email;
    boxes.forEach(function (b) { b.value = ''; b.classList.remove('filled'); });
    cooldown($('resend-btn'), 'Resend code');
    go('verify');
  }
  $('verify-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var c = code(), btn = $('verify-btn');
    if (c.length < 6) return err('verify-error', 'Enter all 6 digits.');
    busy(btn, true, 'Verifying');
    api('/api/auth/email/verify/', { email: pendingEmail, code: c }).then(function (res) {
      if (res.data.status === 'success') { finish(res.data); return; }
      err('verify-error', rate(res) || res.data.error || 'That code did not work.');
      root.classList.remove('ax-shake'); void root.offsetWidth; root.classList.add('ax-shake');
      busy(btn, false);
    }).catch(function () { err('verify-error', 'Network error. Try again.'); busy(btn, false); });
  });
  $('resend-btn').addEventListener('click', function () {
    var btn = this; btn.disabled = true; btn.textContent = 'Sending';
    api('/api/auth/email/resend/', { email: pendingEmail }).then(function (res) {
      if (res.data.status === 'success') cooldown(btn, 'Resend code');
      else { err('verify-error', res.data.error || 'Could not resend.'); btn.disabled = false; btn.textContent = 'Resend code'; }
    }).catch(function () { btn.disabled = false; btn.textContent = 'Resend code'; });
  });

  /* ---- forgot / reset ---- */
  $('forgot-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var em = $('forgot-email').value.trim(), btn = $('forgot-btn');
    err('forgot-error', '');
    if (em.indexOf('@') < 1) { mark('forgot-email', true); return err('forgot-error', 'Enter a valid email address.'); }
    busy(btn, true, 'Sending');
    api('/api/auth/email/forgot/', { email: em }).then(function (res) {
      var d = res.data;
      if (rate(res)) { err('forgot-error', rate(res)); busy(btn, false); return; }
      if (d.status === 'success' || !d.error) {
        $('forgot-title').textContent = d.needsSetPassword ? 'Set a password' : 'Reset your password';
        $('reset-btn').querySelector('span').textContent = d.needsSetPassword ? 'Set password' : 'Set new password';
        $('reset-form').hidden = false;
        $('reset-code').focus();
        cooldown($('forgot-resend-btn'), 'Resend code');
        btn.innerHTML = '<span>Code sent</span>'; btn.disabled = true;
      } else { err('forgot-error', d.error); busy(btn, false); }
    }).catch(function () { err('forgot-error', 'Network error. Try again.'); busy(btn, false); });
  });
  $('forgot-resend-btn').addEventListener('click', function () {
    var btn = this; btn.disabled = true;
    api('/api/auth/email/forgot/', { email: $('forgot-email').value.trim() }).then(function () { cooldown(btn, 'Resend code'); })
      .catch(function () { btn.disabled = false; });
  });
  $('reset-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var c = $('reset-code').value.trim(), p = $('reset-password').value, p2 = $('reset-confirm').value, btn = $('reset-btn');
    err('reset-error', '');
    if (c.length < 6) return err('reset-error', 'Enter the 6-digit code.');
    if (p.length < 8) { mark('reset-password', true); return err('reset-error', 'Password needs at least 8 characters.'); }
    if (p !== p2) { mark('reset-confirm', true); return err('reset-error', 'The two passwords do not match.'); }
    busy(btn, true, 'Saving');
    api('/api/auth/email/reset-password/', { email: $('forgot-email').value.trim(), code: c, newPassword: p, confirmPassword: p2 }).then(function (res) {
      if (res.data.status === 'success') { finish(res.data); return; }
      err('reset-error', rate(res) || res.data.error || 'Could not reset the password.');
      busy(btn, false);
    }).catch(function () { err('reset-error', 'Network error. Try again.'); busy(btn, false); });
  });

  document.querySelectorAll('.ob-input').forEach(function (i) {
    i.addEventListener('input', function () { i.classList.remove('has-error'); });
  });

  var start = params.get('panel') || '';
  go(start === 'email-signup' || start === 'signup' ? 'signup' : start === 'forgot' ? 'forgot' : 'login');
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(movePill);
})();
