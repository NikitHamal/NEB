/* ── Marketplace: the price setter and the studio editor ─────────────────────
 * Two small, independent controllers:
 *
 *   NebPrice   — upgrades the server-rendered price setter (free/paid modes,
 *                preset chips, the live "you receive" line). It never invents a
 *                value: everything it writes the server re-validates.
 *   NebStudio  — the block builder, course/update forms and the JSON saves.
 *
 * Everything is fetched with the CSRF token the template rendered, and every
 * failure is surfaced in the page's toast rather than in the console.
 */
(function () {
  'use strict';

  function readJson(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return null;
    }
  }

  function money(value) {
    var amount = parseFloat(value || 0);
    if (isNaN(amount)) return '0';
    var fixed = Math.round(amount * 100) / 100;
    return (fixed % 1 === 0) ? String(fixed) : fixed.toFixed(2);
  }

  function groupThousands(text) {
    var parts = String(text).split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return parts.join('.');
  }

  /* ── Price setter ──────────────────────────────────────────────────────── */
  function initPriceSetter(root) {
    if (root.dataset.nebPriceReady) return;
    root.dataset.nebPriceReady = '1';

    var modes = root.querySelectorAll('[data-neb-price-mode]');
    var flag = root.querySelector('[data-neb-price-flag]');
    var amountWrap = root.querySelector('[data-neb-price-amount]');
    var field = root.querySelector('[data-neb-price-field]');
    var earnings = root.querySelector('[data-neb-price-earnings]');
    var presets = root.querySelectorAll('[data-neb-price-preset]');
    var commission = parseFloat(root.dataset.commission || '0') || 0;

    function isPaid() {
      var checked = root.querySelector('[data-neb-price-mode]:checked');
      return !!checked && checked.value === 'paid';
    }

    function refresh() {
      var paid = isPaid();
      if (flag) flag.value = paid ? '1' : '0';
      if (amountWrap) amountWrap.hidden = !paid;
      root.classList.toggle('is-unset', paid && !(parseFloat(field && field.value) > 0));
      if (field) field.required = paid;

      var price = parseFloat(field && field.value) || 0;
      if (earnings) {
        if (!paid) {
          earnings.textContent = 'Free for every Nebian.';
        } else if (price > 0) {
          var keeps = price - (price * commission) / 100;
          earnings.textContent =
            'You receive Rs. ' + groupThousands(money(keeps)) +
            ' per sale after the ' + commission + '% platform fee.';
        } else {
          earnings.textContent = '';
        }
      }
      presets.forEach(function (chip) {
        var chosen = paid && parseFloat(chip.dataset.nebPricePreset) === price;
        chip.classList.toggle('is-chosen', !!chosen);
      });
    }

    modes.forEach(function (input) {
      input.addEventListener('change', refresh);
    });

    if (field) {
      field.addEventListener('input', refresh);
    }

    presets.forEach(function (chip) {
      chip.addEventListener('click', function () {
        if (!field) return;
        field.value = chip.dataset.nebPricePreset;
        refresh();
      });
    });

    refresh();
  }

  /* ── Studio ────────────────────────────────────────────────────────────── */
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
    payload.style = style;
    payload.style.gallery_columns = parseInt(payload.style.gallery_columns, 10) || 3;
    payload.style.show_stats = true;
    payload.style.show_contact = true;

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

  /* ── Courses ───────────────────────────────────────────────────────────── */
  NebStudio.prototype.courseField = function (key) {
    return this.root.querySelector('[data-mkt-course-field="' + key + '"]');
  };

  NebStudio.prototype.bindCourses = function () {
    var self = this;

    this.root.querySelectorAll('[data-mkt-course-edit]').forEach(function (button) {
      button.addEventListener('click', function () {
        self.loadCourse(button.dataset.mktCourseEdit);
      });
    });

    this.root.querySelectorAll('[data-mkt-course-delete]').forEach(function (button) {
      button.addEventListener('click', function () {
        if (!window.confirm('Remove this offering? Buyers keep the access they already paid for.')) return;
        self.post(self.root.dataset.courseDeleteUrl, { id: button.dataset.mktCourseDelete })
          .then(function (data) {
            var row = self.root.querySelector('[data-mkt-course-row="' + button.dataset.mktCourseDelete + '"]');
            if (row) row.remove();
            self.courses = self.courses.filter(function (c) { return c.id !== button.dataset.mktCourseDelete; });
            self.toast(data.message || 'Course removed.');
          })
          .catch(function (error) { self.toast(error.message, true); });
      });
    });

    var save = this.root.querySelector('[data-mkt-save-course]');
    if (save) {
      save.addEventListener('click', function () { self.saveCourse(save); });
    }

    var reset = this.root.querySelector('[data-mkt-course-reset]');
    if (reset) {
      reset.addEventListener('click', function () { self.resetCourseForm(); });
    }
  };

  NebStudio.prototype.resetCourseForm = function () {
    var self = this;
    this.courseField('id').value = '';
    ['title', 'summary', 'description', 'level', 'duration_label', 'tags', 'cover_url'].forEach(function (key) {
      var field = self.courseField(key);
      if (field) field.value = '';
    });
    this.courseField('lesson_count').value = '0';
    this.courseField('seat_limit').value = '0';
    this.courseField('includes').value = '';
    this.courseField('status').value = 'draft';
    this.courseField('featured').checked = false;
    var paidMode = this.root.querySelector('[data-mkt-course-price] [data-neb-price-mode][value="free"]');
    if (paidMode) paidMode.checked = true;
    var priceField = this.priceField();
    if (priceField) priceField.value = '';
    this.root.querySelectorAll('[data-mkt-course-resource]').forEach(function (box) { box.checked = false; });
    var title = this.root.querySelector('[data-mkt-course-form-title]');
    if (title) title.textContent = 'New offering';
    var price = this.root.querySelector('[data-mkt-course-price]');
    if (price) initPriceSetter(price);
    var mode = this.root.querySelector('[data-mkt-course-price] [data-neb-price-mode]:checked');
    if (mode) mode.dispatchEvent(new Event('change'));
  };

  NebStudio.prototype.priceField = function () {
    var wrapper = this.root.querySelector('[data-mkt-course-price]') || this.root;
    return wrapper.querySelector('[data-neb-price-field]');
  };

  NebStudio.prototype.priceWrapper = function () {
    return this.root.querySelector('[data-mkt-course-price]');
  };

  NebStudio.prototype.loadCourse = function (id) {
    var self = this;
    var course = null;
    this.courses.forEach(function (entry) { if (entry.id === id) course = entry; });
    if (!course) return;

    this.courseField('id').value = course.id;
    ['title', 'summary', 'description', 'level', 'duration_label', 'tags', 'cover_url'].forEach(function (key) {
      var field = self.courseField(key);
      if (field) field.value = course[key] || '';
    });
    this.courseField('lesson_count').value = course.lesson_count || 0;
    this.courseField('seat_limit').value = course.seat_limit || 0;
    this.courseField('includes').value = (course.includes || []).join('\n');
    this.courseField('status').value = course.status || 'draft';
    this.courseField('featured').checked = !!course.featured;

    var wrapper = this.root.querySelector('[data-mkt-course-price]');
    if (wrapper) {
      var modeValue = course.is_free ? 'free' : 'paid';
      var mode = wrapper.querySelector('[data-neb-price-mode][value="' + modeValue + '"]');
      if (mode) mode.checked = true;
      var priceField = wrapper.querySelector('[data-neb-price-field]');
      if (priceField) priceField.value = course.is_free ? '' : course.price;
      var refresh = wrapper.querySelector('[data-neb-price-mode]:checked');
      if (refresh) refresh.dispatchEvent(new Event('change'));
    }

    var attached = this.courseResources[course.id] || [];
    this.root.querySelectorAll('[data-mkt-course-resource]').forEach(function (box) {
      box.checked = attached.indexOf(box.dataset.mktCourseResource) !== -1;
    });

    var title = this.root.querySelector('[data-mkt-course-form-title]');
    if (title) title.textContent = 'Edit offering';
    var panel = this.root.querySelector('[data-mkt-panel="courses"]');
    if (panel) panel.scrollIntoView({ block: 'start' });
  };

  NebStudio.prototype.saveCourse = function (button) {
    var self = this;
    var wrapper = this.root.querySelector('[data-mkt-course-price]');
    var paid = wrapper && wrapper.querySelector('[data-neb-price-mode][value="paid"]').checked;

    var payload = {
      id: this.courseField('id').value || undefined,
      is_free: !paid,
      includes: this.courseField('includes').value.split('\n').map(function (line) {
        return line.trim();
      }).filter(Boolean),
      featured: this.courseField('featured').checked,
      resource_ids: []
    };

    this.root.querySelectorAll('[data-mkt-course-resource]').forEach(function (box) {
      if (box.checked) payload.resource_ids.push(box.dataset.mktCourseResource);
    });

    ['title', 'summary', 'description', 'level', 'duration_label', 'tags', 'cover_url', 'status'].forEach(function (key) {
      payload[key] = self.courseField(key).value;
    });
    payload.lesson_count = parseInt(this.courseField('lesson_count').value, 10) || 0;
    payload.seat_limit = parseInt(this.courseField('seat_limit').value, 10) || 0;

    if (paid) {
      var price = parseFloat(this.priceField().value);
      if (!(price > 0)) {
        this.toast('Enter a price above Rs. 0 for a paid offering.', true);
        return;
      }
      payload.price = price;
    }

    if (button) button.disabled = true;
    this.post(this.root.dataset.courseSaveUrl, payload)
      .then(function (data) {
        self.toast(data.message || 'Course saved.');
        if (data.course) {
          var replaced = false;
          self.courses = self.courses.map(function (entry) {
            if (entry.id === data.course.id) {
              replaced = true;
              return data.course;
            }
            return entry;
          });
          if (!replaced) self.courses.push(data.course);
        }
        window.location.reload();
      })
      .catch(function (error) { self.toast(error.message, true); })
      .finally(function () { if (button) button.disabled = false; });
  };

  /* ── Updates ───────────────────────────────────────────────────────────── */
  NebStudio.prototype.postField = function (key) {
    return this.root.querySelector('[data-mkt-post-field="' + key + '"]');
  };

  NebStudio.prototype.bindPosts = function () {
    var self = this;

    this.root.querySelectorAll('[data-mkt-post-edit]').forEach(function (button) {
      button.addEventListener('click', function () {
        self.loadPost(button.dataset.mktPostEdit);
      });
    });

    this.root.querySelectorAll('[data-mkt-post-delete]').forEach(function (button) {
      button.addEventListener('click', function () {
        if (!window.confirm('Remove this update?')) return;
        self.post(self.root.dataset.postDeleteUrl, { id: button.dataset.mktPostDelete })
          .then(function (data) {
            var row = self.root.querySelector('[data-mkt-post-row="' + button.dataset.mktPostDelete + '"]');
            if (row) row.remove();
            self.toast(data.message || 'Update removed.');
          })
          .catch(function (error) { self.toast(error.message, true); });
      });
    });

    var save = this.root.querySelector('[data-mkt-save-post]');
    if (save) {
      save.addEventListener('click', function () { self.savePost(save); });
    }

    var reset = this.root.querySelector('[data-mkt-post-reset]');
    if (reset) {
      reset.addEventListener('click', function () {
        self.postField('id').value = '';
        ['title', 'body', 'media_url', 'link_url'].forEach(function (key) {
          self.postField(key).value = '';
        });
        self.postField('pinned').checked = false;
        self.postField('published').checked = true;
        var title = self.root.querySelector('[data-mkt-post-form-title]');
        if (title) title.textContent = 'New update';
      });
    }
  };

  NebStudio.prototype.loadPost = function (id) {
    var self = this;
    var post = null;
    this.posts.forEach(function (entry) { if (entry.id === id) post = entry; });
    if (!post) return;
    this.postField('id').value = post.id;
    ['title', 'body', 'media_url', 'link_url'].forEach(function (key) {
      self.postField(key).value = post[key] || '';
    });
    this.postField('pinned').checked = !!post.pinned;
    this.postField('published').checked = post.published !== false;
    var title = this.root.querySelector('[data-mkt-post-form-title]');
    if (title) title.textContent = 'Edit update';
  };

  NebStudio.prototype.savePost = function (button) {
    var self = this;
    var payload = {
      id: this.postField('id').value || undefined,
      pinned: this.postField('pinned').checked,
      published: this.postField('published').checked
    };
    ['title', 'body', 'media_url', 'link_url'].forEach(function (key) {
      payload[key] = self.postField(key).value;
    });
    if (!payload.body.trim() && !payload.title.trim()) {
      this.toast('Write something first.', true);
      return;
    }

    if (button) button.disabled = true;
    this.post(this.root.dataset.postSaveUrl, payload)
      .then(function (data) {
        self.toast(data.message || 'Update posted.');
        window.location.reload();
      })
      .catch(function (error) { self.toast(error.message, true); })
      .finally(function () { if (button) button.disabled = false; });
  };

  /* ── Withdrawals ───────────────────────────────────────────────────────── */
  NebStudio.prototype.bindWithdraw = function () {
    var self = this;
    var form = this.root.querySelector('[data-mkt-withdraw]');
    if (!form) return;
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var button = form.querySelector('button[type="submit"]');
      if (button) button.disabled = true;
      fetch(form.action, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': self.csrf,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: data
      })
        .then(function (response) {
          return response.json().catch(function () { return {}; }).then(function (payload) {
            if (!response.ok || payload.status === 'error') {
              throw new Error(payload.error || 'Could not submit that request.');
            }
            return payload;
          });
        })
        .then(function () {
          self.toast('Withdrawal requested. Our team reviews it within 7 days.');
          window.setTimeout(function () { window.location.reload(); }, 900);
        })
        .catch(function (error) { self.toast(error.message, true); })
        .finally(function () { if (button) button.disabled = false; });
    });
  };

  /* ── Boot ──────────────────────────────────────────────────────────────── */
  function boot() {
    document.querySelectorAll('[data-neb-price]').forEach(initPriceSetter);

    var studio = document.getElementById('mkt-studio');
    if (studio) new NebStudio(studio);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  document.body.addEventListener('htmx:afterSwap', function (event) {
    if (!event.detail || !event.detail.target) return;
    event.detail.target.querySelectorAll('[data-neb-price]').forEach(initPriceSetter);
  });
})();
