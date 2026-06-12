function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function createPanel(stage, opts = {}) {
  const panel = el('div', 'ix-ctrl-panel');
  if (opts.side === 'left') panel.classList.add('ix-ctrl-left');

  const header = el('div', 'ix-ctrl-header');
  const title = el('span', 'ix-ctrl-title', opts.title || 'Controls');
  const collapseBtn = el('button', 'ix-ctrl-collapse');
  collapseBtn.type = 'button';
  collapseBtn.setAttribute('aria-label', 'Toggle controls');
  collapseBtn.innerHTML = '<span class="material-symbols-outlined">expand_more</span>';
  header.appendChild(title);
  header.appendChild(collapseBtn);
  panel.appendChild(header);

  const body = el('div', 'ix-ctrl-body');
  panel.appendChild(body);

  function toggle() { panel.classList.toggle('collapsed'); }
  header.addEventListener('click', toggle);

  if (opts.startCollapsed || (window.innerWidth < 640 && opts.collapseOnMobile !== false)) {
    panel.classList.add('collapsed');
  }

  stage.appendChild(panel);

  const api = {
    el: panel,
    body,

    slider({ label, min = 0, max = 100, step = 1, value = 0, unit = '', format, onChange }) {
      const wrap = el('label', 'ix-ctrl-row ix-ctrl-slider');
      const top = el('div', 'ix-ctrl-label-row');
      const lab = el('span', 'ix-ctrl-label', label);
      const val = el('span', 'ix-ctrl-value');
      const fmt = format || ((v) => `${v}${unit}`);
      val.textContent = fmt(value);
      top.appendChild(lab);
      top.appendChild(val);
      const input = document.createElement('input');
      input.type = 'range';
      input.min = min;
      input.max = max;
      input.step = step;
      input.value = value;
      input.addEventListener('input', () => {
        const v = parseFloat(input.value);
        val.textContent = fmt(v);
        if (onChange) onChange(v);
      });
      wrap.appendChild(top);
      wrap.appendChild(input);
      body.appendChild(wrap);
      return {
        el: wrap,
        get: () => parseFloat(input.value),
        set: (v) => { input.value = v; val.textContent = fmt(v); },
      };
    },

    toggle({ label, value = false, onChange }) {
      const wrap = el('label', 'ix-ctrl-row ix-ctrl-toggle');
      const lab = el('span', 'ix-ctrl-label', label);
      const input = document.createElement('input');
      input.type = 'checkbox';
      input.checked = value;
      const knob = el('span', 'ix-toggle-track');
      knob.appendChild(el('span', 'ix-toggle-thumb'));
      input.addEventListener('change', () => { if (onChange) onChange(input.checked); });
      wrap.appendChild(lab);
      wrap.appendChild(input);
      wrap.appendChild(knob);
      body.appendChild(wrap);
      return {
        el: wrap,
        get: () => input.checked,
        set: (v) => { input.checked = v; },
      };
    },

    select({ label, options, value, onChange }) {
      const wrap = el('label', 'ix-ctrl-row ix-ctrl-select');
      wrap.appendChild(el('span', 'ix-ctrl-label', label));
      const sel = document.createElement('select');
      options.forEach((opt) => {
        const o = document.createElement('option');
        o.value = typeof opt === 'object' ? opt.value : opt;
        o.textContent = typeof opt === 'object' ? opt.label : opt;
        sel.appendChild(o);
      });
      if (value !== undefined) sel.value = value;
      sel.addEventListener('change', () => { if (onChange) onChange(sel.value); });
      wrap.appendChild(sel);
      body.appendChild(wrap);
      return {
        el: wrap,
        get: () => sel.value,
        set: (v) => { sel.value = v; },
      };
    },

    button({ label, icon, onClick, variant }) {
      const btn = el('button', 'ix-ctrl-btn' + (variant ? ` ix-ctrl-btn-${variant}` : ''));
      btn.type = 'button';
      if (icon) {
        const ic = el('span', 'material-symbols-outlined', icon);
        btn.appendChild(ic);
      }
      btn.appendChild(document.createTextNode(label));
      btn.addEventListener('click', onClick);
      body.appendChild(btn);
      return { el: btn, setLabel: (l) => { btn.lastChild.textContent = l; } };
    },

    buttonRow(buttons) {
      const row = el('div', 'ix-ctrl-btn-row');
      const handles = buttons.map(({ label, icon, onClick, variant }) => {
        const btn = el('button', 'ix-ctrl-btn' + (variant ? ` ix-ctrl-btn-${variant}` : ''));
        btn.type = 'button';
        if (icon) btn.appendChild(el('span', 'material-symbols-outlined', icon));
        btn.appendChild(document.createTextNode(label));
        btn.addEventListener('click', onClick);
        row.appendChild(btn);
        return { el: btn, setLabel: (l) => { btn.lastChild.textContent = l; } };
      });
      body.appendChild(row);
      return handles;
    },

    readout({ label, value = '' }) {
      const wrap = el('div', 'ix-ctrl-row ix-ctrl-readout');
      wrap.appendChild(el('span', 'ix-ctrl-label', label));
      const val = el('span', 'ix-readout-value', String(value));
      wrap.appendChild(val);
      body.appendChild(wrap);
      let lastVal = String(value);
      return { el: wrap, set: (v) => { const s = String(v); if (s === lastVal) return; lastVal = s; val.textContent = s; } };
    },

    info(text) {
      const p = el('p', 'ix-ctrl-info', text);
      body.appendChild(p);
      return { el: p, set: (t) => { p.textContent = t; } };
    },

    divider() {
      body.appendChild(el('div', 'ix-ctrl-divider'));
    },

    section(label) {
      body.appendChild(el('div', 'ix-ctrl-section', label));
    },

    collapse() { panel.classList.add('collapsed'); },
    expand() { panel.classList.remove('collapsed'); },
    dispose() { if (panel.parentNode) panel.parentNode.removeChild(panel); },
  };

  return api;
}

export function createHud(stage, opts = {}) {
  const hud = el('div', 'ix-hud' + (opts.position ? ` ix-hud-${opts.position}` : ''));
  stage.appendChild(hud);
  return {
    el: hud,
    badge(text, color) {
      const b = el('span', 'ix-hud-badge', text);
      if (color) b.style.setProperty('--ix-hud-color', color);
      hud.appendChild(b);
      let lastText = String(text);
      return { el: b, set: (t) => { const s = String(t); if (s === lastText) return; lastText = s; b.textContent = s; }, remove: () => b.remove() };
    },
    clear() { hud.innerHTML = ''; },
    dispose() { hud.remove(); },
  };
}

export function showInfoCard(stage, { title, body, color }) {
  let card = stage.querySelector('.ix-info-card');
  if (!card) {
    card = el('div', 'ix-info-card');
    const close = el('button', 'ix-info-close');
    close.type = 'button';
    close.innerHTML = '<span class="material-symbols-outlined">close</span>';
    close.addEventListener('click', () => card.classList.remove('visible'));
    card.appendChild(close);
    card.appendChild(el('h4', 'ix-info-title'));
    card.appendChild(el('p', 'ix-info-body'));
    stage.appendChild(card);
  }
  card.querySelector('.ix-info-title').textContent = title;
  card.querySelector('.ix-info-body').textContent = body;
  if (color) card.style.setProperty('--ix-color', color);
  card.classList.add('visible');
  return card;
}

export function hideInfoCard(stage) {
  const card = stage.querySelector('.ix-info-card');
  if (card) card.classList.remove('visible');
}
