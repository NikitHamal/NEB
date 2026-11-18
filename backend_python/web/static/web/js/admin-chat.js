(function () {
  'use strict';
  var D = JSON.parse(document.getElementById('ac-data').textContent), esc = AcMd.esc, md = AcMd.render;
  var $ = function (id) { return document.getElementById(id); };
  var els = { list: $('ac-list'), feed: $('ac-feed'), model: $('ac-model'), input: $('ac-input'), send: $('ac-send'), name: $('ac-name'),
    sub: $('ac-sub'), think: $('ac-think'), web: $('ac-web'), voice: $('ac-voice'), custom: $('ac-custom'), note: $('ac-note'), form: $('ac-form') };
  var S = { prov: null, history: [], log: [], busy: false, ctrl: null, health: {} };
  var P = {}; try { P = JSON.parse(localStorage.getItem('acprefs') || '{}'); } catch (e) { P = {}; }
  P.models = P.models || {};
  function save() { try { localStorage.setItem('acprefs', JSON.stringify(P)); } catch (e) { /* private mode */ } }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function icon(n) { return '<span class="material-symbols-outlined">' + n + '</span>'; }
  function secs(ms) { return (ms / 1000).toFixed(ms < 10000 ? 1 : 0) + 's'; }
  var SUGGEST = ['Which model are you, and who made you?', 'Write a haiku about monsoon rain', 'What is 17 x 23? Show the steps', 'Explain quicksort in a short table of cases'];

  function renderList() {
    var q = ($('ac-search').value || '').toLowerCase(), html = '';
    [['Keyless', true], ['Key required', false]].forEach(function (g) {
      var rows = D.providers.filter(function (p) { return (p.keyless || p.id === 'custom') === g[1] && p.label.toLowerCase().indexOf(q) > -1; });
      if (!rows.length) return;
      html += '<div class="ac-group">' + g[0] + '<span>' + rows.length + '</span></div>';
      rows.forEach(function (p) {
        var h = S.health[p.id] || {};
        html += '<button type="button" class="ac-prov" data-id="' + p.id + '"' + (S.prov && S.prov.id === p.id ? ' aria-current="true"' : '') + '>' +
          '<span class="ac-dot" data-s="' + (h.s || '') + '"></span><span class="ac-prov-name">' + esc(p.label.replace(/\s*\(.*\)$/, '')) + '</span>' +
          (h.ms ? '<span class="ac-ms">' + secs(h.ms) + '</span>' : '') + '</button>';
      });
    });
    els.list.innerHTML = html || '<div class="ac-none">No provider matches</div>';
  }
  function showNote() {
    var h = S.health[S.prov.id];
    els.note.hidden = !(h && h.s === 'bad');
    if (!els.note.hidden) els.note.innerHTML = icon('error') + '<span>Last check failed: ' + esc(h.err || 'no answer') + '</span>';
  }
  function fillModels(ms) {
    var keep = P.models[S.prov.id] || els.model.value;
    els.model.innerHTML = ms.map(function (m) {
      var bad = m.state && m.state !== 'ready';
      return '<option value="' + esc(m.id) + '"' + (bad ? ' disabled' : '') + '>' + esc(m.label) + (bad ? ' (' + m.state + ')' : '') + '</option>';
    }).join('');
    if (keep && ms.some(function (m) { return m.id === keep && !(m.state && m.state !== 'ready'); })) els.model.value = keep;
    els.model.parentNode.hidden = !ms.length;
  }
  function setProvider(id, keepChat) {
    S.prov = D.providers.filter(function (p) { return p.id === id; })[0] || D.providers[0];
    if (!keepChat) { S.history = []; S.log = []; }
    P.prov = S.prov.id; save();
    els.name.textContent = S.prov.label.replace(/\s*\(.*\)$/, '');
    els.sub.textContent = S.prov.keyless ? 'No key needed' : (S.prov.id === 'custom' ? 'Your endpoint' : 'Shared key');
    els.think.hidden = !S.prov.thinking; els.web.hidden = !S.prov.web_search; els.voice.hidden = id !== 'inception';
    els.custom.hidden = id !== 'custom'; renderFeed();
    fillModels(D.models[id] || []); showNote();
    fetch('/admin/chat/models/' + id + '/', { credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (d) {
      if (S.prov.id === id && d.models && d.models.length) fillModels(d.models);
    }).catch(function () {});
    renderList(); els.input.focus();
  }
  function renderFeed() {
    els.feed.innerHTML = '';
    if (S.log.length || S.busy) return;
    var n = (D.models[S.prov.id] || []).length;
    var e = el('div', 'ac-empty', '<div class="ac-mark">' + esc(S.prov.label.charAt(0)) + '</div><h2>' + esc(els.name.textContent) + '</h2><p>' +
      (n ? n + ' model' + (n > 1 ? 's' : '') : 'Custom model') + '</p><div class="ac-sugg"></div>');
    SUGGEST.forEach(function (t) { var b = el('button', 'ac-chip', esc(t)); b.type = 'button'; b.onclick = function () { ask(t); }; e.lastChild.appendChild(b); });
    els.feed.appendChild(e);
  }
  function stick() { return els.feed.scrollHeight - els.feed.scrollTop - els.feed.clientHeight < 90; }
  function bottom(force) { if (force || stick()) els.feed.scrollTop = els.feed.scrollHeight; }
  function flash(b, txt) { var o = b.innerHTML; b.innerHTML = icon('check') + txt; setTimeout(function () { b.innerHTML = o; }, 1300); }

  async function ask(text) {
    text = (text || '').trim();
    if (S.busy || !text) return;
    if (!S.log.length) els.feed.innerHTML = '';
    S.busy = true; els.send.innerHTML = icon('stop'); els.send.classList.add('stop');
    els.feed.appendChild(el('div', 'ac-msg user', esc(text)));
    var card = el('div', 'ac-msg bot'), meta = el('div', 'ac-meta', '<span class="ac-mark sm">' + esc(S.prov.label.charAt(0)) + '</span><b>' + esc(els.name.textContent) + '</b>');
    var status = el('div', 'ac-status', '<span class="ac-spin"></span>Waiting for ' + esc(els.name.textContent)), body = el('div', 'ac-body');
    var raw = '', thoughts = '', think = null, thinkBox = null, t0 = Date.now(), tFirst = 0, failed = false, tick = 0, frame = 0, usedModel = els.model.value;
    card.append(meta, status, body); els.feed.appendChild(card); bottom(true);
    function paint() { frame = 0; body.innerHTML = md(raw); bottom(); }
    var fd = new FormData();
    fd.append('provider', S.prov.id); fd.append('model', els.model.value || ''); fd.append('message', text);
    fd.append('history', JSON.stringify(S.history.slice(-20)));
    fd.append('reasoning', els.think.getAttribute('aria-pressed')); fd.append('web_search', els.web.getAttribute('aria-pressed'));
    fd.append('voice_mode', els.voice.getAttribute('aria-pressed'));
    if (S.prov.id === 'custom') { fd.append('api_url', $('ac-url').value); fd.append('api_key', $('ac-key').value); }
    S.ctrl = new AbortController();
    try {
      var r = await fetch('/admin/chat/send/', { method: 'POST', body: fd, headers: { 'X-CSRFToken': CSRF_TOKEN }, credentials: 'same-origin', signal: S.ctrl.signal });
      if (!r.ok) throw new Error(r.status === 401 || r.status === 403 ? 'Session expired. Reload the page and sign in again.' : 'Server answered HTTP ' + r.status);
      var rd = r.body.getReader(), dec = new TextDecoder(), buf = '';
      for (;;) {
        var x = await rd.read(); if (x.done) break;
        buf += dec.decode(x.value, { stream: true });
        var chunks = buf.split('\n\n'); buf = chunks.pop();
        for (var i = 0; i < chunks.length; i++) {
          var line = chunks[i].replace(/^data: /, ''); if (!line || line === '[DONE]') continue;
          var ev; try { ev = JSON.parse(line); } catch (e) { continue; }
          if (ev.type === 'start') { usedModel = ev.model; meta.appendChild(el('span', 'ac-tag', esc(ev.model || 'default'))); }
          else if (ev.type === 'retry') status.innerHTML = '<span class="ac-spin"></span>Cooling down. Retry ' + ev.attempt + ' in ' + ev.wait + 's';
          else if (ev.type === 'thought') {
            if (!think) {
              think = el('details', 'ac-think', '<summary>' + icon('psychology') + '<span>Thinking</span></summary><div></div>'); think.open = true;
              thinkBox = think.lastChild; card.insertBefore(think, body);
              tick = setInterval(function () { think.querySelector('summary span').textContent = 'Thinking ' + Math.round((Date.now() - t0) / 1000) + 's'; }, 500);
            }
            thoughts += ev.content; thinkBox.textContent = thoughts; bottom();
          } else if (ev.type === 'search' && ev.results && ev.results.length) {
            var sr = el('div', 'ac-sources');
            ev.results.slice(0, 6).forEach(function (s) { if (/^https?:/.test(s.url || '')) sr.appendChild(el('a', 'ac-tag', icon('link') + esc((s.title || s.url).slice(0, 48)))).href = s.url; });
            if (sr.children.length) card.insertBefore(sr, body);
          } else if (ev.type === 'text') {
            if (!tFirst) { tFirst = Date.now() - t0; status.remove(); if (think) { clearInterval(tick); think.open = false; think.querySelector('summary span').textContent = 'Thought for ' + secs(tFirst); } }
            raw += ev.content; body.classList.add('ac-cursor'); if (!frame) frame = requestAnimationFrame(paint);
          } else if (ev.type === 'audio') { var au = el('audio'); au.controls = true; au.src = ev.dataUrl; card.appendChild(au); }
          else if (ev.type === 'error') { failed = true; status.remove(); body.className = 'ac-err'; body.innerHTML = icon('error') + '<span>' + esc(ev.message) + '</span>'; }
        }
      }
    } catch (e) {
      status.remove();
      if (e.name !== 'AbortError') { failed = true; body.className = 'ac-err'; body.innerHTML = icon('error') + '<span>' + esc(e.message) + '</span>'; }
      else meta.appendChild(el('span', 'ac-tag', 'Stopped'));
    }
    clearInterval(tick); if (frame) cancelAnimationFrame(frame); status.remove();
    if (raw) body.innerHTML = md(raw);
    body.classList.remove('ac-cursor'); if (think && think.open && raw) think.open = false;
    var total = Date.now() - t0, act = el('div', 'ac-act');
    if (raw) {
      var cps = tFirst ? Math.round(raw.length / 4 / Math.max((total - tFirst) / 1000, 0.3)) : 0;
      act.appendChild(el('span', 'ac-stats', (tFirst ? 'First token ' + secs(tFirst) + ' · ' : '') + secs(total) + ' · ' + raw.length + ' chars' + (cps > 1 && raw.length > 160 ? ' · ~' + cps + ' tok/s' : '')));
      var cp = el('button', 'ac-btn text', icon('content_copy') + 'Copy'); cp.type = 'button'; cp.onclick = function () { navigator.clipboard.writeText(raw); flash(cp, 'Copied'); }; act.appendChild(cp);
    }
    var again = el('button', 'ac-btn text', icon('refresh') + 'Retry'); again.type = 'button';
    again.onclick = function () { if (!S.busy) { card.previousSibling.remove(); card.remove(); S.log.splice(S.log.indexOf(entry), 1); if (!failed) S.history.splice(-2); ask(text); } };
    act.appendChild(again); card.appendChild(act);
    var entry = { q: text, a: raw || (failed ? body.textContent : ''), model: usedModel }; S.log.push(entry);
    if (raw && !failed) S.history.push({ role: 'user', content: text }, { role: 'assistant', content: raw });
    S.busy = false; S.ctrl = null; els.send.innerHTML = icon('arrow_upward'); els.send.classList.remove('stop'); bottom(true);
  }

  function health() {
    var b = $('ac-health'), lab = $('ac-health-label'); b.disabled = true; lab.textContent = 'Checking';
    D.providers.forEach(function (p) { if (p.keyless && p.id !== 'custom') S.health[p.id] = { s: 'run' }; }); renderList();
    fetch('/admin/chat/health/', { credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (d) {
      var ok = 0; d.results.forEach(function (x) { if (x.ok) ok++; S.health[x.id] = { s: x.ok ? 'ok' : 'bad', ms: x.ms, err: x.error }; });
      lab.textContent = ok + ' of ' + d.results.length + ' answered'; renderList(); showNote();
      P.health = { at: Date.now(), data: S.health, label: lab.textContent }; save();
    }).catch(function () { S.health = {}; lab.textContent = 'Check failed, retry'; renderList(); }).then(function () { b.disabled = false; });
  }
  function exportChat() {
    var t = S.log.map(function (e) { return '**You**\n' + e.q + '\n\n**' + els.name.textContent + ' (' + e.model + ')**\n' + e.a; }).join('\n\n---\n\n');
    if (t) { navigator.clipboard.writeText(t); flash($('ac-export'), ''); }
  }

  els.list.addEventListener('click', function (e) { var b = e.target.closest('.ac-prov'); if (b && !S.busy) setProvider(b.dataset.id); });
  els.feed.addEventListener('click', function (e) {
    var b = e.target.closest('.ac-copy-code'); if (!b) return;
    navigator.clipboard.writeText(b.closest('.ac-code').querySelector('code').textContent); b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1200);
  });
  els.model.addEventListener('change', function () { P.models[S.prov.id] = els.model.value; save(); });
  $('ac-search').addEventListener('input', renderList);
  $('ac-health').addEventListener('click', health);
  $('ac-export').addEventListener('click', exportChat);
  $('ac-clear').addEventListener('click', function () { if (S.ctrl) S.ctrl.abort(); S.history = []; S.log = []; renderFeed(); els.input.focus(); });
  [els.think, els.web, els.voice].forEach(function (b) {
    if (P[b.id] && !b.hidden) b.setAttribute('aria-pressed', 'true');
    b.addEventListener('click', function () { var on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', on); P[b.id] = on; save(); });
  });
  els.form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (S.busy) { S.ctrl && S.ctrl.abort(); return; }
    var t = els.input.value; els.input.value = ''; els.input.style.height = ''; ask(t);
  });
  els.input.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); els.form.requestSubmit(); } });
  els.input.addEventListener('input', function () { els.input.style.height = 'auto'; els.input.style.height = Math.min(els.input.scrollHeight, 180) + 'px'; });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && S.ctrl) S.ctrl.abort();
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); $('ac-search').focus(); }
  });
  var first = D.providers.filter(function (p) { return p.id === (P.prov || 'qwen'); })[0] || D.providers[0];
  setProvider(first.id);
  if (P.health && Date.now() - P.health.at < 15 * 60000) { S.health = P.health.data; $('ac-health-label').textContent = P.health.label; renderList(); showNote(); }
  else health();
})();
