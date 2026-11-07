/* Library insights sheet. Two modes, one renderer:
   - one resource: [data-action="open-resource-insights"][data-resource-id]  -> /ajax/resource/<id>/insights/
   - everything you uploaded + your posts: [data-action="open-uploads-insights"] -> /ajax/uploads/insights/
   Same payloads as the app's /api/resources/<id>/insights/ and /api/uploads/insights/. Styles: .ins-* (m3x-app.css). */
(function () {
  'use strict';

  var state = { mode: 'one', id: '', days: 30, back: false };
  var scrim, sheet;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function num(n) {
    n = Number(n) || 0;
    if (n >= 1e6) return (n / 1e6).toFixed(1).replace(/\.0$/, '') + 'M';
    if (n >= 1e4) return (n / 1e3).toFixed(1).replace(/\.0$/, '') + 'K';
    return String(n);
  }
  function secs(s) {
    s = Number(s) || 0;
    if (s < 60) return Math.round(s) + ' s';
    return Math.floor(s / 60) + ' m ' + Math.round(s % 60) + ' s';
  }
  function pct(v) { return v == null ? 'None' : Math.round(v) + '%'; }

  function ensure() {
    if (sheet) return;
    scrim = document.createElement('div');
    scrim.className = 'ins-scrim';
    sheet = document.createElement('aside');
    sheet.className = 'ins-sheet';
    sheet.setAttribute('role', 'dialog');
    sheet.setAttribute('aria-modal', 'true');
    sheet.setAttribute('aria-label', 'Library insights');
    document.body.appendChild(scrim);
    document.body.appendChild(sheet);
    scrim.addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    sheet.addEventListener('click', function (e) {
      var r = e.target.closest('[data-ins-days]');
      if (r) { state.days = parseInt(r.getAttribute('data-ins-days'), 10); load(); }
      if (e.target.closest('[data-ins-close]')) close();
      var one = e.target.closest('[data-ins-open-resource]');
      if (one) { state.mode = 'one'; state.back = true; state.id = one.getAttribute('data-ins-open-resource'); load(); }
      if (e.target.closest('[data-ins-back]')) { state.mode = 'all'; state.back = false; load(); }
    });
  }
  function open(mode, id) {
    ensure();
    state.mode = mode;
    state.id = id || '';
    scrim.classList.add('is-open');
    sheet.classList.add('is-open');
    document.documentElement.style.overflow = 'hidden';
    load();
  }
  function close() {
    if (!sheet) return;
    scrim.classList.remove('is-open');
    sheet.classList.remove('is-open');
    document.documentElement.style.overflow = '';
  }

  function shell(inner, title, sub, back) {
    var ranges = [7, 30, 90].map(function (d) {
      return '<button type="button" data-ins-days="' + d + '" class="' + (state.days === d ? 'is-on' : '') + '">' + d + ' days</button>';
    }).join('');
    return '<div class="ins-bar">' +
      (back ? '<button type="button" class="pc-icon-btn pc-icon-btn--ghost" data-ins-back aria-label="Back"><span class="material-symbols-outlined">arrow_back</span></button>' : '') +
      '<div class="ins-title"><h2>' + esc(title) + '</h2><p>' + esc(sub || '') + '</p></div>' +
      '<button type="button" class="pc-icon-btn pc-icon-btn--ghost" data-ins-close aria-label="Close"><span class="material-symbols-outlined">close</span></button></div>' +
      '<div class="ins-range">' + ranges + '</div><div class="ins-body">' + inner + '</div>';
  }

  function url() {
    if (state.mode === 'one') return '/ajax/resource/' + encodeURIComponent(state.id) + '/insights/?days=' + state.days;
    return '/ajax/uploads/insights/?days=' + state.days;
  }
  function load() {
    var title = state.mode === 'one' ? 'Resource insights' : 'Your library insights';
    sheet.innerHTML = shell('<div class="ins-empty">Loading</div>', title, '', false);
    fetch(url(), { credentials: 'same-origin' })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (r) {
        if (!r.ok) { sheet.innerHTML = shell('<div class="ins-empty">' + esc(r.d.error || 'Insights are not available.') + '</div>', title, '', false); return; }
        if (state.mode === 'one') sheet.innerHTML = shell(oneBody(r.d), 'Resource insights', r.d.title, !!state.back);
        else sheet.innerHTML = shell(allBody(r.d), title, r.d.totals.resources + ' uploads', false);
      })
      .catch(function () { sheet.innerHTML = shell('<div class="ins-empty">Could not load insights.</div>', title, '', false); });
  }

  function chg(c) {
    if (c == null) return '<span class="ins-chg">New</span>';
    var cls = c > 0 ? 'up' : (c < 0 ? 'down' : '');
    return '<span class="ins-chg ' + cls + '">' + (c > 0 ? '+' : '') + c + '%</span>';
  }
  function kpi(label, k, fmt) {
    return '<div class="ins-kpi"><span>' + label + '</span><strong>' + (fmt ? fmt(k.value) : num(k.value)) + '</strong>' + chg(k.change) + '</div>';
  }
  function plain(label, value, sub) {
    return '<div class="ins-kpi"><span>' + label + '</span><strong>' + value + '</strong><span class="ins-chg">' + esc(sub || '') + '</span></div>';
  }
  function rows(list, empty) {
    if (!list || !list.length) return '<div class="ins-empty" style="padding:8px 0;text-align:left">' + (empty || 'No data yet') + '</div>';
    return list.map(function (r) {
      var p = r.pct != null ? r.pct : 0;
      return '<div class="ins-row"><span>' + esc(r.label) + '</span><b>' + num(r.count) + (r.pct != null ? ' <span class="ins-chg">' + Math.round(p) + '%</span>' : '') + '</b>' +
        '<div class="ins-meter"><i style="width:' + Math.max(2, p) + '%"></i></div></div>';
    }).join('');
  }
  function pair(a, b, la, lb) {
    var t = (a + b) || 1;
    return rows([{ label: la, count: a, pct: a * 100 / t }, { label: lb, count: b, pct: b * 100 / t }]);
  }
  function funnel(list) {
    var top = Math.max.apply(null, list.map(function (f) { return f.count; }).concat([1]));
    return rows(list.map(function (f) { return { label: f.label, count: f.count, pct: f.count * 100 / top }; }));
  }
  function tips(list) {
    return (list || []).map(function (t) {
      var ic = t.tone === 'up' ? 'trending_up' : (t.tone === 'down' ? 'trending_down' : 'lightbulb');
      return '<div class="ins-tip"><span class="material-symbols-outlined">' + ic + '</span><div><strong>' + esc(t.title) + '</strong><span class="t">' + esc(t.body) + '</span></div></div>';
    }).join('');
  }
  function chart(series) {
    var W = 520, H = 150, pad = 4, n = series.length, max = 1;
    series.forEach(function (s) { max = Math.max(max, s.views, s.unique); });
    var bw = (W - pad * 2) / n, bars = '', line = '';
    series.forEach(function (s, i) {
      var h = Math.round((s.views / max) * (H - 24));
      bars += '<rect x="' + (pad + i * bw + bw * 0.14).toFixed(1) + '" y="' + (H - 16 - h) + '" width="' + Math.max(2, bw * 0.72).toFixed(1) + '" height="' + Math.max(h, s.views ? 2 : 0) + '" rx="3" fill="var(--md-primary)" opacity=".85"><title>' + s.date + ': ' + s.views + ' opens</title></rect>';
      var y = H - 16 - Math.round((s.unique / max) * (H - 24));
      line += (i ? 'L' : 'M') + (pad + i * bw + bw / 2).toFixed(1) + ' ' + y;
    });
    return '<svg class="ins-chart" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" role="img" aria-label="Opens per day">' + bars +
      '<path d="' + line + '" fill="none" stroke="var(--md-tertiary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>' +
      '<text x="' + pad + '" y="' + (H - 2) + '" font-size="10" fill="var(--md-on-surface-variant)">' + series[0].date.slice(5) + '</text>' +
      '<text x="' + (W - pad) + '" y="' + (H - 2) + '" font-size="10" text-anchor="end" fill="var(--md-on-surface-variant)">' + series[n - 1].date.slice(5) + '</text></svg>' +
      '<div class="ins-legend"><span><i style="background:var(--md-primary)"></i>Opens</span><span><i style="background:var(--md-tertiary)"></i>People</span></div>';
  }
  function hours(h) {
    var max = Math.max.apply(null, h.concat([1]));
    return '<div class="ins-hours">' + h.map(function (v, i) {
      return '<i style="height:' + Math.max(5, Math.round(v * 100 / max)) + '%;opacity:' + (v ? 0.9 : 0.25) + '" title="' + i + ':00 ' + v + ' opens"></i>';
    }).join('') + '</div><div class="ins-hours-l"><span>12 AM</span><span>6 AM</span><span>12 PM</span><span>6 PM</span><span>11 PM</span></div>';
  }
  function card(title, inner) { return '<section class="ins-card"><h3>' + title + '</h3>' + inner + '</section>'; }

  /* The cards both modes share, from the one core payload. */
  function common(d) {
    var k = d.kpis, a = d.audience, out = '';
    out += tips(d.insights);
    out += '<div class="ins-grid">' + kpi('Opens', k.views) + kpi('People reached', k.uniqueViewers) +
      kpi('Seen in lists', k.impressions) + kpi('Read or played', k.reads) +
      kpi('Downloads', k.downloads) + kpi('Saved', k.saves) +
      kpi('Comments', k.comments) + kpi('Average time', k.avgDwellSec, secs) + '</div>';
    out += card('Opens per day', chart(d.series));
    out += card('From a list to a download', funnel(d.funnel) +
      '<div class="ins-chg">' + pct(d.ctr) + ' of those who saw it opened it, ' + pct(d.readRate) + ' read it, ' + pct(d.downloadRate) + ' downloaded it</div>');
    var p = d.push;
    if (p.announced || p.views) {
      out += card('Notifications', '<div class="ins-grid">' + plain('Told', num(p.notified), p.announced + ' announced') +
        plain('Opened from it', num(p.views), p.shareOfViews == null ? '' : Math.round(p.shareOfViews) + '% of opens') + '</div>');
    }
    out += card('Audience', pair(a.newViewers, a.returning, 'First time', 'Came back') + pair(a.members, a.guests, 'Members', 'Visitors'));
    if (d.classes.length) out += card('Reader class', rows(d.classes));
    out += card('Where they found it', rows(d.surfaces) + rows(d.channels));
    out += card('Devices', rows(d.devices) + rows(d.os) + rows(d.sources));
    out += card('Time of day', hours(d.hourly));
    out += card('How long they stayed', rows(d.dwell.buckets, 'Time appears once people scroll.') +
      '<div class="ins-chg">Median ' + secs(d.dwell.medianSec) + ' over ' + d.dwell.samples + ' visits</div>');
    if (d.countries.length) out += card('Countries', rows(d.countries));
    return out;
  }

  function oneBody(d) {
    if (!d.hasData && !d.lifetime.views) return '<div class="ins-empty">' + esc((d.insights[0] || {}).body || 'No opens yet.') + '</div>';
    var L = d.lifetime, s = d.standing;
    var out = common(d);
    out += card('Since it went live', '<div class="ins-grid">' + plain('Opens', num(L.views), L.uniqueViewers + ' people') +
      plain('Likes', num(L.likes)) + plain('Comments', num(L.comments)) + plain('Downloads', num(L.downloads)) +
      plain('Saved', num(L.bookmarks)) + plain('Seen in lists', num(L.impressions)) + '</div>');
    if (s.of > 1) out += card('Against your other uploads', '<div class="ins-chg">Rank ' + s.rank + ' of ' + s.of + ' by opens. Your median is ' + num(s.medianViews) + '.</div>');
    return out;
  }

  function allBody(d) {
    var t = d.totals;
    if (!t.resources && !d.posts.count) return '<div class="ins-empty">You have not uploaded anything yet.</div>';
    var out = '<div class="ins-grid">' + plain('Uploads', num(t.resources), t.live + ' live' + (t.pending ? ', ' + t.pending + ' in review' : '')) +
      plain('Total opens', num(t.views)) + plain('Likes', num(t.likes)) + plain('Downloads', num(t.downloads)) + '</div>';
    out += common(d);
    if (d.subjects.length) out += card('Opens by subject', rows(d.subjects));
    out += card('Your uploads', d.resources.length ? d.resources.map(function (r) {
      var max = Math.max(d.resources[0].views, 1);
      return '<button type="button" class="ins-row" data-ins-open-resource="' + esc(r.id) + '" style="width:100%;text-align:left;background:none;border:0;padding:6px 0;cursor:pointer;color:inherit">' +
        '<span>' + esc(r.title) + (r.status !== 'approved' ? ' (' + esc(r.status) + ')' : '') + '</span>' +
        '<b>' + num(r.views) + ' <span class="ins-chg">' + num(r.reads) + ' read, ' + num(r.downloads) + ' saved</span></b>' +
        '<div class="ins-meter"><i style="width:' + Math.max(2, r.views * 100 / max) + '%"></i></div></button>';
    }).join('') : '<div class="ins-empty">No uploads yet.</div>');
    var p = d.posts;
    if (p.count) {
      out += card('Your posts', '<div class="ins-grid">' + plain('Posts', num(p.count)) +
        '<div class="ins-kpi"><span>Opens</span><strong>' + num(p.views) + '</strong>' + chg(p.change) + '</div>' +
        plain('Likes', num(p.likes)) + plain('Comments', num(p.replies)) + '</div>' +
        rows(p.top.map(function (x) { return { label: x.title, count: x.views }; })));
    }
    return out;
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-action="open-resource-insights"], [data-action="open-uploads-insights"]');
    if (!b) return;
    e.preventDefault();
    e.stopPropagation();
    state.back = false;
    if (b.getAttribute('data-action') === 'open-uploads-insights') open('all');
    else open('one', b.getAttribute('data-resource-id'));
  }, true);

  window.NebResourceInsights = { open: open, close: close };
})();
