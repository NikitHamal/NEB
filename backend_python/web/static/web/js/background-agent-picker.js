(function () {
  'use strict';

  var BA = window.BA;
  if (!BA) return;

  var pickerCounter = 0;
  var activePicker = null;

  function element(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function createPicker(config) {
    var root = config.root;
    if (!root) throw new Error('Picker root is required.');

    var id = 'ba-picker-' + (++pickerCounter);
    var labelText = config.label || root.dataset.label || 'Select';
    var placeholder = config.placeholder || root.dataset.placeholder || 'Select an option';
    var iconName = config.icon || root.dataset.icon || 'expand_circle_down';
    var searchPlaceholder = config.searchPlaceholder || root.dataset.searchPlaceholder || 'Search';
    var searchable = config.searchable !== false;
    var options = [];
    var selectedValue = '';
    var disabled = false;
    var open = false;

    root.innerHTML = '';
    var label = element('span', 'ba-field-label', labelText);
    var trigger = element('button', 'ba-picker-trigger');
    trigger.type = 'button';
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.setAttribute('aria-controls', id);

    var leading = element('span', 'material-symbols-outlined ba-picker-leading', iconName);
    var valueNode = element('span', 'ba-picker-value', placeholder);
    var chevron = element('span', 'material-symbols-outlined ba-picker-chevron', 'expand_more');
    trigger.append(leading, valueNode, chevron);
    root.append(label, trigger);

    var popover = element('div', 'ba-picker-popover');
    popover.id = id;
    popover.hidden = true;
    popover.setAttribute('data-ba-picker-popover', '');

    var searchWrap = element('div', 'ba-picker-search');
    var searchIcon = element('span', 'material-symbols-outlined', 'search');
    var searchInput = element('input');
    searchInput.type = 'search';
    searchInput.autocomplete = 'off';
    searchInput.placeholder = searchPlaceholder;
    searchInput.setAttribute('aria-label', searchPlaceholder);
    searchWrap.append(searchIcon, searchInput);
    if (!searchable) searchWrap.hidden = true;

    var list = element('div', 'ba-picker-options');
    list.setAttribute('role', 'listbox');
    list.setAttribute('aria-labelledby', id + '-label');
    label.id = id + '-label';
    popover.append(searchWrap, list);

    var portalHost = root.closest('dialog') || document.body;
    portalHost.appendChild(popover);

    function selectedOption() {
      return options.find(function (option) { return String(option.value) === selectedValue; }) || null;
    }

    function syncTrigger() {
      var selected = selectedOption();
      valueNode.textContent = selected ? selected.label : placeholder;
      valueNode.classList.toggle('placeholder', !selected);
      trigger.disabled = disabled;
      trigger.classList.toggle('has-value', Boolean(selected));
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
      chevron.textContent = open ? 'expand_less' : 'expand_more';
    }

    function positionPopover() {
      if (!open) return;
      var rect = trigger.getBoundingClientRect();
      var viewportPadding = 12;
      var desiredWidth = Math.max(rect.width, Number(config.minWidth || 260));
      var width = Math.min(desiredWidth, window.innerWidth - viewportPadding * 2);
      var left = Math.min(Math.max(viewportPadding, rect.left), window.innerWidth - width - viewportPadding);
      popover.style.width = width + 'px';
      popover.style.left = left + 'px';

      var measuredHeight = Math.min(popover.scrollHeight || 320, Number(config.maxHeight || 360));
      var spaceBelow = window.innerHeight - rect.bottom - viewportPadding;
      var spaceAbove = rect.top - viewportPadding;
      if (spaceBelow < measuredHeight && spaceAbove > spaceBelow) {
        popover.classList.add('opens-up');
        popover.style.top = Math.max(viewportPadding, rect.top - measuredHeight - 7) + 'px';
      } else {
        popover.classList.remove('opens-up');
        popover.style.top = Math.min(window.innerHeight - measuredHeight - viewportPadding, rect.bottom + 7) + 'px';
      }
    }

    function optionSearchText(option) {
      return [option.label, option.meta, option.badge, option.keywords].filter(Boolean).join(' ').toLowerCase();
    }

    function visibleOptionButtons() {
      return Array.from(list.querySelectorAll('.ba-picker-option:not([hidden])'));
    }

    function focusOption(index) {
      var buttons = visibleOptionButtons();
      if (!buttons.length) return;
      var safeIndex = Math.max(0, Math.min(index, buttons.length - 1));
      buttons[safeIndex].focus();
    }

    function choose(value, emit) {
      var next = String(value == null ? '' : value);
      if (next && !options.some(function (option) { return String(option.value) === next; })) next = '';
      var changed = next !== selectedValue;
      selectedValue = next;
      syncTrigger();
      renderOptions(searchInput.value);
      close();
      if (emit !== false && changed && typeof config.onChange === 'function') config.onChange(selectedValue, selectedOption());
    }

    function renderOptions(query) {
      var normalized = String(query || '').trim().toLowerCase();
      list.innerHTML = '';
      var filtered = options.filter(function (option) { return !normalized || optionSearchText(option).includes(normalized); });

      if (!filtered.length) {
        var empty = element('div', 'ba-picker-empty');
        empty.append(element('span', 'material-symbols-outlined', 'search_off'), element('span', '', options.length ? 'No matching options' : 'No options available'));
        list.appendChild(empty);
        return;
      }

      filtered.forEach(function (option) {
        var value = String(option.value);
        var button = element('button', 'ba-picker-option');
        button.type = 'button';
        button.setAttribute('role', 'option');
        button.setAttribute('aria-selected', value === selectedValue ? 'true' : 'false');
        button.dataset.value = value;

        var optionIcon = element('span', 'ba-picker-option-icon material-symbols-outlined', option.icon || iconName);
        var copy = element('span', 'ba-picker-option-copy');
        var titleRow = element('span', 'ba-picker-option-title');
        titleRow.appendChild(element('strong', '', option.label));
        if (option.badge) titleRow.appendChild(element('em', '', option.badge));
        copy.appendChild(titleRow);
        if (option.meta) copy.appendChild(element('small', '', option.meta));
        var check = element('span', 'ba-picker-option-check material-symbols-outlined', 'check');
        button.append(optionIcon, copy, check);
        button.addEventListener('click', function () { choose(value, true); });
        button.addEventListener('keydown', function (event) {
          var buttons = visibleOptionButtons();
          var index = buttons.indexOf(button);
          if (event.key === 'ArrowDown') { event.preventDefault(); focusOption(index + 1); }
          else if (event.key === 'ArrowUp') { event.preventDefault(); if (index === 0 && searchable) searchInput.focus(); else focusOption(index - 1); }
          else if (event.key === 'Home') { event.preventDefault(); focusOption(0); }
          else if (event.key === 'End') { event.preventDefault(); focusOption(buttons.length - 1); }
          else if (event.key === 'Escape') { event.preventDefault(); close(true); }
        });
        list.appendChild(button);
      });
    }

    function openPicker() {
      if (disabled || open) return;
      if (activePicker && activePicker !== api) activePicker.close();
      activePicker = api;
      open = true;
      popover.hidden = false;
      renderOptions('');
      searchInput.value = '';
      syncTrigger();
      requestAnimationFrame(function () {
        positionPopover();
        if (searchable && options.length > 5) searchInput.focus();
        else {
          var selected = list.querySelector('[aria-selected="true"]');
          (selected || list.querySelector('.ba-picker-option'))?.focus();
        }
      });
    }

    function close(returnFocus) {
      if (!open) return;
      open = false;
      popover.hidden = true;
      syncTrigger();
      if (activePicker === api) activePicker = null;
      if (returnFocus) trigger.focus();
    }

    trigger.addEventListener('click', function () { if (open) close(); else openPicker(); });
    trigger.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowDown' || event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openPicker();
      }
    });
    searchInput.addEventListener('input', function () { renderOptions(searchInput.value); positionPopover(); });
    searchInput.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowDown') { event.preventDefault(); focusOption(0); }
      else if (event.key === 'Escape') { event.preventDefault(); close(true); }
    });

    document.addEventListener('pointerdown', function (event) {
      if (open && !root.contains(event.target) && !popover.contains(event.target)) close();
    });
    window.addEventListener('resize', positionPopover);
    window.addEventListener('scroll', positionPopover, true);

    var api = {
      value: function () { return selectedValue; },
      setValue: function (value, emit) { choose(value, emit === true); },
      setOptions: function (items, value) {
        options = (items || []).map(function (item) {
          if (typeof item === 'string') return { value: item, label: item };
          return Object.assign({}, item, { value: String(item.value), label: String(item.label) });
        });
        var nextValue = value !== undefined ? String(value || '') : selectedValue;
        if (nextValue && !options.some(function (option) { return String(option.value) === nextValue; })) nextValue = '';
        selectedValue = nextValue;
        disabled = false;
        renderOptions('');
        syncTrigger();
      },
      setDisabled: function (value) {
        disabled = Boolean(value);
        if (disabled) close();
        syncTrigger();
      },
      setLoading: function (message) {
        close();
        options = [];
        selectedValue = '';
        disabled = true;
        valueNode.textContent = message || 'Loading…';
        valueNode.classList.add('placeholder');
        trigger.disabled = true;
      },
      setPlaceholder: function (value) {
        placeholder = String(value || 'Select an option');
        syncTrigger();
      },
      close: close,
      open: openPicker
    };

    syncTrigger();
    return api;
  }

  BA.createPicker = createPicker;
})();
