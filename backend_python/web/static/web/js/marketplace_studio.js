/* ── Marketplace studio: page identity and the block builder ─────────────────
 * The constructor, the save/publish path and the block editor. Course, update
 * and payout forms live in `marketplace_studio_forms.js`, which extends the
 * same prototype and boots it — load this file first.
 *
 * Every fetch carries the CSRF token the template rendered, and every failure
 * is surfaced in the page's toast rather than in the console.
 */
(function () {
  'use strict';

  var readJson = window.NebMarket.readJson;

  function NebStudio(root) {
    this.root = root;
    this.schema = readJson('mkt-block-schema') || [];
    this.blocks = readJson('mkt-blocks-data') || [];
    this.courses = readJson('mkt-courses-data') || [];
    this.posts = readJson('mkt-posts-data') || [];
    this.courseResources = readJson('mkt-course-resources-data') || {};
    this.toastEl = root.querySelector('[data-mkt-toast]');
    this.csrf = (root.querySelector('input[name="csrfmiddlewaretoken"]') || {}).value ||
      (document.querySelector('input[name="csrfmiddlewaretoken"]') || {}).value || '';
    this.blocksWrap = root.querySelector('[data-mkt-blocks]');
    this.bind();
    this.renderBlocks();
  }

  NebStudio.prototype.toast = function (message, isError) {
    if (!this.toastEl) return;
    this.toastEl.textContent = message;
    this.toastEl.classList.toggle('is-error', !!isError);
    this.toastEl.hidden = false;
    window.clearTimeout(this._toastTimer);
    var self = this;
    this._toastTimer = window.setTimeout(function () {
      self.toastEl.hidden = true;
    }, 4200);
  };

  NebStudio.prototype.post = function (url, payload) {
    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrf,
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(payload)
    }).then(function (response) {
      return response.json().catch(function () {
        return { error: 'The server did not answer properly (' + response.status + ').' };
      }).then(function (data) {
        if (!response.ok) {
          throw new Error(data.error || ('Request failed (' + response.status + ')'));
        }
        return data;
      });
    });
  };

  NebStudio.prototype.bind = function () {
    var self = this;

    this.root.querySelectorAll('[data-mkt-tab]').forEach(function (tab) {
      tab.addEventListener('click', function () {
        self.root.querySelectorAll('[data-mkt-tab]').forEach(function (other) {
          other.setAttribute('aria-selected', other === tab ? 'true' : 'false');
        });
        self.root.querySelectorAll('[data-mkt-panel]').forEach(function (panel) {
          panel.hidden = panel.dataset.mktPanel !== tab.dataset.mktTab;
        });
      });
    });

    this.root.querySelectorAll('[data-mkt-save-page]').forEach(function (button) {
      button.addEventListener('click', function () {
        self.savePage(button);
      });
    });

    var publish = this.root.querySelector('[data-mkt-toggle-publish]');
    if (publish) {
      publish.addEventListener('click', function () {
        self.togglePublish(publish);
      });
    }

    var accent = this.root.querySelector('[data-mkt-field="accent_hex"]');
    var accentText = this.root.querySelector('[data-mkt-accent-text]');
    if (accent && accentText) {
      accent.addEventListener('input', function () {
        accentText.value = accent.value.toUpperCase();
        self.root.style.setProperty('--creator-accent', accent.value);
      });
      accentText.addEventListener('change', function () {
        if (/^#[0-9a-fA-F]{6}$/.test(accentText.value.trim())) {
          accent.value = accentText.value.trim();
          self.root.style.setProperty('--creator-accent', accent.value);
        }
      });
    }
    this.root.querySelectorAll('[data-mkt-accent-swatch]').forEach(function (swatch) {
      swatch.addEventListener('click', function () {
        var value = swatch.dataset.mktAccentSwatch;
        if (accent) accent.value = value;
        if (accentText) accentText.value = value;
        self.root.style.setProperty('--creator-accent', value);
      });
    });

    this.bindLook();
    this.bindCourses();
    this.bindPosts();
    this.bindWithdraw();
  };

  NebStudio.prototype.pagePayload = function () {
    var self = this;
    var payload = { blocks: this.blocks };

    this.root.querySelectorAll('[data-mkt-field]').forEach(function (input) {
      var key = input.dataset.mktField;
      if (input.type === 'checkbox') {
        payload[key] = input.checked;
      } else if (key === 'subjects' || key === 'languages') {
        payload[key] = input.value.split(',').map(function (part) { return part.trim(); }).filter(Boolean);
      } else {
        payload[key] = input.value;
      }
    });

    var socials = {};
    this.root.querySelectorAll('[data-mkt-social]').forEach(function (input) {
      if (input.value.trim()) socials[input.dataset.mktSocial] = input.value.trim();
    });
    payload.socials = socials;

    var style = {};
    this.root.querySelectorAll('[data-mkt-style]').forEach(function (input) {
      style[input.dataset.mktStyle] = input.value;
    });
    this.root.querySelectorAll('[data-mkt-style-bool]').forEach(function (input) {
      style[input.dataset.mktStyleBool] = input.checked;
    });
    payload.style = style;
    payload.style.gallery_columns = parseInt(payload.style.gallery_columns, 10) || 3;

    return payload;
  };

  NebStudio.prototype.savePage = function (button) {
    var self = this;
    var url = this.root.dataset.pageSaveUrl;
    if (button) button.disabled = true;
    this.post(url, this.pagePayload())
      .then(function (data) {
        self.toast(data.message || 'Page saved.');
        if (data.page) {
          self.root.style.setProperty('--creator-accent', data.page.accent_hex);
          var slugField = self.root.querySelector('[data-mkt-field="slug"]');
          if (slugField) slugField.value = data.page.slug;
        }
        self.reloadPreview();
      })
      .catch(function (error) { self.toast(error.message, true); })
      .finally(function () { if (button) button.disabled = false; });
  };

  NebStudio.prototype.togglePublish = function (button) {
    var self = this;
    var publish = button.dataset.published !== '1';
    button.disabled = true;
    this.post(this.root.dataset.pageSaveUrl, { published: publish })
      .then(function (data) {
        button.dataset.published = publish ? '1' : '0';
        var label = button.querySelector('[data-mkt-publish-label]');
        if (label) label.textContent = publish ? 'Unpublish' : 'Publish page';
        self.toast(publish ? 'Your page is live.' : 'Your page is a draft again.');
      })
      .catch(function (error) { self.toast(error.message, true); })
      .finally(function () { button.disabled = false; });
  };

  /* ── Blocks ────────────────────────────────────────────────────────────── */
  NebStudio.prototype.schemaFor = function (type) {
    for (var i = 0; i < this.schema.length; i++) {
      if (this.schema[i].type === type) return this.schema[i];
    }
    return null;
  };

  NebStudio.prototype.addBlock = function (type) {
    var schema = this.schemaFor(type);
    if (!schema) return;
    var block = { id: 'b' + Math.random().toString(36).slice(2, 10), type: type, enabled: true };
    schema.fields.forEach(function (field) { block[field.key] = ''; });
    if (schema.list_key) {
      block[schema.list_key] = [];
      if (type === 'stats' || type === 'faq' || type === 'schedule') {
        block[schema.list_key].push({});
      }
    }
    this.blocks.push(block);
    this.renderBlocks();
    this.toast('Section added. Save sections to publish it.');
  };

  NebStudio.prototype.moveBlock = function (index, delta) {
    var target = index + delta;
    if (target < 0 || target >= this.blocks.length) return;
    var moved = this.blocks.splice(index, 1)[0];
    this.blocks.splice(target, 0, moved);
    this.renderBlocks();
  };

  NebStudio.prototype.removeBlock = function (index) {
    this.blocks.splice(index, 1);
    this.renderBlocks();
  };

  NebStudio.prototype.renderBlocks = function () {
    if (!this.blocksWrap) return;
    var self = this;
    if (!this._menuDismiss) {
      this._menuDismiss = true;
      document.addEventListener('click', function () { self.closeMenus(null); });
      document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') self.closeMenus(null);
      });
    }
    this.blocksWrap.innerHTML = '';

    if (!this.blocks.length) {
      var empty = document.createElement('p');
      empty.className = 'mkt-quiet';
      empty.textContent = 'No sections yet. Pick a template above, or add a section — Hero and About are a good start.';
      this.blocksWrap.appendChild(empty);
      return;
    }

    this.blocks.forEach(function (block, index) {
      var schema = self.schemaFor(block.type);
      if (!schema) return;
      self.blocksWrap.appendChild(self.blockNode(block, index, schema));
    });
  };

  NebStudio.prototype.duplicateBlock = function (index) {
    var copy = JSON.parse(JSON.stringify(this.blocks[index]));
    copy.id = 'b' + Math.random().toString(36).slice(2, 10);
    this.blocks.splice(index + 1, 0, copy);
    this.renderBlocks();
    this.toast('Section duplicated.');
  };

  NebStudio.prototype.blockNode = function (block, index, schema) {
    var self = this;
    var item = document.createElement('div');
    item.className = 'mkt-block-item is-collapsed';
    item.dataset.index = String(index);

    var head = document.createElement('div');
    head.className = 'mkt-block-item-head';

    /* The handle is the only draggable part of the row, so a creator can still
       scroll the list with a thumb laid anywhere else on it. Dragging is never
       the only way to reorder -- the overflow menu moves a section up or down
       for anyone using a keyboard, a screen reader, or a small screen where
       dragging across a scrolling list is miserable (WCAG 2.5.1). */
    var handle = document.createElement('span');
    handle.className = 'mkt-block-handle';
    handle.setAttribute('draggable', 'true');
    handle.setAttribute('aria-hidden', 'true');
    handle.innerHTML = '<span class="material-symbols-outlined">drag_indicator</span>';
    this.bindDrag(handle, item, index);

    /* The whole title area opens the section. A 44px-tall target beats a 24px
       chevron on a phone, and the chevron stays as the visual affordance. */
    var titleBtn = document.createElement('button');
    titleBtn.type = 'button';
    titleBtn.className = 'mkt-block-item-title';
    titleBtn.setAttribute('aria-expanded', 'false');

    var titleText = document.createElement('span');
    titleText.className = 'mkt-block-item-name';
    var paintTitle = function () {
      titleText.textContent = block.title || schema.label;
    };
    paintTitle();

    var kind = document.createElement('span');
    kind.className = 'mkt-block-item-kind';
    kind.textContent = schema.label;

    var chevron = document.createElement('span');
    chevron.className = 'material-symbols-outlined mkt-block-chevron';
    chevron.textContent = 'expand_more';

    titleBtn.appendChild(chevron);
    var titleStack = document.createElement('span');
    titleStack.className = 'mkt-block-item-stack';
    titleStack.appendChild(titleText);
    titleStack.appendChild(kind);
    titleBtn.appendChild(titleStack);
    titleBtn.addEventListener('click', function () {
      var open = item.classList.toggle('is-collapsed') === false;
      titleBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    /* Hiding a section keeps everything typed into it; removing it does not.
       The app has had this since day one and the two studios have to agree. */
    var hide = document.createElement('button');
    hide.type = 'button';
    hide.className = 'mkt-icon-btn';
    var paintHide = function () {
      var on = block.enabled !== false;
      hide.innerHTML = '<span class="material-symbols-outlined">' + (on ? 'visibility' : 'visibility_off') + '</span>';
      hide.setAttribute('aria-label', on ? 'Hide this section' : 'Show this section');
      hide.setAttribute('aria-pressed', on ? 'false' : 'true');
      item.classList.toggle('is-hidden', !on);
    };
    hide.addEventListener('click', function () {
      block.enabled = block.enabled === false;
      paintHide();
    });
    paintHide();

    /* One menu instead of a row of five icons. Five icons on a phone either
       wrap or squeeze their labels down to a character apiece, which is the
       exact failure the app row had. */
    var menuWrap = document.createElement('div');
    menuWrap.className = 'mkt-block-menu-wrap';
    var menuBtn = document.createElement('button');
    menuBtn.type = 'button';
    menuBtn.className = 'mkt-icon-btn';
    menuBtn.setAttribute('aria-label', 'More actions for this section');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.innerHTML = '<span class="material-symbols-outlined">more_vert</span>';
    var menu = document.createElement('div');
    menu.className = 'mkt-block-menu';
    menu.hidden = true;

    var addAction = function (icon, label, handler, danger) {
      var action = document.createElement('button');
      action.type = 'button';
      action.className = 'mkt-block-menu-item' + (danger ? ' mkt-danger' : '');
      action.innerHTML = '<span class="material-symbols-outlined">' + icon + '</span>';
      action.appendChild(document.createTextNode(label));
      action.addEventListener('click', function () {
        menu.hidden = true;
        menuBtn.setAttribute('aria-expanded', 'false');
        handler();
      });
      menu.appendChild(action);
      return action;
    };
    var moveUp = addAction('arrow_upward', 'Move up', function () { self.moveBlock(index, -1); });
    var moveDown = addAction('arrow_downward', 'Move down', function () { self.moveBlock(index, 1); });
    if (index === 0) moveUp.disabled = true;
    if (index === this.blocks.length - 1) moveDown.disabled = true;
    addAction('content_copy', 'Duplicate', function () { self.duplicateBlock(index); });
    addAction('delete', 'Remove', function () {
      if (window.confirm('Remove this section and everything in it?')) self.removeBlock(index);
    }, true);

    menuBtn.addEventListener('click', function (event) {
      event.stopPropagation();
      self.closeMenus(menu);
      menu.hidden = !menu.hidden;
      menuBtn.setAttribute('aria-expanded', menu.hidden ? 'false' : 'true');
    });
    menuWrap.appendChild(menuBtn);
    menuWrap.appendChild(menu);

    head.appendChild(handle);
    head.appendChild(titleBtn);
    head.appendChild(hide);
    head.appendChild(menuWrap);
    item.appendChild(head);

    var body = document.createElement('div');
    body.className = 'mkt-block-item-body';

    schema.fields.forEach(function (field) { block[field.key] = ''; });
    if (schema.list_key) {
      block[schema.list_key] = [];
      if (type === 'stats' || type === 'faq' || type === 'schedule') {
        block[schema.list_key].push({});
      }
    }
    this.blocks.push(block);
    this.renderBlocks();
    this.toast('Section added. Save sections to publish it.');
  };

  NebStudio.prototype.moveBlock = function (index, delta) {
    var target = index + delta;
    if (target < 0 || target >= this.blocks.length) return;
    var moved = this.blocks.splice(index, 1)[0];
    this.blocks.splice(target, 0, moved);
    this.renderBlocks();
  };

  NebStudio.prototype.removeBlock = function (index) {
    this.blocks.splice(index, 1);
    this.renderBlocks();
  };

  NebStudio.prototype.renderBlocks = function () {
    if (!this.blocksWrap) return;
    var self = this;
    if (!this._menuDismiss) {
      this._menuDismiss = true;
      document.addEventListener('click', function () { self.closeMenus(null); });
      document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') self.closeMenus(null);
      });
    }
    this.blocksWrap.innerHTML = '';

    if (!this.blocks.length) {
      var empty = document.createElement('p');
      empty.className = 'mkt-quiet';
      empty.textContent = 'No sections yet. Pick a template above, or add a section — Hero and About are a good start.';
      this.blocksWrap.appendChild(empty);
      return;
    }

    this.blocks.forEach(function (block, index) {
      var schema = self.schemaFor(block.type);
      if (!schema) return;
      self.blocksWrap.appendChild(self.blockNode(block, index, schema));
    });
  };

  NebStudio.prototype.blockNode = function (block, index, schema) {
    var self = this;
    var item = document.createElement('div');
    item.className = 'mkt-block-item';

    var head = document.createElement('div');
    head.className = 'mkt-block-item-head';

    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'md-btn md-btn-text';
    toggle.innerHTML = '<span class="material-symbols-outlined">expand_more</span>';
    toggle.addEventListener('click', function () {
      item.classList.toggle('is-collapsed');
    });

    var title = document.createElement('span');
    title.className = 'mkt-block-item-title';
    title.textContent = schema.label + (block.title ? ' — ' + block.title : '');

    var up = document.createElement('button');
    up.type = 'button';
    up.className = 'md-btn md-btn-text';
    up.innerHTML = '<span class="material-symbols-outlined">arrow_upward</span>';
    up.setAttribute('aria-label', 'Move up');
    up.addEventListener('click', function () { self.moveBlock(index, -1); });

    var down = document.createElement('button');
    down.type = 'button';
    down.className = 'md-btn md-btn-text';
    down.innerHTML = '<span class="material-symbols-outlined">arrow_downward</span>';
    down.setAttribute('aria-label', 'Move down');
    down.addEventListener('click', function () { self.moveBlock(index, 1); });

    /* Hiding a section keeps everything typed into it; removing it does not.
       The app has had this since day one and the two studios have to agree. */
    var hide = document.createElement('button');
    hide.type = 'button';
    hide.className = 'md-btn md-btn-text';
    var paintHide = function () {
      var on = block.enabled !== false;
      hide.innerHTML = '<span class="material-symbols-outlined">' + (on ? 'visibility' : 'visibility_off') + '</span>';
      hide.setAttribute('aria-label', on ? 'Hide this section' : 'Show this section');
      hide.setAttribute('aria-pressed', on ? 'false' : 'true');
      item.classList.toggle('is-hidden', !on);
    };
    hide.addEventListener('click', function () {
      block.enabled = block.enabled === false;
      paintHide();
    });
    paintHide();

    var remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'md-btn md-btn-text mkt-danger';
    remove.innerHTML = '<span class="material-symbols-outlined">delete</span>';
    remove.setAttribute('aria-label', 'Remove section');
    remove.addEventListener('click', function () { self.removeBlock(index); });

    head.appendChild(toggle);
    head.appendChild(title);
    head.appendChild(up);
    head.appendChild(down);
    head.appendChild(hide);
    head.appendChild(remove);
    item.appendChild(head);

    var body = document.createElement('div');
    body.className = 'mkt-block-item-body';

    schema.fields.forEach(function (field) {
      var label = document.createElement('label');
      label.className = 'md-label';
      label.textContent = field.label;
      body.appendChild(label);

      var input = document.createElement(field.multiline ? 'textarea' : 'input');
      if (!field.multiline) input.type = 'text';
      input.className = 'md-input';
      input.value = block[field.key] || '';
      input.placeholder = field.url ? 'https://' : '';
      input.addEventListener('input', function () {
        block[field.key] = input.value;
        if (field.key === 'title') paintTitle();
        self.markPreviewStale();
      });
      body.appendChild(input);
    });

    if (schema.list_key) {
      var listWrap = document.createElement('div');
      listWrap.className = 'mkt-blocks';
      var items = block[schema.list_key] || (block[schema.list_key] = []);

      var renderItems = function () {
        listWrap.innerHTML = '';
        if (schema.item_hint) {
          var hint = document.createElement('p');
          hint.className = 'mkt-field-hint';
          hint.textContent = schema.item_hint;
          listWrap.appendChild(hint);
        }

        if (schema.list_key === 'images') {
          var area = document.createElement('textarea');
          area.className = 'md-input';
          area.rows = 3;
          area.value = items.join('\n');
          area.addEventListener('input', function () {
            block[schema.list_key] = area.value.split('\n').map(function (line) {
              return line.trim();
            }).filter(Boolean);
          });
          listWrap.appendChild(area);
          return;
        }

        items.forEach(function (entry, itemIndex) {
          var row = document.createElement('div');
          row.className = 'mkt-block-list-row';
          schema.item_fields.forEach(function (itemField) {
            var input = document.createElement('input');
            input.type = 'text';
            input.className = 'md-input';
            input.placeholder = itemField.label;
            input.value = entry[itemField.key] || '';
            input.addEventListener('input', function () {
              entry[itemField.key] = input.value;
            });
            row.appendChild(input);
          });
          var drop = document.createElement('button');
          drop.type = 'button';
          drop.className = 'md-btn md-btn-text mkt-danger mkt-list-remove';
          drop.textContent = 'Remove item';
          drop.addEventListener('click', function () {
            items.splice(itemIndex, 1);
            renderItems();
          });
          row.appendChild(drop);
          listWrap.appendChild(row);
        });

        var addItem = document.createElement('button');
        addItem.type = 'button';
        addItem.className = 'md-btn md-btn-outlined';
        addItem.textContent = 'Add item';
        addItem.addEventListener('click', function () {
          items.push({});
          renderItems();
        });
        listWrap.appendChild(addItem);
      };

      renderItems();
      body.appendChild(listWrap);
    }

    body.appendChild(this.blockSettings(block, schema));
    item.appendChild(body);
    return item;
  };

  /* ── Per-section settings ────────────────────────────────────────────────
   * The four knobs that make a page look composed rather than assembled: where
   * a section's text sits, how loud its background is, how far it runs, and how
   * many columns its items form. They live behind a summary because most
   * sections want the defaults and a row of four selects on every card would
   * bury the fields that actually carry the writing.
   */
  NebStudio.prototype.blockSettings = function (block, schema) {
    var self = this;
    var theme = (this.editorSchema || {}).theme || {};
    var settings = block.settings || (block.settings = {});

    var wrap = document.createElement('details');
    wrap.className = 'mkt-block-settings';
    var summary = document.createElement('summary');
    summary.innerHTML = '<span class="material-symbols-outlined">tune</span>';
    summary.appendChild(document.createTextNode('Look of this section'));
    wrap.appendChild(summary);

    var grid = document.createElement('div');
    grid.className = 'mkt-settings-grid';

    var addSelect = function (key, label, options, fallback, asNumber) {
      if (!options || !options.length) return;
      var field = document.createElement('div');
      field.className = 'mkt-settings-field';
      var tag = document.createElement('label');
      tag.className = 'md-label';
      tag.textContent = label;
      var select = document.createElement('select');
      select.className = 'md-input';
      options.forEach(function (option) {
        var node = document.createElement('option');
        node.value = String(option.id);
        node.textContent = option.label;
        select.appendChild(node);
      });
      select.value = String(settings[key] != null ? settings[key] : fallback);
      select.addEventListener('change', function () {
        /* The server drops anything that equals the default, so writing the
           default back as a deletion here keeps the two in step and keeps a
           page that never touched these as small on the wire as it was. */
        if (select.value === String(fallback)) delete settings[key];
        else settings[key] = asNumber ? parseInt(select.value, 10) : select.value;
        self.markPreviewStale();
      });
      tag.setAttribute('for', (field.id = 'set-' + block.id + '-' + key));
      select.id = field.id;
      field.appendChild(tag);
      field.appendChild(select);
      grid.appendChild(field);
    };

    addSelect('align', 'Text alignment', theme.block_aligns, 'start');
    addSelect('tone', 'Background', theme.block_tones, 'plain');
    addSelect('width', 'Width', theme.block_widths, 'standard');
    if (schema.list_key && schema.list_key !== 'images') {
      addSelect('columns', 'Columns', [
        { id: 0, label: 'Automatic' }, { id: 1, label: '1' },
        { id: 2, label: '2' }, { id: 3, label: '3' }, { id: 4, label: '4' }
      ], 0, true);
    }

    wrap.appendChild(grid);
    return wrap;
  };

  NebStudio.prototype.closeMenus = function (except) {
    this.root.querySelectorAll('.mkt-block-menu').forEach(function (menu) {
      if (menu === except) return;
      menu.hidden = true;
      var button = menu.parentNode.querySelector('.mkt-icon-btn');
      if (button) button.setAttribute('aria-expanded', 'false');
    });
  };

  /* ── Dragging a section into place ───────────────────────────────────────
   * A live indicator rather than a ghost that lands somewhere surprising: the
   * row you would drop onto grows a rule on the edge you are nearest, so the
   * result is visible before you let go.
   */
  NebStudio.prototype.bindDrag = function (handle, item, index) {
    var self = this;

    handle.addEventListener('dragstart', function (event) {
      self.dragIndex = index;
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.setData('text/plain', String(index));
      if (event.dataTransfer.setDragImage) event.dataTransfer.setDragImage(item, 20, 20);
      window.setTimeout(function () { item.classList.add('is-dragging'); }, 0);
    });

    handle.addEventListener('dragend', function () {
      self.dragIndex = null;
      self.clearDropMarks();
      item.classList.remove('is-dragging');
    });

    item.addEventListener('dragover', function (event) {
      if (self.dragIndex == null || self.dragIndex === index) return;
      event.preventDefault();
      event.dataTransfer.dropEffect = 'move';
      var box = item.getBoundingClientRect();
      var after = event.clientY > box.top + box.height / 2;
      self.clearDropMarks();
      item.classList.add(after ? 'is-drop-after' : 'is-drop-before');
    });

    item.addEventListener('dragleave', function (event) {
      if (item.contains(event.relatedTarget)) return;
      item.classList.remove('is-drop-before', 'is-drop-after');
    });

    item.addEventListener('drop', function (event) {
      if (self.dragIndex == null) return;
      event.preventDefault();
      var after = item.classList.contains('is-drop-after');
      self.clearDropMarks();
      var from = self.dragIndex;
      self.dragIndex = null;
      var to = index + (after ? 1 : 0);
      if (from < to) to -= 1;
      if (from === to) return;
      var moved = self.blocks.splice(from, 1)[0];
      self.blocks.splice(to, 0, moved);
      self.renderBlocks();
      self.markPreviewStale();
    });
  };

  NebStudio.prototype.clearDropMarks = function () {
    this.root.querySelectorAll('.mkt-block-item').forEach(function (node) {
      node.classList.remove('is-drop-before', 'is-drop-after');
    });
  };

  window.NebMarket.Studio = NebStudio;
})();
