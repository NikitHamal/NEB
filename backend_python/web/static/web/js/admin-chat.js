(function () {
  'use strict';
  var D = JSON.parse(document.getElementById('ac-data').textContent);
  var $ = function (id) { return document.getElementById(id); };
  var els = { list: $('ac-list'), feed: $('ac-feed'), model: $('ac-model'), input: $('ac-input'), send: $('ac-send'),
    name: $('ac-name'), sub: $('ac-sub'), think: $('ac-think'), web: $('ac-web'), voice: $('ac-voice'), custom: $('ac-custom') };
  var S = { prov: null, history: [], busy: false, ctrl: null, health: {}, last: '' };

  function esc(t) { return t.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function md(src) {
    var parts = esc(src).split(/```(?:[\w+-]*\n)?/), out = '';
    parts.forEach(function (p, i) {
      if (i % 2) { out += '<pre><code>' + p.replace(/\n$/, '') + '</code></pre>'; return; }
      p = p.replace(/`([^`\n]+)`/g, '<code>$1</code>').replace(/\*\*([^*\n]+)\*\*/g, '<b>$1</b>');
      out += p.split(/\n{2,}/).filter(Boolean).map(function (x) { return '<p>' + x.replace(/\n/g, '<br>') + '</p>'; }).join('');
    });
    return out;
  }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function icon(n) { return '<span class="material-symbols-outlined">' + n + '</span>'; }

  function renderList() {
    var q = ($('ac-search').value || '').toLowerCase(), html = '', groups = [['Keyless', true], ['Key required', false]];
    groups.forEach(function (g) {
      var rows = D.providers.filter(function (p) { return (p.keyless || p.id === 'custom') === g[1] && p.label.toLowerCase().indexOf(q) > -1; });
      if (!rows.length) return;
      html += '<div class="ac-group">' + g[0] + '</div>';
      rows.forEach(function (p) {
        var h = S.health[p.id] || {};
        html += '<button type="button" class="ac-prov" data-id="' + p.id + '"' + (S.prov && S.prov.id === p.id ? ' aria-current="true"' : '') + '>' +
          '<span class="ac-dot" data-s="' + (h.s || '') + '"></span><span class="ac-prov-name">' + esc(p.label) + '</span>' +
          (h.ms ? '<span class="ac-ms">' + (h.ms / 1000).toFixed(1) + 's</span>' : '') + '</button>';
      });
    });
    els.list.innerHTML = html;
  }

  function setProvider(id) {
    S.prov = D.providers.filter(function (p) { return p.id === id; })[0];
    S.history = []; renderFeed();
    els.name.textContent = S.prov.label;
    els.sub.textContent = S.prov.keyless ? 'No key needed' : 'Uses the shared key';
    els.think.hidden = !S.prov.thinking; els.web.hidden = !S.prov.web_search; els.voice.hidden = id !== 'inception';
    els.custom.hidden = id !== 'custom';
    fillModels(D.models[id] || []);
    fetch('/admin/chat/models/' + id + '/', { credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (d) {
      if (S.prov.id === id && d.models && d.models.length) fillModels(d.models);
    }).catch(function () {});
    renderList(); els.input.focus();
  }
  function fillModels(ms) {
    var keep = els.model.value;
    els.model.innerHTML = ms.map(function (m) {
      var bad = m.state && m.state !== 'ready';
      return '<option value="' + esc(m.id) + '"' + (bad ? ' disabled' : '') + '>' + esc(m.label) + (bad ? ' (' + m.state + ')' : '') + '</option>';
    }).join('');
    if (keep && ms.some(function (m) { return m.id === keep; })) els.model.value = keep;
    els.model.hidden = !ms.length;
  }

  function renderFeed() {
    els.feed.innerHTML = '';
    if (!S.history.length && !S.busy) {
      var e = el('div', 'ac-empty', icon('forum') + '<b>' + esc(S.prov.label) + '</b>');
      els.feed.appendChild(e);
    }
  }
  function bottom() { els.feed.scrollTop = els.feed.scrollHeight; }

  function copyBtn(card) {
    var b = el('button', 'ac-btn text', icon('content_copy') + 'Copy'); b.type = 'button';
    b.onclick = function () { navigator.clipboard.writeText(card.raw || ''); b.lastChild.textContent = 'Copied'; setTimeout(function () { b.lastChild.textContent = 'Copy'; }, 1200); };
    return b;
  }

  async function ask(text) {
    if (S.busy || !text.trim()) return;
    if (!S.history.length) els.feed.innerHTML = '';
    S.last = text; S.busy = true; els.send.innerHTML = icon('stop'); 
    els.feed.appendChild(el('div', 'ac-msg user', esc(text)));
    var card = el('div', 'ac-msg bot'), meta = el('div', 'ac-meta', '<b>' + esc(S.prov.label) + '</b>'), body = el('div', 'ac-body ac-cursor');
    var think = null, thinkBox = null, audio = null; card.raw = '';
    card.appendChild(meta); card.appendChild(body); els.feed.appendChild(card); bottom();
    var fd = new FormData();
    fd.append('provider', S.prov.id); fd.append('model', els.model.value || ''); fd.append('message', text);
    fd.append('history', JSON.stringify(S.history.slice(-20)));
    fd.append('reasoning', els.think.getAttribute('aria-pressed')); fd.append('web_search', els.web.getAttribute('aria-pressed'));
    fd.append('voice_mode', els.voice.getAttribute('aria-pressed'));
    if (S.prov.id === 'custom') { fd.append('api_url', $('ac-url').value); fd.append('api_key', $('ac-key').value); }
    S.ctrl = new AbortController();
    var failed = false;
    try {
      var r = await fetch('/admin/chat/send/', { method: 'POST', body: fd, headers: { 'X-CSRFToken': CSRF_TOKEN }, credentials: 'same-origin', signal: S.ctrl.signal });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      var rd = r.body.getReader(), dec = new TextDecoder(), buf = '';
      for (;;) {
        var x = await rd.read(); if (x.done) break;
        buf += dec.decode(x.value, { stream: true });
        var chunks = buf.split('\n\n'); buf = chunks.pop();
        for (var i = 0; i < chunks.length; i++) {
          var line = chunks[i].replace(/^data: /, ''); if (!line || line === '[DONE]') continue;
          var ev = JSON.parse(line);
          if (ev.type === 'start') meta.innerHTML = '<b>' + esc(ev.providerLabel) + '</b><span class="ac-tag">' + esc(ev.model) + '</span>';
          else if (ev.type === 'text') { card.raw += ev.content; body.innerHTML = md(card.raw); body.classList.add('ac-cursor'); }
          else if (ev.type === 'thought') {
            if (!think) { think = el('details', 'ac-think', '<summary>Thinking</summary><div></div>'); thinkBox = think.lastChild; card.insertBefore(think, body); }
            thinkBox.textContent += ev.content;
          } else if (ev.type === 'retry') meta.appendChild(el('span', 'ac-tag warn', 'Cooling down, retry ' + ev.attempt + ' in ' + ev.wait + 's'));
          else if (ev.type === 'audio') { audio = el('audio'); audio.controls = true; audio.src = ev.dataUrl; card.appendChild(audio); }
          else if (ev.type === 'error') { failed = true; body.className = 'ac-err'; body.innerHTML = icon('error') + esc(ev.message); }
          else if (ev.type === 'done') meta.appendChild(el('span', 'ac-tag', (ev.ms / 1000).toFixed(1) + 's · ' + ev.chars + ' chars'));
          bottom();
        }
      }
    } catch (e) {
      if (e.name !== 'AbortError') { failed = true; body.className = 'ac-err'; body.innerHTML = icon('error') + esc(e.message); }
      else meta.appendChild(el('span', 'ac-tag', 'Stopped'));
    }
    body.classList.remove('ac-cursor');
    var act = el('div', 'ac-act');
    if (card.raw) act.appendChild(copyBtn(card));
    var again = el('button', 'ac-btn text', icon('refresh') + 'Retry'); again.type = 'button';
    again.onclick = function () { S.busy || ask(text); }; act.appendChild(again); card.appendChild(act);
    if (card.raw && !failed) { S.history.push({ role: 'user', content: text }, { role: 'assistant', content: card.raw }); }
    S.busy = false; S.ctrl = null; els.send.innerHTML = icon('arrow_upward'); bottom();
  }

  function health() {
    var b = $('ac-health'); b.disabled = true;
    D.providers.forEach(function (p) { if (p.keyless) S.health[p.id] = { s: 'run' }; }); renderList();
    fetch('/admin/chat/health/', { credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (d) {
      d.results.forEach(function (x) { S.health[x.id] = { s: x.ok ? 'ok' : 'bad', ms: x.ms, err: x.error }; });
      renderList();
    }).catch(function () { S.health = {}; renderList(); }).then(function () { b.disabled = false; });
  }

  els.list.addEventListener('click', function (e) { var b = e.target.closest('.ac-prov'); if (b) setProvider(b.dataset.id); });
  els.list.addEventListener('mouseover', function (e) { var b = e.target.closest('.ac-prov'); if (b) { var h = S.health[b.dataset.id]; b.title = h && h.err ? h.err : ''; } });
  $('ac-search').addEventListener('input', renderList);
  $('ac-health').addEventListener('click', health);
  $('ac-clear').addEventListener('click', function () { S.history = []; renderFeed(); });
  [els.think, els.web, els.voice].forEach(function (b) { b.addEventListener('click', function () { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); }); });
  $('ac-form').addEventListener('submit', function (e) {
    e.preventDefault();
    if (S.busy) { S.ctrl && S.ctrl.abort(); return; }
    var t = els.input.value; els.input.value = ''; els.input.style.height = ''; ask(t);
  });
  els.input.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); $('ac-form').requestSubmit(); } });
  els.input.addEventListener('input', function () { els.input.style.height = 'auto'; els.input.style.height = Math.min(els.input.scrollHeight, 180) + 'px'; });
  setProvider((D.providers.filter(function (p) { return p.id === 'deepai'; })[0] || D.providers[0]).id);
})();
