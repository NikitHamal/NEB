/* Post insights sheet: opened from "See insights" in a post's menu (author and staff only).
   Data: GET /ajax/post/<id>/insights/?days=7|30|90 (same payload as the app's /api/posts/<id>/insights/). */
(function () {
  'use strict';

  var state = { id: '', days: 30, data: null };
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
  function ensure() {
    if (sheet) return;
    scrim = document.createElement('div');
    scrim.className = 'ins-scrim';
    sheet = document.createElement('aside');
    sheet.className = 'ins-sheet';
    sheet.setAttribute('role', 'dialog');
    sheet.setAttribute('aria-modal', 'true');
    sheet.setAttribute('aria-label', 'Post insights');
    document.body.appendChild(scrim);
    document.body.appendChild(sheet);
    scrim.addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    sheet.addEventListener('click', function (e) {
      var r = e.target.closest('[data-ins-days]');
      if (r) { state.days = parseInt(r.getAttribute('data-ins-days'), 10); load(); }
      if (e.target.closest('[data-ins-close]')) close();
    });
  }
  function open(id) {
    ensure();
    state.id = id;
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

  function shell(inner, sub) {
    var ranges = [7, 30, 90].map(function (d) {
      return '<button type="button" data-ins-days="' + d + '" class="' + (state.days === d ? 'is-on' : '') + '">' + d + ' days</button>';
    }).join('');
    return '<div class="ins-bar"><div class="ins-title"><h2>Post insights</h2><p>' + esc(sub || '') + '</p></div>' +
      '<button type="button" class="pc-icon-btn pc-icon-btn--ghost" data-ins-close aria-label="Close"><span class="material-symbols-outlined">close</span></button></div>' +
      '<div class="ins-range">' + ranges + '</div><div class="ins-body">' + inner + '</div>';
  }

  function load() {
    sheet.innerHTML = shell('<div class="ins-empty">Loading</div>');
    fetch('/ajax/post/' + encodeURIComponent(state.id) + '/insights/?days=' + state.days, { credentials: 'same-origin' })
      .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
      .then(function (r) {
        if (!r.ok) { sheet.innerHTML = shell('<div class="ins-empty">' + esc(r.d.error || 'Insights are not available.') + '</div>'); return; }
        state.data = r.d;
        sheet.innerHTML = shell(body(r.d), r.d.title);
      })
      .catch(function () { sheet.innerHTML = shell('<div class="ins-empty">Could not load insights.</div>'); });
  }

  function chg(c) {
    if (c == null) return '<span class="ins-chg">New</span>';
    var cls = c > 0 ? 'up' : (c < 0 ? 'down' : '');
    return '<span class="ins-chg ' + cls + '">' + (c > 0 ? '+' : '') + c + '%</span>';
  }
  function kpi(label, k, fmt) {
    return '<div class="ins-kpi"><span>' + label + '</span><strong>' + (fmt ? fmt(k.value) : num(k.value)) + '</strong>' + chg(k.change) + '</div>';
  }
  function rows(list, empty) {
    if (!list || !list.length) return '<div class="ins-empty" style="padding:8px 0;text-align:left">' + (empty || 'No data yet') + '</div>';
    return list.map(function (r) {
      return '<div class="ins-row"><span>' + esc(r.label) + '</span><b>' + num(r.count != null ? r.count : r.votes) + ' <span class="ins-chg">' + Math.round(r.pct) + '%</span></b>' +
        '<div class="ins-meter"><i style="width:' + Math.max(2, r.pct) + '%"></i></div></div>';
    }).join('');
  }
  function pair(a, b, la, lb) {
    var t = (a + b) || 1;
    return rows([{ label: la, count: a, pct: a * 100 / t }, { label: lb, count: b, pct: b * 100 / t }]);
  }

  function chart(series) {
    var W = 520, H = 150, pad = 4;
    var n = series.length;
    var max = 1;
    series.forEach(function (s) { max = Math.max(max, s.views, s.unique); });
    var bw = (W - pad * 2) / n;
    var bars = '', line = '';
    series.forEach(function (s, i) {
      var h = Math.round((s.views / max) * (H - 24));
      bars += '<rect x="' + (pad + i * bw + bw * 0.14).toFixed(1) + '" y="' + (H - 16 - h) + '" width="' + Math.max(2, bw * 0.72).toFixed(1) + '" height="' + Math.max(h, s.views ? 2 : 0) + '" rx="3" fill="var(--md-primary)" opacity=".85"><title>' + s.date + ': ' + s.views + ' views</title></rect>';
      var y = H - 16 - Math.round((s.unique / max) * (H - 24));
      line += (i ? 'L' : 'M') + (pad + i * bw + bw / 2).toFixed(1) + ' ' + y;
    });
    var first = series[0].date.slice(5), last = series[n - 1].date.slice(5);
    return '<svg class="ins-chart" viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" role="img" aria-label="Views per day">' + bars +
      '<path d="' + line + '" fill="none" stroke="var(--md-tertiary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>' +
      '<text x="' + pad + '" y="' + (H - 2) + '" font-size="10" fill="var(--md-on-surface-variant)">' + first + '</text>' +
      '<text x="' + (W - pad) + '" y="' + (H - 2) + '" font-size="10" text-anchor="end" fill="var(--md-on-surface-variant)">' + last + '</text></svg>' +
      '<div class="ins-legend"><span><i style="background:var(--md-primary)"></i>Views</span><span><i style="background:var(--md-tertiary)"></i>People</span></div>';
  }

  function hours(h) {
    var max = Math.max.apply(null, h.concat([1]));
    return '<div class="ins-hours">' + h.map(function (v, i) {
      return '<i style="height:' + Math.max(5, Math.round(v * 100 / max)) + '%;opacity:' + (v ? 0.9 : 0.25) + '" title="' + i + ':00 ' + v + ' opens"></i>';
    }).join('') + '</div><div class="ins-hours-l"><span>12 AM</span><span>6 AM</span><span>12 PM</span><span>6 PM</span><span>11 PM</span></div>';
  }

  function card(title, inner) { return '<section class="ins-card"><h3>' + title + '</h3>' + inner + '</section>'; }

  function body(d) {
    var k = d.kpis, out = '';
    if (!d.hasData && !d.lifetime.views) {
      return '<div class="ins-empty">' + esc((d.insights[0] || {}).body || 'No views yet.') + '</div>';
    }
    out += d.insights.map(function (t) {
      var ic = t.tone === 'up' ? 'trending_up' : (t.tone === 'down' ? 'trending_down' : 'lightbulb');
      return '<div class="ins-tip"><span class="material-symbols-outlined">' + ic + '</span><div><strong>' + esc(t.title) + '</strong><span class="t">' + esc(t.body) + '</span></div></div>';
    }).join('');
    out += '<div class="ins-grid">' +
      kpi('Views', k.views) + kpi('People reached', k.uniqueViewers) +
      kpi('Impressions', k.impressions) + kpi('Reactions', k.reactions) +
      kpi('Average read', k.avgDwellSec, secs) +
      '<div class="ins-kpi"><span>Open rate</span><strong>' + (d.ctr == null ? 'None' : d.ctr + '%') + '</strong><span class="ins-chg">' + (d.engagementRate == null ? '' : d.engagementRate + '% react') + '</span></div></div>';
    out += card('Views per day', chart(d.series));
    var L = d.lifetime;
    out += card('Since it was posted', '<div class="ins-grid">' +
      '<div class="ins-kpi"><span>Views</span><strong>' + num(L.views) + '</strong></div>' +
      '<div class="ins-kpi"><span>Likes</span><strong>' + num(L.likes) + '</strong></div>' +
      '<div class="ins-kpi"><span>Comments</span><strong>' + num(L.replies) + '</strong></div>' +
      '<div class="ins-kpi"><span>Saved</span><strong>' + num(L.bookmarks) + '</strong></div></div>');
    var a = d.audience;
    out += card('Audience', pair(a.newViewers, a.returning, 'First time', 'Came back') + pair(a.members, a.guests, 'Members', 'Visitors') + pair(a.followers, a.nonFollowers, 'Your followers', 'Everyone else'));
    out += card('Devices', rows(d.devices) + '<div class="ins-row" style="margin-top:6px"><b></b></div>' + rows(d.os) + rows(d.sources));
    out += card('Where readers came from', rows(d.surfaces) + rows(d.channels));
    out += card('Time of day', hours(d.hourly));
    out += card('How long they read', rows(d.dwell.buckets, 'Read time appears once people scroll.') +
      '<div class="ins-chg">Median ' + secs(d.dwell.medianSec) + ' over ' + d.dwell.samples + ' reads</div>');
    var ad = d.actionsByDevice;
    if ((ad.like || []).length || (ad.reply || []).length || (ad.vote || []).length) {
      out += card('Reactions by device',
        (ad.like.length ? '<div class="ins-chg">Likes</div>' + rows(ad.like) : '') +
        (ad.reply.length ? '<div class="ins-chg">Comments</div>' + rows(ad.reply) : '') +
        (ad.vote.length ? '<div class="ins-chg">Poll votes</div>' + rows(ad.vote) : ''));
    }
    if (d.poll) {
      var p = d.poll;
      out += card('Poll results', '<div class="ins-chg">' + num(p.voters) + ' voters' + (p.participation != null ? ', ' + p.participation + '% of readers' : '') + '</div>' +
        rows(p.options.map(function (o) { return { label: o.text + (o.added ? ' (added)' : ''), count: o.votes, pct: o.pct }; })));
    }
    if (d.countries.length) out += card('Countries', rows(d.countries));
    var s = d.standing;
    if (s.of > 1) out += card('Against your other posts', '<div class="ins-chg">Rank ' + s.rank + ' of ' + s.of + ' by views. Your median is ' + num(s.medianViews) + '.</div>');
    return out;
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-action="open-post-insights"]');
    if (!b) return;
    e.preventDefault();
    e.stopPropagation();
    if (typeof closeAllMoreMenus === 'function') closeAllMoreMenus();
    document.querySelectorAll('.more-menu').forEach(function (m) { m.style.display = 'none'; });
    open(b.getAttribute('data-post-id'));
  }, true);

  window.NebPostInsights = { open: open, close: close };
})();
