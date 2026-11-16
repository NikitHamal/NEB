/* Dynamic posts on the web: a post can wear a note page's look (tone, cover, icon, paper, type).
   The look is data-look="{...}" on a feed card or the reading page; this file draws it.
   Palettes mirror NoteTones.kt / NotePage.kt on Android. Only numbers and a short icon key come
   from the server; nothing user-written is ever put into markup. */
(function () {
  'use strict';
  var T = {
    0: null, 1: ['DCE4FF', '0A2A6B', '2A3A66', 'DCE4FF'], 2: ['E1E2EC', '1B1F2A', '3F4759', 'DCE2F9'],
    3: ['F6DAF0', '33102F', '5A2D55', 'FFD6F5'], 4: ['FFDAD6', '410002', '93000A', 'FFDAD6'],
    5: ['E7E8EE', '1A1B20', '2A2B31', 'E3E2E9'], 6: ['E1E2EC', '44474F', '44474F', 'C4C6D0'],
    7: ['F5EBDD', '4A3B22', '3A3126', 'EBDDC5'], 8: ['DDF3E4', '0F3D26', '17382A', 'BFEBD0'],
    9: ['FBF1C4', '4A4000', '3B3512', 'F3E8A3'], 10: ['FFE3D3', '5A2B10', '442618', 'FFD0B5'],
    11: ['BFE6F7', '063B57', '0C3550', 'B4E2FA'], 12: ['E1EBD9', '2B3A1E', '27301F', 'D3E3C6'],
    13: ['EFEAE4', '3B342D', '2E2B28', 'E5DED5'], 14: ['DDE3FF', '1D2A6B', '232B55', 'C9D2FF'],
    15: ['2B2E36', 'E6E8EE', '1A1C22', 'E6E8EE'], 16: ['0F1A33', 'DCE6FF', '0A1226', 'DCE6FF'],
    17: ['163B2A', 'D5F0E0', '0F2A1E', 'D5F0E0'], 18: ['FFDCE0', '4F1A24', '4A2229', 'FFD0D6'],
    19: ['D2F3EF', '08403B', '123A37', 'BDEFE9'], 20: ['FFE0DB', '5A2018', '4A2823', 'FFD0C8'],
    21: ['222B45', 'DDE5FF', '151B30', 'DDE5FF'], 22: ['EADFF7', '35214F', '3A2D4D', 'E3D3F6'],
    23: ['FFE6C2', '553300', '45331A', 'FFDBA8'], 24: ['E6E8C8', '3A3D12', '2D2F17', 'DEE1B4'],
    25: ['4A3426', 'F3E4D8', '2A1D14', 'F3E4D8'], 26: ['1F2124', 'E8EAED', '121315', 'E8EAED'],
    27: ['D9E1E8', '1C2B38', '2A3540', 'CFDAE4']
  };
  var COVER = [
    ['F5EBDD', '3A3126', '7A5C2E', 'EBDDC5', 'E2B66B'], ['DDF3E4', '17382A', '1F7A4D', 'BFEBD0', '6FD39A'],
    ['FFE3D3', '442618', 'B5521C', 'FFD0B5', 'FFA173'], ['FBF1C4', '3B3512', '8A7500', 'F3E8A3', 'F2D04B'],
    ['BFE6F7', '0C3550', '0B6DA0', 'B4E2FA', '4FB6E8'], ['2B2E36', '1A1C22', 'C9CDD8', 'C9CDD8', '59607A'],
    ['0F1A33', '0A1226', 'B9CCFF', 'B9CCFF', '2E56C9'], ['163B2A', '0F2A1E', 'A7E3C0', 'A7E3C0', '2E9A66'],
    ['FFDCE0', '45202A', 'B3263E', 'FFC2CB', 'FF8CA0'], ['D2F3EF', '0F3A36', '0B7A70', 'B2EAE3', '3CC4B5'],
    ['E4E8EF', '262B36', '4A5670', 'CDD4E3', '8C9AB8'], ['FFE0DB', '4A2420', 'C4412F', 'FFC7BE', 'FF8C7A'],
    ['D9E6FF', '14264F', '0B4AC2', 'B5CCFF', '5B8DEF'], ['2E2A27', '1E1B19', 'E0D6CC', 'E0D6CC', '7A6A5A']
  ];
  var ICON = {
    page: 'description', book: 'menu_book', bio: 'biotech', math: 'calculate', idea: 'lightbulb', mind: 'psychology',
    task: 'task_alt', world: 'public', music: 'music_note', sun: 'light_mode', moon: 'dark_mode', fire: 'local_fire_department',
    rocket: 'rocket_launch', trophy: 'emoji_events', game: 'sports_esports', camera: 'photo_camera', food: 'restaurant',
    fitness: 'fitness_center', cart: 'shopping_cart', car: 'directions_car', puzzle: 'extension', health: 'health_and_safety',
    soccer: 'sports_soccer', bike: 'pedal_bike', beach: 'beach_access', wallet: 'account_balance_wallet', chart: 'bar_chart',
    gift: 'redeem', chip: 'memory', podcast: 'podcasts', cafe: 'local_cafe', coffee: 'coffee', group: 'group', work: 'work'
  };
  var PAPER = ['', 'lines', 'grid', 'dots', 'lines', 'grid'];
  var sheet;

  function hex(v) { return '#' + v; }
  function dark() { return document.documentElement.getAttribute('data-theme') === 'dark'; }
  function css() {
    var text = '.pl{border-radius:28px;overflow:hidden;background-color:var(--pl-bg);color:var(--pl-ink)}' +
      '.pl :is(a,h1,h2,h3,p,time,.post-card-meta,.fp-post-body,.fp-post-title,.post-card-title){color:inherit!important}' +
      '.pl .material-symbols-outlined{color:inherit}' +
      '.pl-cover{position:relative;display:block;overflow:visible;margin-bottom:var(--pl-gap,14px)}' +
      '.pl-art{display:block;width:100%;height:var(--pl-h,92px);object-fit:cover;overflow:hidden}' +
      '.pl-tile{position:absolute;left:16px;bottom:calc(var(--pl-tile,44px)/-2);width:var(--pl-tile,44px);height:var(--pl-tile,44px);' +
      'border-radius:32%;display:grid;place-items:center;background:var(--pl-bg);color:var(--pl-ink)}' +
      '.pl-tile.alone{position:relative;left:0;bottom:0;background:var(--pl-soft)}' +
      '.pl-tile .material-symbols-outlined{font-size:calc(var(--pl-tile,44px)*.54)}' +
      '.pl[data-paper=lines]{background-image:repeating-linear-gradient(transparent 0 27px,var(--pl-line) 27px 28px)}' +
      '.pl[data-paper=grid]{background-image:linear-gradient(var(--pl-line) 1px,transparent 1px),linear-gradient(90deg,var(--pl-line) 1px,transparent 1px);background-size:28px 28px}' +
      '.pl[data-paper=dots]{background-image:radial-gradient(var(--pl-line2) 1.4px,transparent 1.5px);background-size:28px 28px}' +
      '.pl[data-font=serif]{font-family:Georgia,"Times New Roman",serif}.pl[data-font=mono]{font-family:ui-monospace,Menlo,Consolas,monospace}' +
      '@media (prefers-reduced-motion:no-preference){.pl-cover{animation:pl-in .5s cubic-bezier(.2,.9,.3,1.2) both}@keyframes pl-in{from{opacity:0;transform:translateY(8px)}}}';
    return text;
  }
  function install() {
    if (sheet) return;
    sheet = true;
    var text = css();
    try {
      var s = new CSSStyleSheet();
      s.replaceSync(text);
      document.adoptedStyleSheets = document.adoptedStyleSheets.concat([s]);
    } catch (e) {
      var el = document.createElement('style');
      var me = document.currentScript;
      if (me && me.nonce) el.setAttribute('nonce', me.nonce);
      el.textContent = text;
      document.head.appendChild(el);
    }
  }
  function art(look, h) {
    if (look.photo > 0) {
      var img = document.createElement('img');
      img.className = 'pl-art'; img.alt = ''; img.loading = 'lazy';
      img.src = '/media/content_images/' + (look.photo | 0) + '.webp';
      return img;
    }
    var k = (look.cover | 0) - 1;
    if (k < 0) return null;
    var p = COVER[k % COVER.length], d = dark();
    var bg = hex(d ? p[1] : p[0]), deep = hex(d ? p[3] : p[2]), vivid = hex(p[4]);
    var ax = 60 + ((k * 37) % 280), bx = 20 + ((k * 29) % 340), ar = (k * 17) % 50 - 20;
    var svg = '<svg class="pl-art" viewBox="0 0 400 100" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' +
      '<rect width="400" height="100" fill="' + bg + '"/>' +
      '<circle cx="' + ax + '" cy="42" r="' + (46 + (k % 4) * 6) + '" fill="' + vivid + '" opacity="' + (d ? .5 : .85) + '"/>' +
      '<rect x="' + bx + '" y="52" width="70" height="70" rx="22" transform="rotate(' + ar + ' ' + (bx + 35) + ' 87)" fill="' + deep + '" opacity=".26"/></svg>';
    var wrap = document.createElement('div');
    wrap.innerHTML = svg;
    return wrap.firstChild;
  }
  function apply(el) {
    var look;
    try { look = JSON.parse(el.getAttribute('data-look') || ''); } catch (e) { return; }
    if (!look || typeof look !== 'object') return;
    install();
    var d = dark(), t = T[look.tone | 0], big = el.tagName === 'ARTICLE' && el.classList.contains('fp-post-thread-main');
    el.classList.add('pl');
    var old = el.querySelector(':scope > .pl-cover');
    if (old) old.remove();
    if (t) {
      var bg = hex(d ? t[2] : t[0]), ink = hex(d ? t[3] : t[1]);
      el.style.setProperty('--pl-bg', bg); el.style.setProperty('--pl-ink', ink);
      el.style.setProperty('--pl-soft', 'color-mix(in srgb,' + ink + ' 14%,' + bg + ')');
      el.style.setProperty('--pl-line', 'color-mix(in srgb,' + ink + ' 10%,transparent)');
      el.style.setProperty('--pl-line2', 'color-mix(in srgb,' + ink + ' 24%,transparent)');
    } else {
      el.style.setProperty('--pl-bg', 'var(--md-sys-color-surface,Canvas)'); el.style.setProperty('--pl-ink', 'var(--md-sys-color-on-surface,CanvasText)');
      el.style.setProperty('--pl-soft', 'color-mix(in srgb,currentColor 12%,transparent)');
      el.style.setProperty('--pl-line', 'color-mix(in srgb,currentColor 10%,transparent)');
      el.style.setProperty('--pl-line2', 'color-mix(in srgb,currentColor 24%,transparent)');
    }
    var paper = PAPER[look.paper | 0];
    if (paper) el.setAttribute('data-paper', paper); else el.removeAttribute('data-paper');
    var font = ['', 'serif', 'mono'][look.font | 0];
    if (font) el.setAttribute('data-font', font); else el.removeAttribute('data-font');
    var a = art(look, big ? 148 : 92), name = ICON[look.icon] || look.icon;
    if (!a && !name) return;
    var cs = getComputedStyle(el), cover = document.createElement('div');
    cover.className = 'pl-cover';
    cover.style.setProperty('--pl-h', (big ? 148 : 92) + 'px');
    cover.style.setProperty('--pl-tile', (big ? 56 : 44) + 'px');
    cover.style.margin = '-' + cs.paddingTop + ' -' + cs.paddingRight + ' ' + (name && a ? (big ? 42 : 36) : 14) + 'px -' + cs.paddingLeft;
    if (a) cover.appendChild(a);
    if (name && /^[a-z_]{1,40}$/.test(name)) {
      var tile = document.createElement('span'), g = document.createElement('span');
      tile.className = 'pl-tile' + (a ? '' : ' alone');
      g.className = 'material-symbols-outlined'; g.textContent = name; g.setAttribute('aria-hidden', 'true');
      tile.appendChild(g); cover.appendChild(tile);
      if (!a) cover.style.margin = '0 0 12px';
    }
    el.insertBefore(cover, el.firstChild);
  }
  function scan(root) {
    var list = (root || document).querySelectorAll('[data-look]');
    for (var i = 0; i < list.length; i++) if (!list[i].classList.contains('pl')) apply(list[i]);
  }
  function start() {
    scan(document);
    new MutationObserver(function (muts) {
      for (var i = 0; i < muts.length; i++) {
        var added = muts[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var n = added[j];
          if (n.nodeType !== 1) continue;
          if (n.hasAttribute && n.hasAttribute('data-look') && !n.classList.contains('pl')) apply(n);
          if (n.querySelectorAll) scan(n);
        }
      }
    }).observe(document.body, { childList: true, subtree: true });
    new MutationObserver(function () {
      var all = document.querySelectorAll('.pl[data-look]');
      for (var i = 0; i < all.length; i++) apply(all[i]);
    }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
