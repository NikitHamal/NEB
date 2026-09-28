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

    var addButton = this.root.querySelector('[data-mkt-add-block]');
    if (addButton) {
      addButton.addEventListener('click', function () {
        var select = self.root.querySelector('[data-mkt-add-block-select]');
        self.addBlock(select ? select.value : 'about');
      });
    }

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
    this.blocksWrap.innerHTML = '';

    if (!this.blocks.length) {
      var empty = document.createElement('p');
      empty.className = 'mkt-quiet';
      empty.textContent = 'No sections yet. Add one below — Hero and About are a good start.';
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
        if (field.key === 'title') {
          title.textContent = schema.label + (input.value ? ' — ' + input.value : '');
        }
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

    item.appendChild(body);
    return item;
  };

  window.NebMarket.Studio = NebStudio;
})();
