/* Admin > Analytics: trend chart, KPI <-> chart linking, section scroll-spy,
   range popover.  Plain SVG, no chart library: the page loads one fewer CDN
   script and the chart follows the theme tokens by itself. */
(function () {
  'use strict';

  var root = document.getElementById('an-root');
  if (!root) return;

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS = 'http://www.w3.org/2000/svg';
  var METRICS = { visitors: 'Visitors', visits: 'Visits', pageviews: 'Pageviews' };

  /* ───────── "Updated 14:32" ───────── */
  Array.prototype.forEach.call(root.querySelectorAll('.an-updated[data-ts]'), function (node) {
    var t = Number(node.getAttribute('data-ts'));
    if (t) node.textContent = 'Updated ' + new Date(t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  });

  /* ───────── custom-range popover ───────── */
  var pop = root.querySelector('.an-pop');
  if (pop) {
    document.addEventListener('pointerdown', function (e) {
      if (pop.open && !pop.contains(e.target)) pop.open = false;
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && pop.open) {
        pop.open = false;
        var s = pop.querySelector('summary');
        if (s) s.focus();
      }
    });
  }

  /* ───────── scroll-spy for the section chips ───────── */
  var jump = root.querySelector('.an-jump');
  if (jump && 'IntersectionObserver' in window) {
    var links = {};
    Array.prototype.forEach.call(jump.querySelectorAll('a[data-spy]'), function (a) {
      links[a.getAttribute('data-spy')] = a;
      a.addEventListener('click', function (e) {
        var target = document.getElementById(a.getAttribute('data-spy'));
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
        if (history.replaceState) history.replaceState(null, '', '#' + target.id);
      });
    });
    var activate = function (id) {
      Object.keys(links).forEach(function (k) {
        var on = k === id;
        links[k].classList.toggle('is-active', on);
        if (on) {
          jump.scrollLeft = links[k].offsetLeft - (jump.clientWidth - links[k].offsetWidth) / 2;
        }
      });
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && links[en.target.id]) activate(en.target.id);
      });
    }, { rootMargin: '-140px 0px -60% 0px', threshold: 0 });
    Array.prototype.forEach.call(root.querySelectorAll('[data-section]'), function (s) { io.observe(s); });
  }

  /* ───────── trend chart ───────── */
  var host = document.getElementById('an-trend');
  var dataEl = document.getElementById('an-data');
  if (!host || !dataEl) return;

  var data;
  try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var T = data.trend;
  var N = T.labels.length;
  var state = { metric: 'visitors', compare: true };

  var tip = document.createElement('div');
  tip.className = 'an-tip';
  host.appendChild(tip);

  function node(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(n);
    return n;
  }

  function fmt(n) {
    n = Math.round(n);
    if (n >= 1e6) return (n / 1e6).toFixed(1).replace(/\.0$/, '') + 'M';
    if (n >= 1e4) return (n / 1e3).toFixed(1).replace(/\.0$/, '') + 'k';
    return n.toLocaleString();
  }

  function niceScale(max) {
    if (max <= 0) return { top: 4, step: 1, steps: 4 };
    var raw = max / 4;
    var p = Math.pow(10, Math.floor(Math.log10(raw)));
    var n = raw / p;
    var step = (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * p;
    step = Math.max(step, 1);
    var steps = Math.max(Math.ceil(max / step), 2);
    return { top: step * steps, step: step, steps: steps };
  }

  /* Monotone cubic (Fritsch-Carlson): smooth, and never overshoots below zero. */
  function smooth(pts) {
    var n = pts.length;
    if (n === 0) return '';
    if (n === 1) return 'M' + pts[0][0] + ',' + pts[0][1];
    var dx = [], m = [], t = [], i;
    for (i = 0; i < n - 1; i++) {
      dx[i] = pts[i + 1][0] - pts[i][0];
      m[i] = (pts[i + 1][1] - pts[i][1]) / dx[i];
    }
    t[0] = m[0];
    t[n - 1] = m[n - 2];
    for (i = 1; i < n - 1; i++) t[i] = m[i - 1] * m[i] <= 0 ? 0 : (m[i - 1] + m[i]) / 2;
    for (i = 0; i < n - 1; i++) {
      if (m[i] === 0) { t[i] = 0; t[i + 1] = 0; continue; }
      var a = t[i] / m[i], b = t[i + 1] / m[i], s = a * a + b * b;
      if (s > 9) { var k = 3 / Math.sqrt(s); t[i] = k * a * m[i]; t[i + 1] = k * b * m[i]; }
    }
    var d = 'M' + pts[0][0].toFixed(1) + ',' + pts[0][1].toFixed(1);
    for (i = 0; i < n - 1; i++) {
      d += ' C' + (pts[i][0] + dx[i] / 3).toFixed(1) + ',' + (pts[i][1] + t[i] * dx[i] / 3).toFixed(1) +
        ' ' + (pts[i + 1][0] - dx[i] / 3).toFixed(1) + ',' + (pts[i + 1][1] - t[i + 1] * dx[i] / 3).toFixed(1) +
        ' ' + pts[i + 1][0].toFixed(1) + ',' + pts[i + 1][1].toFixed(1);
    }
    return d;
  }

  var geo = null; // last layout, used by the pointer handlers

  function render(animate) {
    var W = host.clientWidth, H = host.clientHeight;
    if (!W || !H) return;
    var old = host.querySelector('svg');
    if (old) host.removeChild(old);

    var series = T[state.metric] || [];
    var prev = (T.prev && T.prev[state.metric]) || [];
    var showPrev = state.compare && prev.length > 0;
    var max = Math.max.apply(null, series.concat(showPrev ? prev.slice(0, N) : [0]));
    var sc = niceScale(max);

    var M = { l: 40, r: 14, t: 14, b: 30 };
    var w = W - M.l - M.r, h = H - M.t - M.b;
    var base = M.t + h;
    var X = function (i) { return M.l + (N === 1 ? w / 2 : (i * w) / (N - 1)); };
    var Y = function (v) { return M.t + h - (v / sc.top) * h; };

    var svg = node('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, 'aria-hidden': 'true' });

    var i;
    for (i = 0; i <= sc.steps; i++) {
      var v = i * sc.step, y = Y(v);
      node('line', { x1: M.l, x2: W - M.r, y1: y, y2: y, class: 'an-grid-line' }, svg);
      var lab = node('text', { x: M.l - 10, y: y + 4, 'text-anchor': 'end', class: 'an-axis-text' }, svg);
      lab.textContent = fmt(v);
    }

    var perLabel = 64;
    var every = Math.max(1, Math.ceil(N / Math.max(2, Math.floor(w / perLabel))));
    for (i = 0; i < N; i += every) {
      var xl = node('text', { x: X(i), y: H - 8, 'text-anchor': 'middle', class: 'an-axis-text' }, svg);
      xl.textContent = T.labels[i];
    }

    var pts = series.map(function (v, k) { return [X(k), Y(v)]; });
    if (showPrev) {
      var pp = prev.slice(0, N).map(function (v2, k) { return [X(k), Y(v2)]; });
      node('path', { d: smooth(pp), class: 'an-prev' }, svg);
    }
    var line = smooth(pts);
    if (pts.length > 1) {
      node('path', { d: line + ' L' + X(N - 1).toFixed(1) + ',' + base + ' L' + X(0).toFixed(1) + ',' + base + ' Z', class: 'an-area' }, svg);
    }
    var ln = node('path', { d: line, class: 'an-line', pathLength: '1' }, svg);
    if (animate && !reduceMotion) ln.setAttribute('class', 'an-line is-drawing');
    if (N === 1) node('circle', { cx: pts[0][0], cy: pts[0][1], r: 5, fill: 'var(--md-primary)' }, svg);

    var guide = node('line', { y1: M.t, y2: base, class: 'an-guide', opacity: '0' }, svg);
    var dotPrev = node('circle', { r: 4, class: 'an-point-prev', opacity: '0' }, svg);
    var dot = node('circle', { r: 6, class: 'an-point', opacity: '0' }, svg);
    var hit = node('rect', { x: M.l, y: M.t, width: w, height: h, fill: 'transparent' }, svg);
    host.insertBefore(svg, tip);

    geo = { M: M, w: w, W: W, X: X, Y: Y, series: series, prev: prev, showPrev: showPrev, guide: guide, dot: dot, dotPrev: dotPrev };

    function show(evt) {
      var rect = svg.getBoundingClientRect();
      var px = evt.clientX - rect.left;
      var k = N === 1 ? 0 : Math.round(((px - M.l) / w) * (N - 1));
      k = Math.max(0, Math.min(N - 1, k));
      var cx = X(k);
      guide.setAttribute('x1', cx); guide.setAttribute('x2', cx); guide.setAttribute('opacity', '1');
      dot.setAttribute('cx', cx); dot.setAttribute('cy', Y(series[k])); dot.setAttribute('opacity', '1');
      if (showPrev && prev[k] !== undefined) {
        dotPrev.setAttribute('cx', cx); dotPrev.setAttribute('cy', Y(prev[k])); dotPrev.setAttribute('opacity', '1');
      } else {
        dotPrev.setAttribute('opacity', '0');
      }
      var html = '<div class="an-tip-date">' + T.fulls[k] + '</div>' +
        '<div class="an-tip-row"><span>' + METRICS[state.metric] + '</span><strong>' + series[k].toLocaleString() + '</strong></div>';
      if (showPrev && prev[k] !== undefined) {
        html += '<div class="an-tip-row an-tip-row--prev"><span>Previous</span><span>' + prev[k].toLocaleString() + '</span></div>';
      }
      tip.innerHTML = html;
      var tw = tip.offsetWidth, th = tip.offsetHeight;
      var left = cx + 16;
      if (left + tw > W) left = cx - tw - 16;
      var top = Math.max(0, Math.min(H - th - M.b, Y(series[k]) - th / 2));
      tip.style.transform = 'translate(' + Math.max(0, left) + 'px,' + top + 'px)';
      tip.classList.add('is-on');
    }
    function hide() {
      guide.setAttribute('opacity', '0'); dot.setAttribute('opacity', '0'); dotPrev.setAttribute('opacity', '0');
      tip.classList.remove('is-on');
    }
    hit.addEventListener('pointermove', show);
    hit.addEventListener('pointerdown', show);
    hit.addEventListener('pointerleave', hide);
    hit.addEventListener('pointercancel', hide);
  }

  /* ───────── metric switching (tabs and KPI cards share one state) ───────── */
  var tabs = Array.prototype.slice.call(root.querySelectorAll('.an-tabs [data-metric]'));
  var cards = Array.prototype.slice.call(root.querySelectorAll('.an-kpi[data-metric]'));

  function setMetric(m) {
    if (!METRICS[m] || m === state.metric) return;
    state.metric = m;
    tabs.forEach(function (b) { b.setAttribute('aria-selected', b.getAttribute('data-metric') === m ? 'true' : 'false'); });
    cards.forEach(function (c) {
      var on = c.getAttribute('data-metric') === m;
      c.classList.toggle('is-selected', on);
      c.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    render(true);
  }
  tabs.forEach(function (b) { b.addEventListener('click', function () { setMetric(b.getAttribute('data-metric')); }); });
  cards.forEach(function (c) {
    c.addEventListener('click', function () { setMetric(c.getAttribute('data-metric')); });
    c.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setMetric(c.getAttribute('data-metric')); }
    });
  });

  var cmp = document.getElementById('an-compare');
  if (cmp) cmp.addEventListener('change', function () { state.compare = cmp.checked; render(false); });

  var lastW = host.clientWidth;
  if ('ResizeObserver' in window) {
    new ResizeObserver(function () {
      var w = host.clientWidth;
      if (w && w !== lastW) { lastW = w; render(false); }
    }).observe(host);
  } else {
    window.addEventListener('resize', function () { render(false); });
  }
  render(true);
})();
