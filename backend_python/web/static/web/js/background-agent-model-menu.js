/* Tembo-style two-pane model/provider selector (search + providers | models).
 *
 *   var menu = BA.createModelMenu({ root, onChange });
 *   menu.setCatalog(catalog, selection)  // selection: {provider, model, providerId}
 *   menu.value()  -> {provider, model, providerId, label}
 *   menu.setDisabled(bool)
 *
 * Left pane: providers with monogram badges. Right pane: that provider's
 * models. Searching filters both panes. Unavailable official providers stay
 * visible (dimmed, "key" tag) and offer a one-click jump into the settings
 * dialog via the onAddKey callback.
 */
(function () {
  'use strict';

  var BA = window.BA;
  if (!BA) return;

  function esc(value) { return BA.escapeHtml(value); }

  function shortLabel(label) {
    return String(label || '').split(' (')[0].trim() || label;
  }
  function monoFor(slug) {
    var map = { agnes: 'Ag', openai: 'OA', anthropic: 'An', gemini: 'Gm', deepseek: 'DS', qwen: 'Qw' };
    return map[slug] || 'Cu';
  }
  function slugClass(slug) {
    return ['agnes', 'openai', 'anthropic', 'gemini', 'deepseek', 'qwen'].includes(slug) ? slug : 'custom';
  }

  function normalize(catalog) {
    var providers = [];
    ((catalog && catalog.community) || []).forEach(function (p) {
      if (!p.selectableForAgent) return;
      providers.push({
        slug: p.slug, name: shortLabel(p.label), kind: 'community', official: false,
        available: p.available, hint: 'Free web model · no key needed', keySource: p.keySource,
        defaultModel: p.defaultModel, freeNote: '', id: '',
        models: (p.models || []).map(function (m) { return { id: m.id, label: m.label || m.id, note: m.note || '' }; })
      });
    });
    ((catalog && catalog.official) || []).forEach(function (p) {
      providers.push({
        slug: p.slug, name: shortLabel(p.label), kind: 'official', official: true,
        available: p.available, keySource: p.keySource, keyMasked: p.keyMasked,
        defaultModel: p.defaultModel, freeNote: p.freeNote || '', id: '',
        hint: p.available
          ? (p.keySource === 'byok' ? 'Your key' : (p.keySource === 'env' ? 'Server key' : 'Shared key'))
          : 'Needs an API key',
        models: (p.models || []).map(function (m) { return { id: m.id, label: m.label || m.id, note: m.note || '' }; })
      });
    });
    ((catalog && catalog.custom) || []).forEach(function (c) {
      providers.push({
        slug: 'custom', name: c.label || 'Custom provider', kind: 'custom', official: true,
        available: c.available, keySource: 'custom', defaultModel: c.defaultModel, freeNote: '', id: c.id,
        hint: 'Your provider',
        models: (c.models || []).map(function (m) { return { id: m.id, label: m.label || m.id, note: m.note || '' }; })
      });
    });
    return providers;
  }

  function createModelMenu(config) {
    var root = config.root;
    var onChange = config.onChange || function () {};
    var onAddKey = config.onAddKey || null;
    var catalog = null;
    var providers = [];
    var selection = { provider: '', model: '', providerId: '' };
    var activeProviderIndex = 0;
    var disabled = false;
    var query = '';

    root.classList.add('ba-model-menu');
    root.innerHTML =
      '<div class="ba-mm-head"><span class="ba-field-label">Model & provider</span>' +
      (config.onSettings
        ? '<button type="button" class="ba-icon-button ba-icon-button-quiet ba-mm-settings" title="AI provider settings" aria-label="AI provider settings"><span class="material-symbols-outlined">tune</span></button>'
        : '') +
      '</div>' +
      '<button type="button" class="ba-mm-trigger" aria-haspopup="listbox" aria-expanded="false">' +
      '<span class="ba-mono ba-mono-default"></span><span class="ba-mm-trigger-label">Select a model</span>' +
      '<span class="material-symbols-outlined ba-mm-chevron">expand_more</span></button>' +
      '<div class="ba-mm-backdrop" hidden></div>' +
      '<div class="ba-mm-popover" hidden>' +
      '<div class="ba-mm-search"><span class="material-symbols-outlined">search</span>' +
      '<input type="text" placeholder="Search models…" autocomplete="off" spellcheck="false"></div>' +
      '<div class="ba-mm-panes">' +
      '<div class="ba-mm-providers" role="listbox"></div>' +
      '<div class="ba-mm-models" role="listbox"></div>' +
      '</div></div>';

    var trigger = root.querySelector('.ba-mm-trigger');
    var triggerLabel = root.querySelector('.ba-mm-trigger-label');
    var triggerMono = root.querySelector('.ba-mono');
    var backdrop = root.querySelector('.ba-mm-backdrop');
    var popover = root.querySelector('.ba-mm-popover');
    var searchInput = root.querySelector('.ba-mm-search input');
    var providersPane = root.querySelector('.ba-mm-providers');
    var modelsPane = root.querySelector('.ba-mm-models');

    function isOpen() { return !popover.hidden; }

    /* The popover is portaled to <body> and anchored with fixed coordinates:
       the composer boxes (overflow:hidden, sticky stacking) would otherwise
       clip a downward menu — this always opens cleanly above the trigger. */
    function placePopover() {
      if (popover.hidden) return;
      var rect = trigger.getBoundingClientRect();
      var vw = window.innerWidth;
      var vh = window.innerHeight;
      var gap = 8;
      var width = Math.min(560, vw - 32);
      var left = Math.max(16, Math.min(rect.left, vw - width - 16));
      var maxHeight = Math.max(220, Math.min(470, rect.top - gap - 16));
      var dropUp = rect.top - gap - 16 >= 220 || rect.top > vh - rect.bottom;
      popover.style.width = width + 'px';
      popover.style.left = left + 'px';
      popover.style.right = 'auto';
      popover.style.maxHeight = maxHeight + 'px';
      if (dropUp) {
        popover.style.bottom = (vh - rect.top + gap) + 'px';
        popover.style.top = 'auto';
      } else {
        popover.style.top = (rect.bottom + gap) + 'px';
        popover.style.bottom = 'auto';
        popover.style.maxHeight = Math.max(200, Math.min(470, vh - rect.bottom - gap - 16)) + 'px';
      }
    }

    function open() {
      if (disabled || !providers.length) return;
      query = '';
      searchInput.value = '';
      if (backdrop.parentNode !== document.body) document.body.appendChild(backdrop); // fixed layers escape composer clipping/stacking
      if (popover.parentNode !== document.body) document.body.appendChild(popover);
      backdrop.hidden = false;
      popover.hidden = false;
      trigger.setAttribute('aria-expanded', 'true');
      trigger.querySelector('.ba-mm-chevron').style.transform = 'rotate(180deg)';
      ensureActiveProvider();
      render();
      placePopover();
      window.addEventListener('resize', placePopover);
      window.addEventListener('scroll', placePopover, true);
      setTimeout(function () { searchInput.focus(); }, 0);
    }
    function close() {
      if (popover.hidden) return;
      popover.hidden = true;
      backdrop.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');
      trigger.querySelector('.ba-mm-chevron').style.transform = '';
      window.removeEventListener('resize', placePopover);
      window.removeEventListener('scroll', placePopover, true);
    }
    function toggle() { isOpen() ? close() : open(); }

    document.addEventListener('click', function (event) {
      // The popover is portaled to <body>, so an in-popover click is not
      // inside `root` anymore — guard it explicitly.
      if (isOpen() && !root.contains(event.target) && !popover.contains(event.target)) close();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen()) close();
    });
    trigger.addEventListener('click', function (event) { event.stopPropagation(); toggle(); });
    backdrop.addEventListener('click', function (event) { event.stopPropagation(); close(); });
    if (config.onSettings) {
      root.querySelector('.ba-mm-settings').addEventListener('click', function (event) {
        event.stopPropagation();
        config.onSettings();
      });
    }
    searchInput.addEventListener('input', function () {
      query = searchInput.value.trim().toLowerCase();
      if (query) {
        var first = providers.findIndex(function (p) { return providerMatches(p); });
        if (first >= 0) activeProviderIndex = first;
      }
      render();
    });

    function providerMatches(p) {
      if (!query) return true;
      if (p.name.toLowerCase().includes(query)) return true;
      return p.models.some(function (m) {
        return m.label.toLowerCase().includes(query) || m.id.toLowerCase().includes(query);
      });
    }
    function modelMatches(m, p) {
      if (!query) return true;
      return m.label.toLowerCase().includes(query) || m.id.toLowerCase().includes(query) ||
        p.name.toLowerCase().includes(query);
    }

    function keyFor(p) { return p.kind === 'custom' ? 'custom:' + p.id : p.slug; }
    function findProvider(sel) {
      if (!sel || !sel.provider) return null;
      if (sel.provider === 'custom') {
        return providers.find(function (p) { return p.kind === 'custom' && p.id === sel.providerId; }) || null;
      }
      return providers.find(function (p) { return p.slug === sel.provider && p.kind !== 'custom'; }) || null;
    }
    function selectedKey() { return selection.provider ? (selection.provider + '|' + (selection.model || '')) : ''; }

    function ensureActiveProvider() {
      var selected = findProvider(selection);
      if (selected) {
        activeProviderIndex = providers.indexOf(selected);
        return;
      }
      var firstSelectable = providers.findIndex(function (p) { return p.available; });
      if (providers[activeProviderIndex] && providers[activeProviderIndex].available) return;
      if (firstSelectable >= 0) activeProviderIndex = firstSelectable;
    }

    function computeLabel() {
      var p = findProvider(selection);
      if (p) {
        var m = p.models.find(function (m) { return m.id === selection.model; });
        return { short: p.name + ' · ' + (m ? m.label : selection.model), mono: monoFor(p.slug), cls: slugClass(p.slug) };
      }
      var community = providers.find(function (p) { return p.kind === 'community'; });
      if (community) {
        var dm = community.models.find(function (m) { return m.id === community.defaultModel; }) || community.models[0];
        return { short: community.name + ' · ' + (dm ? dm.label : 'default') + ' (default)', mono: monoFor(community.slug), cls: slugClass(community.slug) };
      }
      return { short: 'Select a model', mono: 'Ai', cls: 'default' };
    }

    function syncTrigger() {
      var info = computeLabel();
      triggerLabel.textContent = info.short;
      triggerMono.textContent = info.mono;
      triggerMono.className = 'ba-mono ba-mono-' + info.cls;
      trigger.disabled = disabled;
    }

    function pick(p, m) {
      if (p.kind === 'official' && !p.available) return;
      selection = {
        provider: p.slug,
        model: m ? m.id : (p.defaultModel || (p.models[0] && p.models[0].id) || ''),
        providerId: p.kind === 'custom' ? p.id : ''
      };
      syncTrigger();
      close();
      onChange({
        provider: selection.provider,
        model: selection.model,
        providerId: selection.providerId,
        label: computeLabel().short
      });
    }

    function pickDefault(p) {
      selection = { provider: '', model: '', providerId: '' };
      syncTrigger();
      close();
      var dm = p.models.find(function (m) { return m.id === p.defaultModel; }) || p.models[0];
      onChange({ provider: '', model: '', providerId: '', label: (dm ? dm.label : 'Default') + ' (server default)' });
    }

    function renderProviders() {
      providersPane.innerHTML = '';
      var visible = providers.filter(providerMatches);
      if (!visible.length) {
        providersPane.innerHTML = '<div class="ba-mm-empty">No providers match</div>';
        return;
      }
      visible.forEach(function (p) {
        var row = document.createElement('button');
        row.type = 'button';
        var isSelectedProvider = findProvider(selection) === p;
        var isActive = providers[activeProviderIndex] === p;
        row.className = 'ba-mm-provider' + (isActive ? ' active' : '') + (isSelectedProvider ? ' chosen' : '') + (!p.available && p.official ? ' locked' : '');
        row.innerHTML =
          '<span class="ba-mono ba-mono-' + slugClass(p.slug) + '">' + esc(monoFor(p.slug)) + '</span>' +
          '<span class="ba-mm-provider-name"></span>' +
          (isSelectedProvider ? '<span class="material-symbols-outlined ba-mm-check">check</span>' : '') +
          '<span class="material-symbols-outlined ba-mm-arrow">chevron_right</span>';
        row.querySelector('.ba-mm-provider-name').textContent = p.name;
        row.addEventListener('click', function () {
          activeProviderIndex = providers.indexOf(p);
          render();
        });
        providersPane.appendChild(row);
      });
    }

    function renderModels() {
      modelsPane.innerHTML = '';
      var p = providers[activeProviderIndex];
      if (!p) { modelsPane.innerHTML = '<div class="ba-mm-empty"></div>'; return; }

      if (p.keyMasked) {
        var keyMeta = document.createElement('div');
        keyMeta.className = 'ba-mm-pane-meta';
        keyMeta.textContent = p.hint + ' · ' + p.keyMasked;
        modelsPane.appendChild(keyMeta);
      } else if (p.official) {
        var meta = document.createElement('div');
        meta.className = 'ba-mm-pane-meta' + (p.available ? ' ok' : ' warn');
        meta.textContent = p.hint + (p.freeNote ? ' · ' + p.freeNote : '');
        modelsPane.appendChild(meta);
      }

      if (p.kind === 'community') {
        var def = document.createElement('button');
        def.type = 'button';
        var isDefault = !selection.provider;
        def.className = 'ba-mm-model' + (isDefault ? ' chosen' : '');
        var dm = p.models.find(function (m) { return m.id === p.defaultModel; }) || p.models[0];
        def.innerHTML = '<span class="material-symbols-outlined ba-mm-model-icon">auto_awesome</span>' +
          '<span class="ba-mm-model-text"><span class="ba-mm-model-name">Server default</span>' +
          '<span class="ba-mm-model-note"></span></span>' +
          (isDefault ? '<span class="material-symbols-outlined ba-mm-check">check</span>' : '');
        def.querySelector('.ba-mm-model-note').textContent = dm ? dm.label : 'Managed by NEBians';
        def.addEventListener('click', function () { pickDefault(p); });
        modelsPane.appendChild(def);
      }

      var shown = p.models.filter(function (m) { return modelMatches(m, p); });
      if (!shown.length) {
        var empty = document.createElement('div');
        empty.className = 'ba-mm-empty';
        empty.textContent = query ? 'No models match “' + query + '”' : 'No models listed';
        modelsPane.appendChild(empty);
      }
      shown.forEach(function (m) {
        var row = document.createElement('button');
        row.type = 'button';
        var isChosen = Boolean(selection.provider) && findProvider(selection) === p &&
          (selection.model || '').toLowerCase() === m.id.toLowerCase();
        row.className = 'ba-mm-model' + (isChosen ? ' chosen' : '') + (!p.available && p.official ? ' locked' : '');
        row.innerHTML =
          '<span class="material-symbols-outlined ba-mm-model-icon">smart_toy</span>' +
          '<span class="ba-mm-model-text"><span class="ba-mm-model-name">' + esc(m.label) + '</span>' +
          (m.note ? '<span class="ba-mm-model-note">' + esc(m.note) + '</span>' : '') +
          '</span>' +
          (isChosen ? '<span class="material-symbols-outlined ba-mm-check">check</span>' : '');
        if (p.available || p.kind === 'community') {
          row.addEventListener('click', function () { pick(p, m); });
        }
        modelsPane.appendChild(row);
      });

      if (p.official && !p.available && onAddKey) {
        var cta = document.createElement('button');
        cta.type = 'button';
        cta.className = 'ba-mm-addkey';
        cta.innerHTML = '<span class="material-symbols-outlined">key</span><span>Add your ' + esc(p.name) + ' API key…</span>';
        cta.addEventListener('click', function () {
          close();
          onAddKey({ slug: p.slug === 'custom' ? null : p.slug });
        });
        modelsPane.appendChild(cta);
      }
    }

    function render() {
      renderProviders();
      renderModels();
    }

    return {
      value: function () {
        return { provider: selection.provider, model: selection.model, providerId: selection.providerId };
      },
      label: function () { return computeLabel().short; },
      setCatalog: function (nextCatalog, sel) {
        catalog = nextCatalog || catalog;
        providers = normalize(catalog);
        if (sel !== undefined) {
          selection = {
            provider: sel.provider || '',
            model: sel.model || '',
            providerId: sel.providerId || ''
          };
          // Drop a stale selection whose provider vanished.
          if (selection.provider && !findProvider(selection)) {
            selection = { provider: '', model: '', providerId: '' };
          }
        }
        syncTrigger();
        if (isOpen()) render();
      },
      setDisabled: function (value) {
        disabled = Boolean(value);
        if (disabled) close();
        syncTrigger();
      },
      close: close
    };
  }

  BA.createModelMenu = createModelMenu;
})();
