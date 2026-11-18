/* Pathways v5 extras: keyboard activation for card buttons, header state on scroll. */
(function () {
  'use strict';
  var V = window.V, D = document;
  D.addEventListener('keydown', function (e) {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.matches && e.target.matches('[tabindex="0"][data-go],[tabindex="0"][data-act]')) { e.preventDefault(); e.target.click(); }
  });
  window.addEventListener('scroll', function () { D.body.classList.toggle('scrolled', window.scrollY > 8); }, { passive: true });
})();
/* Near me: nearest district that has listed places, from the browser location and the map centroids. */
(function () {
  'use strict';
  var V = window.V;
  V.nearest = function (lat, lon) {
    var x = (lon - 80.06) / 8.14 * 4000, y = (30.45 - lat) / 4.1 * 2299, have = {}, best = null;
    V.PW.providers.forEach(function (p) { have[p.district] = 1; });
    window.NM_DATA.d.forEach(function (d) { if (!have[d.n]) return; var k = Math.hypot(d.c[0] - x, d.c[1] - y); if (!best || k < best.k) best = { n: d.n, k: k }; });
    return best && best.n;
  };
  V.acts.locate = function () {
    if (!navigator.geolocation) return V.toast('Location is not available here', 'location_off');
    V.toast('Finding your district', 'my_location');
    navigator.geolocation.getCurrentPosition(function (pos) {
      var d = V.nearest(pos.coords.latitude, pos.coords.longitude);
      if (!d) return V.toast('No listed places near you yet', 'location_off');
      Object.assign(V.st.colleges, { district: d, n: 24 }); V.toast('Showing ' + d, 'location_on');
      if (location.hash.indexOf('#/colleges') === 0) V.render(); else V.go('colleges');
    }, function () { V.toast('Location is off. Pick a district instead', 'location_off'); }, { timeout: 8000, maximumAge: 600000 });
  };
})();

/* Long notes: two lead sentences, the rest as a tidy fact list behind one tap. */
(function () {
  'use strict';
  var V = window.V, E = V.esc;
  V.facts = function (t) {
    t = String(t || ''); var ss = t.split(/(?<=[.!?])\s+(?=[A-Z0-9])/);
    if (ss.length <= 3 && t.length < 360) return '<p class="sm mut" style="margin-top:8px">' + E(t) + '</p>';
    return '<p class="sm mut" style="margin-top:8px">' + E(ss.slice(0, 2).join(' ')) + '</p><details class="more-f"><summary>' + V.ms('expand_more', 'sm') + 'Show ' + (ss.length - 2) + ' more facts</summary><ul>' +
      ss.slice(2).map(function (x) { return '<li>' + E(x) + '</li>'; }).join('') + '</ul></details>';
  };
})();

/* Recently viewed, share, and a render wrapper that runs after every route. */
(function () {
  'use strict';
  var V = window.V, M = V.ms, E = V.esc, o = V.render;
  var KIND = { course: ['school', function (i) { return V.R[i] && V.R[i].name; }, 'Course'], college: ['apartment', function (i) { return V.P[i] && V.P[i].name; }, 'College'], career: ['work', function (i) { return V.C[i] && V.C[i].name; }, 'Career'], exam: ['quiz', function (i) { return V.G[i] && V.G[i].name; }, 'Exam'], country: ['public', function (i) { return V.A[i] && V.A[i].country; }, 'Country'] };
  function track(r) {
    var k = KIND[r.name]; if (!k || !r.arg || !k[1](r.arg)) return;
    var a = V.store.recent = (V.store.recent || []).filter(function (x) { return !(x[0] === r.name && x[1] === r.arg); });
    a.unshift([r.name, r.arg]); V.store.recent = a.slice(0, 8); V.persist();
  }
  V.recentHtml = function () {
    var a = (V.store.recent || []).filter(function (x) { return KIND[x[0]] && KIND[x[0]][1](x[1]); }).slice(0, 6);
    if (!a.length) return '';
    return '<section class="sec"><div class="hd"><h2>Pick up where you left</h2><button class="more" data-act="clearRecent">Clear</button></div><div class="chips">' + a.map(function (x) {
      var k = KIND[x[0]]; return '<button class="chip rc" data-go="' + x[0] + '/' + E(x[1]) + '">' + M(k[0]) + '<span class="rt">' + E(k[1](x[1])) + '</span><span class="xs mut">' + k[2] + '</span></button>';
    }).join('') + '</div></section>';
  };
  V.acts.clearRecent = function () { V.store.recent = []; V.persist(); V.render(); };
  V.acts.share = function () {
    var u = location.href, t = document.title;
    if (navigator.share) navigator.share({ title: t, url: u }).catch(function () {});
    else if (navigator.clipboard) navigator.clipboard.writeText(u).then(function () { V.toast('Link copied', 'link'); }, function () { V.toast('Copy is not available here', 'info'); });
    else V.toast('Copy the address bar link', 'info');
  };
  window.removeEventListener('hashchange', o);
  V.render = function () {
    o.apply(this, arguments); var r = V.parse(), s = V.$('#shareBtn'); track(r); if (s) s.hidden = !KIND[r.name] && r.name !== 'roadmap';
  };
  window.addEventListener('hashchange', V.render);
})();
