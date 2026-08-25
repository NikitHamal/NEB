(function () {
  'use strict';

  var BA = window.BA;
  var root = BA.qs('#background-agent-app');
  if (!root) return;
  var providersUrl = root.dataset.llmProvidersUrl || '';
  var detailTemplate = root.dataset.llmDetailTemplate || '';
  var testUrl = root.dataset.llmTestUrl || '';
  if (!providersUrl || !detailTemplate || !testUrl) return;

  var els = {
    open: BA.qs('#ba-open-providers'),
    dialog: BA.qs('#ba-providers-dialog'),
    close: BA.qs('#ba-providers-close'),
    listView: BA.qs('#ba-providers-list-view'),
    loading: BA.qs('#ba-providers-loading'),
    list: BA.qs('#ba-providers-list'),
    editorView: BA.qs('#ba-provider-editor-view'),
    back: BA.qs('#ba-provider-back'),
    editor: BA.qs('#ba-provider-editor'),
    deleteDialog: BA.qs('#ba-provider-delete-dialog'),
    deleteTitle: BA.qs('#ba-provider-delete-title'),
    deleteCopy: BA.qs('#ba-provider-delete-copy'),
    deleteCancel: BA.qs('#ba-provider-delete-cancel'),
    deleteConfirm: BA.qs('#ba-provider-delete-confirm')
  };
  if (!els.dialog || !els.list) return;

  var catalog = null;
  var providers = [];
  var pendingDelete = null;
  try {
    var seeded = JSON.parse((BA.qs('#ba-llm-catalog') || {}).textContent || 'null');
    if (seeded && seeded.official) catalog = seeded;
  } catch (error) { catalog = null; }

  function esc(value) { return BA.escapeHtml(value); }
  function detailUrl(id) { return detailTemplate.replace('__ID__', encodeURIComponent(id)); }
  function showList() { els.editorView.hidden = true; els.listView.hidden = false; }
  function showEditor() { els.listView.hidden = true; els.editorView.hidden = false; }

  function rowForPreset(slug) {
    return providers.find(function (row) { return row.provider === slug; }) || null;
  }

  function patch(url, fields) {
    return BA.api(url, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(fields || {})
    });
  }

  // Test calls must never strand the button: server caps at 30s, we abort at 45s.
  function postJson(url, payload, timeoutMs) {
    var controller = new AbortController();
    var timer = setTimeout(function () { controller.abort(); }, timeoutMs || 45000);
    return BA.api(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload || {}),
      signal: controller.signal
    }).finally(function () { clearTimeout(timer); });
  }

  function testErrorMessage(error) {
    if (error && error.name === 'AbortError') return 'Timed out after 45s — the provider is slow or unreachable.';
    return (error && error.message) || 'request failed';
  }

  function setBusy(button, busy) {
    if (!button) return;
    if (busy) {
      button.dataset.label = button.innerHTML;
      button.disabled = true;
      button.innerHTML = '<span class="ba-spinner"></span>';
    } else {
      button.disabled = false;
      if (button.dataset.label) button.innerHTML = button.dataset.label;
    }
  }

  function broadcastCatalog() {
    document.dispatchEvent(new CustomEvent('ba:llm-catalog-changed', { detail: { catalog: catalog } }));
  }

  async function refresh() {
    els.loading.hidden = false;
    try {
      var data = await BA.api(providersUrl);
      if (data.catalog) catalog = data.catalog;
      providers = data.providers || [];
      renderList();
      broadcastCatalog();
    } catch (error) {
      BA.toast(error.message || 'Could not load providers.', 'error');
    } finally {
      els.loading.hidden = true;
    }
  }

  // ---------------------------------------------------------------- list ---

  function sectionHeader(title, sub, onAdd) {
    var head = document.createElement('div');
    head.className = 'ba-provider-section';
    var textWrap = document.createElement('div');
    textWrap.innerHTML = '<h3></h3><small></small>';
    textWrap.querySelector('h3').textContent = title;
    textWrap.querySelector('small').textContent = sub;
    head.appendChild(textWrap);
    if (onAdd) {
      var add = document.createElement('button');
      add.type = 'button';
      add.className = 'ba-text-button ba-provider-add';
      add.innerHTML = '<span class="material-symbols-outlined">add</span><span>Add custom provider</span>';
      add.addEventListener('click', onAdd);
      head.appendChild(add);
    }
    return head;
  }

  function monoFor(slug) {
    var map = { agnes: 'Ag', openai: 'OA', anthropic: 'An', gemini: 'Gm', deepseek: 'DS', qwen: 'Qw', agentrouter: 'AR', empero: 'Em' };
    return map[slug] || 'Cu';
  }
  function slugClass(slug) {
    return ['agnes', 'openai', 'anthropic', 'gemini', 'deepseek', 'qwen', 'agentrouter', 'empero'].includes(slug) ? slug : 'custom';
  }

  function presetRow(preset, row) {
    var node = document.createElement('div');
    node.className = 'ba-provider-row';
    var dotClass = row ? 'ok' : (preset.keySource ? '' : 'warn');
    node.innerHTML =
      '<div class="ba-provider-row-icon"><span class="ba-mono ba-mono-' + slugClass(preset.slug) + '"></span></div>' +
      '<div class="ba-provider-row-body"><strong></strong><small><span class="ba-status-dot ' + dotClass + '"></span><span class="ba-status-text"></span></small></div>';
    node.querySelector('.ba-mono').textContent = monoFor(preset.slug);
    var label = node.querySelector('strong');
    label.textContent = preset.label;
    if (preset.freeNote) {
      var chip = document.createElement('span');
      chip.className = 'ba-provider-chip';
      chip.textContent = preset.freeNote;
      label.appendChild(chip);
    }
    var statusText = node.querySelector('.ba-status-text');
    if (row) {
      statusText.textContent = row.keyMasked ? ('Your key ' + row.keyMasked) : 'Your key saved';
    } else if (preset.keySource === 'env') {
      statusText.textContent = 'Using server key';
    } else if (preset.keySource === 'bot') {
      statusText.textContent = 'Using shared workspace key';
    } else {
      statusText.textContent = 'Not connected — add your API key';
      statusText.classList.add('ba-provider-off');
    }
    var actions = document.createElement('div');
    actions.className = 'ba-provider-row-actions';
    var manage = document.createElement('button');
    manage.type = 'button';
    manage.className = 'ba-text-button';
    manage.innerHTML = '<span>' + (row ? 'Manage' : 'Add key') + '</span>';
    manage.addEventListener('click', function () { openPresetEditor(preset, rowForPreset(preset.slug)); });
    actions.appendChild(manage);
    node.appendChild(actions);
    return node;
  }

  function customRow(row) {
    var node = document.createElement('div');
    node.className = 'ba-provider-row' + (row.enabled ? '' : ' ba-provider-row-disabled');
    node.innerHTML =
      '<div class="ba-provider-row-icon"><span class="ba-mono ba-mono-custom"></span></div>' +
      '<div class="ba-provider-row-body"><strong></strong><small></small></div>';
    node.querySelector('.ba-mono').textContent = (row.name || 'Cu').slice(0, 2);
    node.querySelector('strong').textContent = row.name || 'Custom provider';
    var meta = [row.baseUrl, row.models.length + ' model' + (row.models.length === 1 ? '' : 's'), row.keyMasked].filter(Boolean);
    node.querySelector('small').textContent = (row.enabled ? '' : 'Paused · ') + meta.join(' · ');
    var actions = document.createElement('div');
    actions.className = 'ba-provider-row-actions';

    var toggle = document.createElement('label');
    toggle.className = 'ba-toggle';
    toggle.title = row.enabled ? 'Disable provider' : 'Enable provider';
    toggle.innerHTML = '<input type="checkbox"><span></span>';
    var checkbox = toggle.querySelector('input');
    checkbox.checked = row.enabled;
    checkbox.addEventListener('change', async function () {
      try {
        var data = await patch(detailUrl(row.id), { enabled: checkbox.checked });
        if (data.provider) { row.enabled = data.provider.enabled; }
        await refresh();
        BA.toast((row.name || 'Provider') + (checkbox.checked ? ' enabled.' : ' disabled.'));
      } catch (error) {
        checkbox.checked = !checkbox.checked;
        BA.toast(error.message || 'Could not update the provider.', 'error');
      }
    });
    actions.appendChild(toggle);

    var edit = iconButton('edit', 'Edit provider', function () { openCustomEditor(row); });
    var remove = iconButton('delete', 'Remove provider', function () { askDelete(row); });
    remove.classList.add('ba-provider-danger-icon');
    actions.appendChild(edit);
    actions.appendChild(remove);
    node.appendChild(actions);
    return node;
  }

  function iconButton(icon, title, onClick) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'ba-icon-button ba-icon-button-quiet';
    button.title = title;
    button.setAttribute('aria-label', title);
    button.innerHTML = '<span class="material-symbols-outlined">' + icon + '</span>';
    button.addEventListener('click', onClick);
    return button;
  }

  function renderList() {
    els.list.innerHTML = '';
    els.list.appendChild(sectionHeader('Official APIs', 'Agnes, OpenAI, Anthropic, Gemini, DeepSeek'));
    ((catalog && catalog.official) || []).forEach(function (preset) {
      els.list.appendChild(presetRow(preset, preset.byokProviderId ? rowForPreset(preset.slug) : null));
    });
    els.list.appendChild(sectionHeader('Custom providers', 'Any OpenAI / Anthropic / Gemini compatible endpoint', function () {
      openCustomEditor(null);
    }));
    var custom = providers.filter(function (row) { return row.provider === 'custom'; });
    if (!custom.length) {
      var note = document.createElement('p');
      note.className = 'ba-providers-note';
      note.textContent = 'Point NEBians at local models, gateways or proxies — stored encrypted, used only for your tasks.';
      els.list.appendChild(note);
    }
    custom.forEach(function (row) { els.list.appendChild(customRow(row)); });
  }

  // -------------------------------------------------------------- editor ---

  function testLine() {
    var line = document.createElement('p');
    line.className = 'ba-test-line';
    line.hidden = true;
    return line;
  }

  function showTestResult(line, message, ok) {
    line.hidden = false;
    line.className = 'ba-test-line ' + (ok ? 'ok' : 'bad');
    line.textContent = message;
  }

  function openPresetEditor(preset, row) {
    showEditor();
    var hasRow = Boolean(row);
    var masked = row && row.keyMasked ? row.keyMasked : '';
    els.editor.innerHTML =
      '<h3 class="ba-provider-form-title"></h3>' +
      (preset.freeNote ? '<p class="ba-provider-chip ba-provider-chip-banner"></p>' : '') +
      '<label class="ba-form-field"><span>API key</span>' +
      '<input id="pe-key" type="password" autocomplete="new-password" spellcheck="false"></label>' +
      '<label class="ba-form-field"><span>Default model</span><select id="pe-model"></select></label>' +
      '<label class="ba-form-field"><span>Base URL <small>(optional — overrides the default endpoint)</small></span>' +
      '<input id="pe-url" type="url" spellcheck="false"></label>';
    els.editor.querySelector('.ba-provider-form-title').textContent = preset.label;
    if (preset.freeNote) els.editor.querySelector('.ba-provider-chip-banner').textContent = preset.freeNote;

    var keyInput = els.editor.querySelector('#pe-key');
    keyInput.placeholder = masked ? ('Saved: ' + masked + ' — type to replace') : 'Paste your API key';
    var modelSelect = els.editor.querySelector('#pe-model');
    (preset.models || []).forEach(function (model) {
      var option = document.createElement('option');
      option.value = model.id;
      option.textContent = (model.label || model.id) + (model.note ? (' — ' + model.note) : '');
      modelSelect.appendChild(option);
    });
    var selectedModel = (row && row.defaultModel) || preset.defaultModel || '';
    if (selectedModel && !Array.from(modelSelect.options).some(function (option) { return option.value === selectedModel; })) {
      var custom = document.createElement('option');
      custom.value = selectedModel;
      custom.textContent = selectedModel;
      modelSelect.appendChild(custom);
    }
    modelSelect.value = selectedModel || modelSelect.value;
    var urlInput = els.editor.querySelector('#pe-url');
    urlInput.placeholder = preset.baseUrl || 'https://';
    urlInput.value = (row && row.baseUrl) || '';

    var resultLine = testLine();
    els.editor.appendChild(resultLine);
    var actions = document.createElement('div');
    actions.className = 'ba-dialog-actions ba-provider-editor-actions';
    if (hasRow) {
      var remove = document.createElement('button');
      remove.type = 'button';
      remove.className = 'ba-text-button ba-provider-danger';
      remove.innerHTML = '<span class="material-symbols-outlined">delete</span><span>Remove saved key</span>';
      remove.addEventListener('click', function () { askDelete(row); });
      actions.appendChild(remove);
    }
    var testButton = document.createElement('button');
    testButton.type = 'button';
    testButton.className = 'ba-button ba-button-secondary';
    testButton.innerHTML = '<span>Test connection</span>';
    var saveButton = document.createElement('button');
    saveButton.type = 'button';
    saveButton.className = 'ba-button ba-button-primary';
    saveButton.innerHTML = '<span>Save key</span>';
    actions.appendChild(testButton);
    actions.appendChild(saveButton);
    els.editor.appendChild(actions);

    function refreshTestState() {
      testButton.disabled = !(hasRow || keyInput.value.trim());
    }
    keyInput.addEventListener('input', refreshTestState);
    refreshTestState();

    testButton.addEventListener('click', async function () {
      setBusy(testButton, true);
      resultLine.hidden = true;
      try {
        var payload;
        var key = keyInput.value.trim();
        if (hasRow && !key) {
          payload = { providerId: row.id };
        } else {
          payload = { provider: preset.slug, model: modelSelect.value };
          if (key) payload.apiKey = key;
          if (urlInput.value.trim()) payload.baseUrl = urlInput.value.trim();
        }
        var data = await postJson(testUrl, payload);
        showTestResult(resultLine, 'Connected to ' + (data.model || 'provider') + ' in ' + (data.latencyMs || '?') + ' ms.', true);
      } catch (error) {
        showTestResult(resultLine, 'Test failed: ' + testErrorMessage(error), false);
      } finally {
        setBusy(testButton, false);
        refreshTestState();
      }
    });

    saveButton.addEventListener('click', async function () {
      var key = keyInput.value.trim();
      if (!hasRow && !key) {
        showTestResult(resultLine, 'Paste your API key first.', false);
        return;
      }
      var fields = {};
      if (key) fields.apiKey = key;
      if (modelSelect.value) fields.defaultModel = modelSelect.value;
      if (urlInput.value.trim()) fields.baseUrl = urlInput.value.trim();
      setBusy(saveButton, true);
      try {
        if (hasRow) {
          await patch(detailUrl(row.id), fields);
        } else {
          fields.provider = preset.slug;
          await BA.json(providersUrl, fields);
        }
        await refresh();
        showList();
        BA.toast(preset.label + ' key saved.');
      } catch (error) {
        showTestResult(resultLine, error.message || 'Could not save.', false);
      } finally {
        setBusy(saveButton, false);
      }
    });
  }

  function openCustomEditor(row) {
    showEditor();
    var creating = !row;
    els.editor.innerHTML =
      '<h3 class="ba-provider-form-title"></h3>' +
      '<label class="ba-form-field"><span>Name</span><input id="ce-name" type="text" maxlength="100" placeholder="My provider"></label>' +
      '<label class="ba-form-field"><span>API format</span><select id="ce-format">' +
      '<option value="openai">OpenAI compatible (/chat/completions)</option>' +
      '<option value="anthropic">Anthropic Messages (x-api-key)</option>' +
      '<option value="gemini">Gemini generateContent</option>' +
      '</select></label>' +
      '<label class="ba-form-field"><span>Base URL</span><input id="ce-url" type="url" spellcheck="false" placeholder="https://api.example.com/v1"></label>' +
      '<label class="ba-form-field"><span>API key</span><input id="ce-key" type="password" autocomplete="new-password" spellcheck="false"></label>' +
      '<label class="ba-form-field"><span>Models <small>(comma separated)</small></span><textarea id="ce-models" rows="2" spellcheck="false" placeholder="gpt-5.4-mini, claude-sonnet-5"></textarea></label>' +
      '<label class="ba-form-field"><span>Default model <small>(optional)</small></span><input id="ce-default" type="text" spellcheck="false"></label>' +
      '<div class="ba-form-inline">' +
      '<label class="ba-form-field"><span>Context window</span><input id="ce-context" type="number" min="1024"></label>' +
      '<label class="ba-form-field"><span>Max output tokens</span><input id="ce-maxout" type="number" min="256"></label>' +
      '</div>';
    els.editor.querySelector('.ba-provider-form-title').textContent = creating ? 'Add custom provider' : ('Edit ' + (row.name || 'provider'));
    var nameInput = els.editor.querySelector('#ce-name');
    var formatSelect = els.editor.querySelector('#ce-format');
    var urlInput = els.editor.querySelector('#ce-url');
    var keyInput = els.editor.querySelector('#ce-key');
    var modelsInput = els.editor.querySelector('#ce-models');
    var defaultInput = els.editor.querySelector('#ce-default');
    var contextInput = els.editor.querySelector('#ce-context');
    var maxoutInput = els.editor.querySelector('#ce-maxout');

    nameInput.value = (row && row.name) || '';
    formatSelect.value = (row && row.apiFormat) || 'openai';
    urlInput.value = (row && row.baseUrl) || '';
    keyInput.placeholder = (row && row.keyMasked) ? ('Saved: ' + row.keyMasked + ' — type to replace') : 'sk-...';
    modelsInput.value = (row && row.models.join(', ')) || '';
    defaultInput.value = (row && row.defaultModel) || '';
    defaultInput.placeholder = 'first model is used';
    contextInput.value = String((row && row.contextWindow) || 131072);
    maxoutInput.value = String((row && row.maxOutputTokens) || 4096);

    function parsedModels() {
      return modelsInput.value.split(',').map(function (value) { return value.trim(); }).filter(Boolean).slice(0, 40);
    }
    function chosenModel() { return defaultInput.value.trim() || parsedModels()[0] || ''; }
    function baseUrlOk() {
      var url = urlInput.value.trim();
      return !url || url.startsWith('http://') || url.startsWith('https://');
    }

    var resultLine = testLine();
    els.editor.appendChild(resultLine);
    var actions = document.createElement('div');
    actions.className = 'ba-dialog-actions ba-provider-editor-actions';
    var testButton = document.createElement('button');
    testButton.type = 'button';
    testButton.className = 'ba-button ba-button-secondary';
    testButton.innerHTML = '<span>Test connection</span>';
    var saveButton = document.createElement('button');
    saveButton.type = 'button';
    saveButton.className = 'ba-button ba-button-primary';
    saveButton.innerHTML = '<span>' + (creating ? 'Add provider' : 'Save changes') + '</span>';
    actions.appendChild(testButton);
    actions.appendChild(saveButton);
    els.editor.appendChild(actions);

    testButton.addEventListener('click', async function () {
      if (!baseUrlOk()) { showTestResult(resultLine, 'Base URL must start with http:// or https://', false); return; }
      var key = keyInput.value.trim();
      var payload;
      if (!creating && !key) {
        payload = { providerId: row.id };
      } else {
        payload = {
          provider: 'custom',
          apiFormat: formatSelect.value,
          model: chosenModel()
        };
        if (urlInput.value.trim()) payload.baseUrl = urlInput.value.trim();
        if (key) payload.apiKey = key;
        if (!payload.baseUrl) { showTestResult(resultLine, 'Enter the base URL first.', false); return; }
        if (!payload.model) { showTestResult(resultLine, 'Add at least one model id first.', false); return; }
      }
      setBusy(testButton, true);
      resultLine.hidden = true;
      try {
        var data = await postJson(testUrl, payload);
        showTestResult(resultLine, 'Connected to ' + (data.model || 'provider') + ' in ' + (data.latencyMs || '?') + ' ms.', true);
      } catch (error) {
        showTestResult(resultLine, 'Test failed: ' + testErrorMessage(error), false);
      } finally {
        setBusy(testButton, false);
      }
    });

    saveButton.addEventListener('click', async function () {
      var models = parsedModels();
      var url = urlInput.value.trim();
      if (creating) {
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
          showTestResult(resultLine, 'Base URL must start with http:// or https://', false);
          return;
        }
        if (!models.length) {
          showTestResult(resultLine, 'Add at least one model id.', false);
          return;
        }
      } else if (!baseUrlOk()) {
        showTestResult(resultLine, 'Base URL must start with http:// or https://', false);
        return;
      }
      var fields = {
        provider: 'custom',
        apiFormat: formatSelect.value
      };
      if (nameInput.value.trim()) fields.name = nameInput.value.trim();
      if (url) fields.baseUrl = url;
      var key = keyInput.value.trim();
      if (key) fields.apiKey = key;
      if (defaultInput.value.trim()) fields.defaultModel = defaultInput.value.trim();
      if (parseInt(contextInput.value, 10)) fields.contextWindow = parseInt(contextInput.value, 10);
      if (parseInt(maxoutInput.value, 10)) fields.maxOutputTokens = parseInt(maxoutInput.value, 10);
      if (creating || models.length) fields.models = models;
      setBusy(saveButton, true);
      try {
        if (creating) {
          await BA.json(providersUrl, fields);
        } else {
          await patch(detailUrl(row.id), fields);
        }
        await refresh();
        showList();
        BA.toast(creating ? 'Provider added.' : 'Provider updated.');
      } catch (error) {
        showTestResult(resultLine, error.message || 'Could not save.', false);
      } finally {
        setBusy(saveButton, false);
      }
    });
  }

  // -------------------------------------------------------------- delete ---

  function askDelete(row) {
    pendingDelete = row;
    if (row.provider === 'custom') {
      els.deleteTitle.textContent = 'Remove provider?';
      els.deleteCopy.textContent = '"' + (row.name || 'Custom provider') + '" and its API key will be permanently removed from your account.';
    } else {
      els.deleteTitle.textContent = 'Remove saved key?';
      els.deleteCopy.textContent = 'Your saved ' + row.provider + ' API key will be removed. Server-managed keys remain available.';
    }
    els.deleteDialog.showModal();
  }

  els.deleteCancel.addEventListener('click', function () { pendingDelete = null; els.deleteDialog.close(); });
  els.deleteConfirm.addEventListener('click', async function () {
    var row = pendingDelete;
    if (!row) { els.deleteDialog.close(); return; }
    setBusy(els.deleteConfirm, true);
    try {
      await BA.api(detailUrl(row.id), { method: 'DELETE' });
      pendingDelete = null;
      els.deleteDialog.close();
      await refresh();
      showList();
      BA.toast('Provider removed.');
    } catch (error) {
      BA.toast(error.message || 'Could not remove the provider.', 'error');
    } finally {
      setBusy(els.deleteConfirm, false);
    }
  });

  // --------------------------------------------------------------- wiring ---

  if (els.open) {
    els.open.addEventListener('click', function () {
      showList();
      els.dialog.showModal();
      refresh();
    });
  }
  // The settings gear lives inside the model menu (rendered after this file
  // loads) — delegate so we always catch it.
  document.addEventListener('click', function (event) {
    var btn = event.target.closest && event.target.closest('.ba-mm-settings');
    if (btn) {
      showList();
      els.dialog.showModal();
      refresh();
    }
  });
  els.close.addEventListener('click', function () { els.dialog.close(); });
  els.back.addEventListener('click', function () { showList(); });

  // "Add key" from the model picker — jump straight into that provider's editor.
  var pendingFocusSlug = null;
  document.addEventListener('ba:llm-open-settings', function (event) {
    var slug = event.detail && event.detail.slug;
    pendingFocusSlug = slug || null;
    showList();
    els.dialog.showModal();
    refresh();
  });
  var originalRenderList = renderList;
  renderList = function () {
    originalRenderList();
    if (pendingFocusSlug && catalog) {
      var preset = ((catalog.official) || []).find(function (p) { return p.slug === pendingFocusSlug; });
      if (preset) openPresetEditor(preset, rowForPreset(preset.slug));
      pendingFocusSlug = null;
    }
  };
  if (catalog) renderList();
})();
