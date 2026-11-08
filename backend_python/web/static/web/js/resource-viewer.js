/* Resource viewer: the file is never opened on arrival. The stage starts as a cover; Read mounts the
   right reader for the file's kind (pdf, image, video, audio, hosted embed, link). Documents and
   anything the browser cannot show lead to the app. While an overlay is open every frame is hidden
   (neb-has-overlay), because a PDF viewer paints above backdrop-filter and stays sharp over the blur. */
(function () {
  'use strict';
  var stage = document.getElementById('vw-stage');
  if (!stage) return;
  var cover = document.getElementById('vw-cover');
  var reader = document.getElementById('vw-reader');
  var view = document.getElementById('vw-view');
  var loading = document.getElementById('vw-loading');
  var fs = document.getElementById('vw-fs');
  var kind = stage.getAttribute('data-kind');
  var src = stage.getAttribute('data-src') || '';
  var embed = stage.getAttribute('data-embed') || '';
  var title = stage.getAttribute('data-title') || '';
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mounted = false, loadTimer = 0;

  function el(tag, cls, attrs) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    for (var k in (attrs || {})) n.setAttribute(k, attrs[k]);
    return n;
  }

  function appCard(icon, text) {
    var box = el('div', 'vw-fallback');
    box.innerHTML = '<span class="px-sprite px-downloadTray" aria-hidden="true"></span><p></p>';
    box.querySelector('p').textContent = text;
    var b = el('button', 'x-btn x-btn-filled', { type: 'button', 'data-neb-open': 'get-app-dialog' });
    b.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">' + icon + '</span>Download';
    box.appendChild(b);
    return box;
  }

  function settle(node) {
    var done = function () { if (loading) loading.classList.add('is-done'); };
    var wait = reduced ? 0 : 650;
    var t0 = Date.now();
    var finish = function () { clearTimeout(loadTimer); setTimeout(done, Math.max(0, wait - (Date.now() - t0))); };
    if (node && node.tagName === 'IFRAME') {
      node.addEventListener('load', finish, { once: true });
      loadTimer = setTimeout(finish, 7000);
    } else if (node && node.tagName === 'IMG') {
      if (node.complete) finish(); else { node.addEventListener('load', finish, { once: true }); node.addEventListener('error', finish, { once: true }); }
    } else finish();
  }

  function pdfFallback() {
    if (navigator.pdfViewerEnabled === false) return appCard('download', 'This browser cannot show PDFs');
    var f = el('iframe', 'vw-iframe', { title: title, referrerpolicy: 'no-referrer' });
    f.src = src + '#toolbar=0&navpanes=0&view=FitH';
    return f;
  }

  /* PDF styles: the page-turning book (default) or the classic scrolling reader. The choice is remembered; switching
     keeps the page you are on, and both share one downloaded document (NebPdf.open). */
  var MODE_KEY = 'neb.reader.mode';
  var mode = 'book';
  try { mode = localStorage.getItem(MODE_KEY) === 'classic' ? 'classic' : 'book'; } catch (e) { /* storage blocked */ }
  var handle = null;
  var modeBox = stage.querySelector('[data-vw-mode]');

  function paintMode() {
    if (kind !== 'pdf') return;
    stage.setAttribute('data-mode', mode);
    if (modeBox) modeBox.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-mode') === mode ? 'true' : 'false'); });
  }

  function pdfNode(page) {
    var h;
    if (mode === 'book' && window.NebBook && window.NebPdf) {
      h = window.NebBook.mount(src, title, { page: page, onClassic: function () { setMode('classic'); } });
    } else if (window.NebPdf && 'IntersectionObserver' in window) {
      h = window.NebPdf.mount(src, title);
    } else return pdfFallback();
    handle = h;
    h.node._ready = h.ready;
    return h.node;
  }

  function dropPdf() {
    if (!handle) return;
    if (handle.destroy) handle.destroy(); else if (handle.node) handle.node.remove();
    handle = null;
  }

  function setMode(next) {
    if (kind !== 'pdf' || next === mode) return;
    var page = handle && handle.page ? handle.page() : 0;
    mode = next;
    try { localStorage.setItem(MODE_KEY, mode); } catch (e) { /* storage blocked */ }
    paintMode();
    if (!mounted) return;
    dropPdf();
    view.querySelectorAll('.vw-pdf, .vw-iframe, .vw-fallback').forEach(function (n) { n.remove(); });
    if (loading) loading.classList.remove('is-done');
    var node = pdfNode(page);
    view.appendChild(node);
    if (node._ready) {
      node._ready.then(function () {
        if (mode === 'classic' && page > 1 && handle && handle.goto) setTimeout(function () { handle.goto(page); }, 80);
        settle(null);
        if (node.focus) node.focus({ preventScroll: true });
      }, function () {
        var alt = pdfFallback();
        if (node.parentNode) view.replaceChild(alt, node); else view.appendChild(alt);
        settle(alt);
      });
    } else settle(node);
  }

  if (modeBox) {
    modeBox.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-mode]');
      if (b) setMode(b.getAttribute('data-mode'));
    });
    paintMode();
  }

  function build() {
    var node;
    if (kind === 'pdf') {
      node = pdfNode(0);
    } else if (kind === 'image') {
      node = el('div', 'vw-image');
      var img = el('img', '', { alt: title, draggable: 'false' });
      img.src = src;
      img.addEventListener('click', function () { node.classList.toggle('is-zoom'); });
      node.appendChild(img);
      node._probe = img;
    } else if (kind === 'embed') {
      node = el('iframe', 'vw-iframe', { title: title, allow: 'autoplay; encrypted-media; picture-in-picture; fullscreen', allowfullscreen: '', referrerpolicy: 'strict-origin-when-cross-origin' });
      node.src = embed;
    } else if (kind === 'video' || kind === 'audio') {
      var tpl = document.getElementById('vw-tpl');
      node = el('div', 'vw-media');
      if (tpl) node.appendChild(tpl.content.cloneNode(true));
      node.querySelectorAll('video, audio').forEach(function (m) {
        m.setAttribute('controlsList', 'nodownload noremoteplayback');
        m.setAttribute('disablePictureInPicture', '');
      });
    }
    return node;
  }

  function openReader() {
    if (kind === 'link') { window.open(src, '_blank', 'noopener,noreferrer'); return; }
    if (!mounted) {
      var node = build();
      if (!node) return;
      view.appendChild(node);
      mounted = true;
      if (kind === 'video' || kind === 'audio') {
        if (window.NebMedia) window.NebMedia.mount(node);
        settle(null);
      } else if (node._ready) {
        node._ready.then(function () { settle(null); if (node.focus) node.focus({ preventScroll: true }); }, function () {
          var alt = pdfFallback();
          view.replaceChild(alt, node);
          settle(alt);
        });
      } else settle(node._probe || node);
    }
    stage.setAttribute('data-state', 'reading');
    cover.hidden = true;
    reader.hidden = false;
    if (!reduced && reader.animate) reader.animate([{ opacity: 0, transform: 'scale(.97)' }, { opacity: 1, transform: 'none' }], { duration: 420, easing: 'cubic-bezier(.2,1.1,.3,1)' });
    if (window.innerWidth < 900) stage.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
  }

  function closeReader() {
    if (document.fullscreenElement) document.exitFullscreen();
    stage.setAttribute('data-state', 'cover');
    reader.hidden = true;
    cover.hidden = false;
    view.querySelectorAll('video, audio').forEach(function (m) { m.pause(); });
    if (kind === 'pdf' && mode === 'book' && handle) {
      // The book stops its timers and keys when closed; opening again resumes at the saved page.
      dropPdf();
      view.querySelectorAll('.bk').forEach(function (n) { n.remove(); });
      if (loading) loading.classList.remove('is-done');
      mounted = false;
    }
    if (!reduced && cover.animate) cover.animate([{ opacity: 0, transform: 'scale(.98)' }, { opacity: 1, transform: 'none' }], { duration: 360, easing: 'cubic-bezier(.2,1.1,.3,1)' });
  }

  var read = stage.querySelector('[data-vw-read]');
  if (read) read.addEventListener('click', openReader);
  var close = stage.querySelector('[data-vw-close]');
  if (close) close.addEventListener('click', closeReader);

  if (fs) {
    fs.addEventListener('click', function () {
      if (document.fullscreenElement) document.exitFullscreen();
      else if (stage.requestFullscreen) stage.requestFullscreen();
    });
    document.addEventListener('fullscreenchange', function () {
      fs.querySelector('.material-symbols-outlined').textContent = document.fullscreenElement ? 'fullscreen_exit' : 'fullscreen';
    });
  }

  stage.addEventListener('click', function (e) {
    if (e.target.closest('[data-neb-open]') && document.fullscreenElement) document.exitFullscreen();
  });

  stage.addEventListener('contextmenu', function (e) { if (e.target.closest('img, video, audio')) e.preventDefault(); });
})();
