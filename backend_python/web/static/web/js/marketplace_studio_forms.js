/* ── Marketplace studio: courses, updates and payouts ────────────────────────
 * Extends the prototype `marketplace_studio.js` defines, then boots the studio.
 * Load order is price → studio → forms.
 */
(function () {
  'use strict';

  var NebStudio = window.NebMarket.Studio;

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
    // The setter inside this wrapper booted itself on page load; re-running the
    // initialiser on the wrapper bound a second set of handlers to the wrong
    // element (and read no `data-commission` off it, so the "you receive" line
    // showed the full price). Dispatching `change` is all a reset needs.
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

    /* The picker only lists the 100 most recent notes, so a note attached before
       that window would be saved away by a ticked-boxes-only payload. Anything
       already attached but not on screen rides along untouched. */
    var listed = {};
    this.root.querySelectorAll('[data-mkt-course-resource]').forEach(function (box) {
      listed[box.dataset.mktCourseResource] = true;
      if (box.checked) payload.resource_ids.push(box.dataset.mktCourseResource);
    });
    (this.courseResources[payload.id] || []).forEach(function (id) {
      if (!listed[id]) payload.resource_ids.push(id);
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

  function boot() {
    var studio = document.getElementById('mkt-studio');
    if (studio) new NebStudio(studio);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
