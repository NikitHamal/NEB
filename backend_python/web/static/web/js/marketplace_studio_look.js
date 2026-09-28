/* ── Marketplace studio: the Look tab, the template gallery and the preview ──
 *
 * Extends the prototype `marketplace_studio.js` defines. Load order is
 * price → studio → look → forms.
 *
 * Everything here is about shortening the loop between a creator changing
 * something and seeing what they changed. Three mechanisms, in order of how
 * fast they are:
 *
 *   1. The studio's own chrome re-tints instantly from the palette table the
 *      server sent, so a palette click is felt before it is saved.
 *   2. The preview iframe reloads after a save, which is the only honest way
 *      to show what a visitor will actually see.
 *   3. A template applies server-side and reloads the editor, because a
 *      template rewrites the sections and the look together and half of that
 *      applied is worse than none of it.
 */
(function () {
  'use strict';

  var NebStudio = window.NebMarket.Studio;
  var readJson = window.NebMarket.readJson;

  NebStudio.prototype.bindLook = function () {
    var self = this;
    this.editorSchema = readJson('mkt-editor-schema') || {};
    this.palettes = {};
    ((this.editorSchema.theme || {}).palettes || []).forEach(function (entry) {
      self.palettes[entry.id] = entry;
    });

    /* Palette swatches. The hidden input is what `pagePayload` reads, so the
       buttons only have to keep it and their own pressed state in step. */
    this.root.querySelectorAll('[data-mkt-palette]').forEach(function (button) {
      button.addEventListener('click', function () {
        self.chooseValue('palette', button.dataset.mktPalette);
        self.root.querySelectorAll('[data-mkt-palette]').forEach(function (other) {
          var on = other === button;
          other.classList.toggle('is-on', on);
          other.setAttribute('aria-checked', on ? 'true' : 'false');
        });
        self.syncAccentToPalette(button.dataset.mktPalette);
      });
    });

    /* Segmented controls: scheme and hero. Same contract as the swatches. */
    this.root.querySelectorAll('[data-mkt-choice]').forEach(function (button) {
      button.addEventListener('click', function () {
        var key = button.dataset.mktChoice;
        self.chooseValue(key, button.dataset.value);
        self.root.querySelectorAll('[data-mkt-choice="' + key + '"]').forEach(function (other) {
          var on = other === button;
          other.classList.toggle('is-on', on);
          other.setAttribute('aria-checked', on ? 'true' : 'false');
        });
      });
    });

    var reset = this.root.querySelector('[data-mkt-accent-reset]');
    if (reset) {
      reset.addEventListener('click', function () {
        var field = self.root.querySelector('[data-mkt-style="palette"]');
        self.syncAccentToPalette(field ? field.value : '');
      });
    }

    this.bindImagePreviews();
    this.bindTemplates();
    this.bindPreview();
  };

  NebStudio.prototype.chooseValue = function (key, value) {
    var field = this.root.querySelector('[data-mkt-style="' + key + '"]');
    if (field) field.value = value;
  };

  /* The accent follows the palette unless a creator has deliberately picked
     their own -- which is exactly the rule the server applies on save, and the
     two have to agree or the colour jumps the moment you press Save. */
  NebStudio.prototype.syncAccentToPalette = function (paletteId) {
    var entry = this.palettes[paletteId];
    if (!entry) return;
    var accent = this.root.querySelector('[data-mkt-field="accent_hex"]');
    var accentText = this.root.querySelector('[data-mkt-accent-text]');
    if (accent) accent.value = entry.accent;
    if (accentText) accentText.value = entry.accent.toUpperCase();
    this.root.style.setProperty('--creator-accent', entry.accent);
  };

  NebStudio.prototype.bindImagePreviews = function () {
    var self = this;
    this.root.querySelectorAll('[data-mkt-image]').forEach(function (input) {
      var key = input.dataset.mktField;
      var target = self.root.querySelector('[data-mkt-preview-for="' + key + '"]');
      if (!target) return;
      var paint = function () {
        var url = input.value.trim();
        if (!url) {
          target.classList.remove('is-broken');
          target.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">'
            + (key === 'avatar_url' ? 'account_circle' : 'image') + '</span>';
          return;
        }
        var img = document.createElement('img');
        img.alt = '';
        /* A link that does not resolve says so here rather than becoming a
           broken picture on a published page. */
        img.addEventListener('error', function () {
          target.classList.add('is-broken');
          target.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">broken_image</span>';
        });
        img.addEventListener('load', function () { target.classList.remove('is-broken'); });
        img.src = url;
        target.innerHTML = '';
        target.appendChild(img);
      };
      input.addEventListener('change', paint);
      input.addEventListener('blur', paint);
    });
  };

  /* ── Templates ─────────────────────────────────────────────────────────── */
  NebStudio.prototype.bindTemplates = function () {
    var self = this;
    this.root.querySelectorAll('[data-mkt-template]').forEach(function (card) {
      card.addEventListener('click', function () {
        var mode = (self.root.querySelector('input[name="mkt-template-mode"]:checked') || {}).value || 'page';
        var warning = {
          page: 'Replace your look and all your sections with this template? '
              + 'Your name, contacts, courses and updates are not touched.',
          theme: 'Repaint your page with this template? Everything you have written stays.',
          sections: 'Replace your sections with this template’s? Your colours stay as they are.'
        }[mode];
        if (!window.confirm(warning)) return;

        card.disabled = true;
        self.post(self.root.dataset.templateUrl, { template: card.dataset.mktTemplate, mode: mode })
          .then(function () {
            self.toast('Template applied. Loading it…');
            /* A template rewrites the look and the sections at once. Re-drawing
               half of that in place would leave the Look tab showing the old
               palette over the new sections, so the editor reloads instead. */
            window.location.reload();
          })
          .catch(function (error) {
            self.toast(error.message, true);
            card.disabled = false;
          });
      });
    });

    var open = this.root.querySelector('[data-mkt-add-open]');
    var sheet = this.root.querySelector('[data-mkt-add-sheet]');
    var close = this.root.querySelector('[data-mkt-add-close]');
    if (open && sheet) {
      open.addEventListener('click', function () {
        sheet.hidden = !sheet.hidden;
        if (!sheet.hidden) sheet.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      });
    }
    if (close && sheet) {
      close.addEventListener('click', function () { sheet.hidden = true; });
    }
    this.root.querySelectorAll('[data-mkt-add-block]').forEach(function (option) {
      option.addEventListener('click', function () {
        self.addBlock(option.dataset.mktAddBlock);
        if (sheet) sheet.hidden = true;
      });
    });
  };

  /* ── Preview ───────────────────────────────────────────────────────────── */
  NebStudio.prototype.bindPreview = function () {
    var self = this;
    var frame = this.root.querySelector('[data-mkt-preview-frame]');
    var iframe = this.root.querySelector('[data-mkt-preview]');
    if (!frame || !iframe) return;

    this.root.querySelectorAll('[data-mkt-preview-size]').forEach(function (button) {
      button.addEventListener('click', function () {
        frame.dataset.size = button.dataset.mktPreviewSize;
        self.root.querySelectorAll('[data-mkt-preview-size]').forEach(function (other) {
          var on = other === button;
          other.classList.toggle('is-on', on);
          other.setAttribute('aria-checked', on ? 'true' : 'false');
        });
      });
    });

    var reload = this.root.querySelector('[data-mkt-preview-reload]');
    if (reload) {
      reload.addEventListener('click', function () { self.reloadPreview(); });
    }
  };

  NebStudio.prototype.reloadPreview = function () {
    var iframe = this.root.querySelector('[data-mkt-preview]');
    if (!iframe) return;
    var base = this.root.dataset.pageUrl || iframe.src.split('?')[0];
    /* Cache-busting rather than `location.reload()` on the frame: the page is
       served with ordinary caching headers and a creator pressing Reload means
       "show me what I just saved", not "show me what you have". */
    iframe.src = base + '?preview=' + Date.now();
    var state = this.root.querySelector('[data-mkt-preview-state]');
    if (state) state.textContent = 'Showing your page as it is saved right now.';
  };

  NebStudio.prototype.markPreviewStale = function () {
    var state = this.root.querySelector('[data-mkt-preview-state]');
    if (state) state.textContent = 'You have unsaved changes — save to see them here.';
  };
})();
