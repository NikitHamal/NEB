/* Forum media attachments: compact audio player + one-video-at-a-time. */
(function () {
  'use strict';

  function fmtTime(sec) {
    if (!isFinite(sec) || sec < 0) return '0:00';
    var m = Math.floor(sec / 60);
    var s = Math.floor(sec % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  function wrapOf(el) { return el.closest('[data-fm-audio]'); }

  function pauseAllAudio(except) {
    document.querySelectorAll('[data-fm-audio] audio').forEach(function (a) {
      if (a !== except && !a.paused) a.pause();
    });
  }

  function bindAudio(wrap) {
    if (!wrap || wrap.dataset.fmBound) return;
    wrap.dataset.fmBound = '1';
    var audio = wrap.querySelector('audio');
    var btn = wrap.querySelector('[data-action="fm-audio-toggle"]');
    var icon = btn && btn.querySelector('.material-symbols-outlined');
    var fill = wrap.querySelector('.fm-audio-progress-fill');
    var time = wrap.querySelector('.fm-audio-time');
    if (!audio) return;
    audio.addEventListener('play', function () {
      pauseAllAudio(audio);
      if (icon) icon.textContent = 'pause';
    });
    audio.addEventListener('pause', function () { if (icon) icon.textContent = 'play_arrow'; });
    audio.addEventListener('ended', function () {
      if (icon) icon.textContent = 'play_arrow';
      if (fill) fill.style.width = '0%';
      if (time) time.textContent = fmtTime(audio.duration);
    });
    audio.addEventListener('loadedmetadata', function () {
      if (time) time.textContent = fmtTime(audio.duration);
    });
    audio.addEventListener('timeupdate', function () {
      if (fill && audio.duration) fill.style.width = (audio.currentTime / audio.duration * 100) + '%';
      if (time) time.textContent = fmtTime(audio.currentTime);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-fm-audio]').forEach(bindAudio);
  });

  // HTMX / dynamic inserts: bind lazily via delegation instead of observers.
  if (window.registerAction) {
    window.registerAction('fm-audio-toggle', function (el) {
      var wrap = wrapOf(el);
      bindAudio(wrap);
      var audio = wrap && wrap.querySelector('audio');
      if (!audio) return;
      if (audio.paused) { audio.play(); } else { audio.pause(); }
    });
    window.registerAction('fm-audio-seek', function (el, e) {
      var wrap = wrapOf(el);
      bindAudio(wrap);
      var audio = wrap && wrap.querySelector('audio');
      if (!audio || !audio.duration) return;
      var rect = el.getBoundingClientRect();
      var ratio = Math.min(1, Math.max(0, (e.clientX - rect.left) / rect.width));
      audio.currentTime = ratio * audio.duration;
    });
  }

  // Only one video plays at a time.
  document.addEventListener('play', function (e) {
    var v = e.target;
    if (!v || v.tagName !== 'VIDEO' || !v.classList.contains('fm-video')) return;
    document.querySelectorAll('video.fm-video').forEach(function (other) {
      if (other !== v && !other.paused) other.pause();
    });
  }, true);
})();
