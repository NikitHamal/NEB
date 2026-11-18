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
