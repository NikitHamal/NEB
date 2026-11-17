(function () {
  var U = window.U, D = window.PROFILES, T = window.TABS, ORDER = ['student', 'teacher', 'institution', 'contributor'];
  var st = { type: 'all', tab: {}, followed: {} }, stage = document.getElementById('stage');

  function tabsOf(P) { return P.tabs.filter(function (t) { return S.self || !t[4]; }); }
  function railHtml(P, cur) {
    return '<div class="rail" role="tablist">' + tabsOf(P).map(function (t) {
      return '<button role="tab" data-act="tab" data-tab="' + t[0] + '" aria-selected="' + (t[0] === cur) + '">' + (t[4] ? U.ms('lock', 'xs') : '') + t[1] + (t[3] != null ? '<i>' + t[3] + '</i>' : '') + '</button>';
    }).join('') + '</div>';
  }
  function actions(P) {
    var f = st.followed[P.id];
    if (S.self) return '<button class="btn t" data-act="toast" data-what="Edit profile opens">' + U.ms('edit', 's') + 'Edit profile</button><button class="btn o ib" data-act="share" aria-label="Share">' + U.ms('ios_share') + '</button>';
    return '<button class="btn f' + (f ? ' on' : '') + '" data-act="follow">' + U.ms(f ? 'check' : 'person_add', 's') + (f ? 'Following' : 'Follow') + '</button>' +
      (P.contact ? '<button class="btn t" data-act="call" data-phone="' + P.contact.phone + '">' + U.ms('call', 's') + 'Call</button>' : '') +
      '<button class="btn o ib" data-act="share" aria-label="Share">' + U.ms('ios_share') + '</button>';
  }
  function header(P) {
    var meta = P.meta.map(function (m) { return '<span>' + U.ms(m.i, 's') + (m.link ? '<a href="#" onclick="return false">' + m.t + '</a>' : m.t) + '</span>'; }).join('');
    var nums = P.nums.map(function (n) { return '<button data-act="tab" data-tab="' + (n[2] || 'overview') + '"><b>' + n[0] + '</b><span>' + n[1] + '</span></button>'; }).join('');
    return '<div class="cover">' + U.art(P.cover.kind, P.cover.seed, { palette: P.cover.palette, layout: P.cover.layout }) + '</div>' +
      '<div class="hd"><div class="hd-top">' + U.av(P.letter, P.shape, P.tone) + '<div class="acts">' + actions(P) + '</div></div>' +
      '<div class="nm"><h2>' + P.name + '</h2>' + U.verified(P.verified) + '</div>' +
      '<div class="sub"><span class="role">' + U.ms(P.role.icon, 's') + P.role.label + '</span><span>@' + P.user + '</span></div>' +
      '<div class="hl">' + P.headline + '</div><div class="meta">' + meta + '</div><div class="nums">' + nums + '</div></div>';
  }
  function phone(P) {
    var cur = st.tab[P.id] || 'overview'; if (!tabsOf(P).some(function (t) { return t[0] === cur; })) cur = 'overview';
    return '<div class="slot" data-p="' + P.id + '"><div class="cap">' + P.label + '<i style="font-style:normal;font-weight:400">' + (S.self ? 'my own' : 'visitor') + '</i></div><div class="phone"><div class="dev"><div class="sb"><span>9:41</span><i></i><span>' + U.ms('signal_cellular_alt', 's') + U.ms('battery_full', 's') + '</span></div>' +
      '<div class="scr"><div class="top"><button class="iconbtn" aria-label="Back">' + U.ms('arrow_back') + '</button><div class="mini">' + U.av(P.letter, P.shape, P.tone, 'sm') + '<b>' + P.name + '</b></div><button class="iconbtn" data-act="share" aria-label="Share">' + U.ms('ios_share') + '</button><button class="iconbtn" aria-label="More">' + U.ms('more_vert') + '</button></div>' +
      header(P) + '<div class="railbox">' + railHtml(P, cur) + '</div><div class="pane">' + T[cur](P) + '</div></div></div></div></div>';
  }
  function render() {
    document.documentElement.dataset.theme = S.theme;
    var ids = st.type === 'all' ? ORDER : [st.type];
    stage.className = 'stage' + (ids.length === 1 ? ' one' : '');
    stage.innerHTML = ids.map(function (i) { return phone(D[i]); }).join('');
    stage.querySelectorAll('.scr').forEach(bindScroll);
    document.querySelectorAll('[data-type]').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.type === st.type); });
    document.querySelectorAll('[data-self]').forEach(function (b) { b.setAttribute('aria-pressed', (b.dataset.self === '1') === S.self); });
    document.getElementById('theme').firstChild.textContent = S.theme === 'light' ? 'dark_mode' : 'light_mode';
  }
  function bindScroll(scr) { scr.addEventListener('scroll', function () { scr.parentNode.dataset.stuck = scr.scrollTop > 120 ? '1' : '0'; }); }
  function setTab(slot, tab) {
    var P = D[slot.dataset.p], scr = slot.querySelector('.scr'); st.tab[P.id] = tab;
    slot.querySelector('.railbox').innerHTML = railHtml(P, tab); slot.querySelector('.pane').outerHTML = '<div class="pane">' + T[tab](P) + '</div>';
    var rb = slot.querySelector('.railbox'); if (scr.scrollTop > rb.offsetTop - 84) scr.scrollTo({ top: rb.offsetTop - 84, behavior: 'smooth' });
    var a = slot.querySelector('.rail [aria-selected=true]'); if (a) a.scrollIntoView({ inline: 'center', block: 'nearest' });
  }
  function toast(slot, text, icon) {
    var dev = slot.querySelector('.dev'), old = dev.querySelector('.toast'); if (old) old.remove();
    var t = document.createElement('div'); t.className = 'toast'; t.innerHTML = U.ms(icon || 'info', 's') + '<span>' + text + '</span>'; dev.appendChild(t); setTimeout(function () { t.remove(); }, 2200);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-act]'), slot = e.target.closest('.slot'); if (!b || !slot) return; var P = D[slot.dataset.p], a = b.dataset.act;
    if (a === 'tab') setTab(slot, b.dataset.tab);
    else if (a === 'follow') { st.followed[P.id] = !st.followed[P.id]; b.parentNode.innerHTML = actions(P); }
    else if (a === 'call') toast(slot, 'Dialer opens with ' + b.dataset.phone, 'call');
    else if (a === 'like') { var on = b.classList.toggle('liked'), n = +b.dataset.n + (on ? 1 : 0); b.querySelector('b').textContent = n; if (!b.dataset.base) b.dataset.base = b.dataset.n; if (!on) b.querySelector('b').textContent = b.dataset.n; }
    else if (a === 'share') toast(slot, 'Link copied', 'content_copy');
    else if (a === 'invite') toast(slot, S.self ? 'Edit what you are open to' : 'Sent to ' + P.name.split(' ')[0] + ': ' + b.dataset.what, S.self ? 'edit' : 'check');
    else if (a === 'open') toast(slot, 'Opens ' + b.dataset.what, 'open_in_new');
    else if (a === 'toast') toast(slot, b.dataset.what, 'edit');
  });
  document.querySelectorAll('[data-type]').forEach(function (b) { b.onclick = function () { st.type = b.dataset.type; render(); }; });
  document.querySelectorAll('[data-self]').forEach(function (b) { b.onclick = function () { S.self = b.dataset.self === '1'; render(); }; });
  document.getElementById('theme').onclick = function () { S.theme = S.theme === 'light' ? 'dark' : 'light'; render(); };
  render();
})();
