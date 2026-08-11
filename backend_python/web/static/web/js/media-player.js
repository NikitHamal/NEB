(function () {
  'use strict';

  var SPEEDS = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2];
  var SEEK_STEP = 10;
  var SAVE_INTERVAL_MS = 2500;
  var RESUME_MIN = 8;
  var RESUME_END_PAD = 12;

  function $(sel, root) {
    return (root || document).querySelector(sel);
  }

  function fmt(sec) {
    if (!isFinite(sec) || sec < 0) sec = 0;
    sec = Math.floor(sec);
    var h = Math.floor(sec / 3600);
    var m = Math.floor((sec % 3600) / 60);
    var s = sec % 60;
    var mm = h > 0 ? String(m).padStart(2, '0') : String(m);
    var ss = String(s).padStart(2, '0');
    return h > 0 ? h + ':' + mm + ':' + ss : mm + ':' + ss;
  }

  function storageKey(id) {
    return 'nmp:pos:' + id;
  }

  function loadPos(id) {
    try {
      var v = localStorage.getItem(storageKey(id));
      return v ? parseFloat(v) : 0;
    } catch (e) {
      return 0;
    }
  }

  function savePos(id, t) {
    try {
      if (t > RESUME_MIN) localStorage.setItem(storageKey(id), String(Math.floor(t)));
      else localStorage.removeItem(storageKey(id));
    } catch (e) { /* ignore quota */ }
  }

  function clearPos(id) {
    try { localStorage.removeItem(storageKey(id)); } catch (e) {}
  }

  function clamp(n, a, b) {
    return Math.max(a, Math.min(b, n));
  }

  function initPlayer(root) {
    if (!root || root._nmpReady) return;
    root._nmpReady = true;

    var kind = root.getAttribute('data-kind') || 'video';
    var src = root.getAttribute('data-src') || '';
    var mime = root.getAttribute('data-mime') || '';
    var resourceId = root.getAttribute('data-resource-id') || src;
    var provider = root.getAttribute('data-provider') || 'direct';

    if (provider !== 'direct' && kind !== 'audio') {
      initEmbed(root);
      return;
    }
    if (!src) return;

    var media = $('.nmp-el', root);
    if (!media) return;

    var playBtn = $('[data-nmp-play]', root);
    var bigPlay = $('[data-nmp-big-play]', root);
    var muteBtn = $('[data-nmp-mute]', root);
    var fsBtn = $('[data-nmp-fs]', root);
    var pipBtn = $('[data-nmp-pip]', root);
    var backBtn = $('[data-nmp-back]', root);
    var fwdBtn = $('[data-nmp-fwd]', root);
    var progress = $('[data-nmp-progress]', root);
    var fill = $('[data-nmp-fill]', root);
    var bufEl = $('[data-nmp-buf]', root);
    var thumb = $('[data-nmp-thumb]', root);
    var timeCur = $('[data-nmp-current]', root);
    var timeDur = $('[data-nmp-duration]', root);
    var volRange = $('[data-nmp-volume]', root);
    var speedWrap = $('[data-nmp-speed]', root);
    var speedBtn = speedWrap ? $('[data-nmp-speed-btn]', speedWrap) : null;
    var speedMenu = speedWrap ? $('[data-nmp-speed-menu]', speedWrap) : null;
    var resumeEl = $('[data-nmp-resume]', root);
    var playIcon = playBtn ? playBtn.querySelector('.material-symbols-outlined') : null;

    var srcBound = false;
    var dragging = false;
    var raf = 0;
    var lastSave = 0;
    var savedSpeed = 1;
    var resumeAt = loadPos(resourceId);

    function setPlayUi(playing) {
      root.classList.toggle('is-playing', playing);
      if (playIcon) {
        playIcon.textContent = playing ? 'pause' : 'play_arrow';
        playIcon.style.fontVariationSettings = playing ? "'FILL' 1" : '';
      }
      if (playBtn) playBtn.setAttribute('aria-label', playing ? 'Pause' : 'Play');
    }

    function setLoading(on) {
      root.classList.toggle('is-loading', !!on);
    }

    function applyAspectRatio() {
      var vw = media.videoWidth;
      var vh = media.videoHeight;
      if (vw > 0 && vh > 0) {
        var ratio = vw / vh;
        root.style.setProperty('--nmp-stage-ratio', ratio);
        if (ratio < 0.85) {
          root.classList.add('is-portrait');
          root.classList.remove('is-square', 'is-landscape');
        } else if (ratio >= 0.85 && ratio <= 1.15) {
          root.classList.add('is-square');
          root.classList.remove('is-portrait', 'is-landscape');
        } else {
          root.classList.add('is-landscape');
          root.classList.remove('is-portrait', 'is-square');
        }
      }
    }

    function bindSrc() {
      if (srcBound) return Promise.resolve();
      srcBound = true;
      while (media.firstChild) media.removeChild(media.firstChild);
      var source = document.createElement('source');
      source.src = src;
      if (mime) source.type = mime;
      media.appendChild(source);
      media.preload = 'metadata';
      media.load();
      return new Promise(function (resolve) {
        var done = function () {
          applyAspectRatio();
          media.removeEventListener('loadedmetadata', done);
          media.removeEventListener('error', done);
          resolve();
        };
        media.addEventListener('loadedmetadata', done, { once: true });
        media.addEventListener('error', done, { once: true });
      });
    }

    function updateProgress() {
      var d = media.duration || 0;
      var t = media.currentTime || 0;
      var pct = d > 0 ? (t / d) * 100 : 0;
      if (fill) fill.style.width = pct + '%';
      if (thumb) thumb.style.left = pct + '%';
      if (timeCur) timeCur.textContent = fmt(t);
      if (timeDur && isFinite(d) && d > 0) timeDur.textContent = fmt(d);

      if (media.buffered && media.buffered.length && d > 0 && bufEl) {
        try {
          var end = media.buffered.end(media.buffered.length - 1);
          bufEl.style.width = ((end / d) * 100) + '%';
        } catch (e) {}
      }

      var now = performance.now();
      if (now - lastSave > SAVE_INTERVAL_MS && !media.paused) {
        lastSave = now;
        if (d > 0 && t < d - RESUME_END_PAD) savePos(resourceId, t);
        else if (d > 0 && t >= d - RESUME_END_PAD) clearPos(resourceId);
      }
    }

    function tick() {
      if (!dragging) updateProgress();
      if (!media.paused && !media.ended) {
        raf = requestAnimationFrame(tick);
      } else {
        raf = 0;
      }
    }

    function startTick() {
      if (!raf) raf = requestAnimationFrame(tick);
    }

    function showResume() {
      if (!resumeEl || !(resumeAt > RESUME_MIN)) return;
      var label = $('[data-nmp-resume-label]', resumeEl);
      if (label) label.textContent = 'Resume from ' + fmt(resumeAt);
      resumeEl.classList.add('is-visible');
    }

    function hideResume() {
      if (resumeEl) resumeEl.classList.remove('is-visible');
    }

    async function play(from) {
      setLoading(true);
      root.classList.add('is-ready');
      hideResume();
      await bindSrc();
      if (typeof from === 'number' && isFinite(from) && from > 0) {
        try { media.currentTime = from; } catch (e) {}
      }
      try {
        media.playbackRate = savedSpeed;
        await media.play();
        setPlayUi(true);
        startTick();
      } catch (e) {
        setPlayUi(false);
        if (e && e.name !== 'AbortError') {
          root.classList.add('has-error');
        }
      } finally {
        setLoading(false);
      }
    }

    function pause() {
      media.pause();
      setPlayUi(false);
      savePos(resourceId, media.currentTime || 0);
    }

    function toggle() {
      if (media.paused) play();
      else pause();
    }

    function seekBy(delta) {
      if (!srcBound && !(media.duration > 0)) {
        bindSrc().then(function () {
          media.currentTime = clamp((media.currentTime || 0) + delta, 0, media.duration || 0);
          updateProgress();
        });
        return;
      }
      var d = media.duration || 0;
      media.currentTime = clamp((media.currentTime || 0) + delta, 0, d);
      updateProgress();
    }

    function seekToRatio(ratio) {
      var d = media.duration || 0;
      if (!(d > 0)) return;
      media.currentTime = clamp(ratio, 0, 1) * d;
      updateProgress();
    }

    function ratioFromEvent(e) {
      if (!progress) return 0;
      var rect = progress.getBoundingClientRect();
      var x = (e.clientX != null ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0));
      return clamp((x - rect.left) / rect.width, 0, 1);
    }

    function setMuted(m) {
      media.muted = m;
      if (muteBtn) {
        var ic = muteBtn.querySelector('.material-symbols-outlined');
        if (ic) ic.textContent = m || media.volume === 0 ? 'volume_off' : (media.volume < 0.4 ? 'volume_down' : 'volume_up');
        muteBtn.setAttribute('aria-pressed', m ? 'true' : 'false');
      }
    }

    if (playBtn) playBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (!srcBound && resumeAt > RESUME_MIN) play(resumeAt);
      else toggle();
    });

    if (bigPlay) {
      bigPlay.addEventListener('click', function (e) {
        e.stopPropagation();
        if (resumeAt > RESUME_MIN) play(resumeAt);
        else play();
      });
    }

    if (backBtn) backBtn.addEventListener('click', function () { seekBy(-SEEK_STEP); });
    if (fwdBtn) fwdBtn.addEventListener('click', function () { seekBy(SEEK_STEP); });

    if (muteBtn) muteBtn.addEventListener('click', function () { setMuted(!media.muted); });

    if (volRange) {
      volRange.addEventListener('input', function () {
        var v = parseFloat(volRange.value);
        media.volume = clamp(v, 0, 1);
        if (v > 0 && media.muted) setMuted(false);
        setMuted(media.muted || v === 0);
      });
    }

    if (fsBtn && kind === 'video') {
      fsBtn.addEventListener('click', function () {
        var doc = document;
        if (doc.fullscreenElement || doc.webkitFullscreenElement) {
          (doc.exitFullscreen || doc.webkitExitFullscreen).call(doc);
        } else {
          var req = root.requestFullscreen || root.webkitRequestFullscreen;
          if (req) req.call(root);
        }
      });
    }

    if (pipBtn && kind === 'video' && document.pictureInPictureEnabled) {
      pipBtn.hidden = false;
      pipBtn.addEventListener('click', async function () {
        try {
          await bindSrc();
          if (document.pictureInPictureElement) await document.exitPictureInPicture();
          else await media.requestPictureInPicture();
        } catch (e) {}
      });
    } else if (pipBtn) {
      pipBtn.hidden = true;
    }

    if (speedBtn && speedMenu) {
      speedBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = !speedMenu.classList.contains('is-open');
        speedMenu.classList.toggle('is-open', open);
        speedBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      speedMenu.addEventListener('click', function (e) {
        var opt = e.target.closest('[data-speed]');
        if (!opt) return;
        var rate = parseFloat(opt.getAttribute('data-speed'));
        if (!isFinite(rate)) return;
        savedSpeed = rate;
        media.playbackRate = rate;
        speedBtn.textContent = (rate === 1 ? '1x' : rate + 'x');
        speedMenu.querySelectorAll('[data-speed]').forEach(function (el) {
          el.classList.toggle('is-active', parseFloat(el.getAttribute('data-speed')) === rate);
        });
        speedMenu.classList.remove('is-open');
        speedBtn.setAttribute('aria-expanded', 'false');
      });
      document.addEventListener('click', function () {
        speedMenu.classList.remove('is-open');
        speedBtn.setAttribute('aria-expanded', 'false');
      });
    }

    if (progress) {
      var onDown = function (e) {
        if (e.button != null && e.button !== 0) return;
        dragging = true;
        progress.classList.add('is-dragging');
        bindSrc().then(function () {
          seekToRatio(ratioFromEvent(e));
        });
        e.preventDefault();
      };
      var onMove = function (e) {
        if (!dragging) return;
        seekToRatio(ratioFromEvent(e.touches ? e.touches[0] : e));
      };
      var onUp = function () {
        if (!dragging) return;
        dragging = false;
        progress.classList.remove('is-dragging');
        savePos(resourceId, media.currentTime || 0);
      };
      progress.addEventListener('pointerdown', onDown);
      window.addEventListener('pointermove', onMove);
      window.addEventListener('pointerup', onUp);
      progress.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') { seekBy(-SEEK_STEP); e.preventDefault(); }
        if (e.key === 'ArrowRight') { seekBy(SEEK_STEP); e.preventDefault(); }
        if (e.key === 'Home') { seekToRatio(0); e.preventDefault(); }
        if (e.key === 'End') { seekToRatio(1); e.preventDefault(); }
      });
    }

    if (resumeEl) {
      var resumeGo = $('[data-nmp-resume-go]', resumeEl);
      var resumeSkip = $('[data-nmp-resume-skip]', resumeEl);
      if (resumeGo) resumeGo.addEventListener('click', function () {
        hideResume();
        play(resumeAt);
      });
      if (resumeSkip) resumeSkip.addEventListener('click', function () {
        hideResume();
        clearPos(resourceId);
        resumeAt = 0;
      });
    }

    media.addEventListener('play', function () {
      setPlayUi(true);
      root.classList.add('is-ready');
      startTick();
      setLoading(false);
    });
    media.addEventListener('pause', function () {
      setPlayUi(false);
      savePos(resourceId, media.currentTime || 0);
    });
    media.addEventListener('ended', function () {
      setPlayUi(false);
      clearPos(resourceId);
      resumeAt = 0;
      updateProgress();
    });
    media.addEventListener('waiting', function () { setLoading(true); });
    media.addEventListener('canplay', function () { setLoading(false); });
    media.addEventListener('playing', function () { setLoading(false); });
    media.addEventListener('timeupdate', function () {
      if (!raf) updateProgress();
    });
    media.addEventListener('loadedmetadata', function () {
      updateProgress();
      if (resumeAt > RESUME_MIN && resumeAt < (media.duration || Infinity) - RESUME_END_PAD) {
        /* wait for user gesture for autoplay policy */
      }
    });
    media.addEventListener('error', function () {
      setLoading(false);
      if (srcBound) root.classList.add('has-error');
    });

    root.addEventListener('keydown', function (e) {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
      var k = e.key;
      if (k === ' ' || k === 'k' || k === 'K') { toggle(); e.preventDefault(); }
      else if (k === 'ArrowLeft' || k === 'j' || k === 'J') { seekBy(-SEEK_STEP); e.preventDefault(); }
      else if (k === 'ArrowRight' || k === 'l' || k === 'L') { seekBy(SEEK_STEP); e.preventDefault(); }
      else if (k === 'm' || k === 'M') { setMuted(!media.muted); e.preventDefault(); }
      else if ((k === 'f' || k === 'F') && kind === 'video' && fsBtn) { fsBtn.click(); e.preventDefault(); }
    });

    if (kind === 'video') {
      var stage = $('.nmp-stage', root);
      if (stage) {
        var lastTap = 0;
        stage.addEventListener('click', function (e) {
          if (e.target.closest('button, a, [data-nmp-progress], .nmp-resume')) return;
          var now = Date.now();
          if (now - lastTap < 280) {
            if (document.fullscreenElement) (document.exitFullscreen || document.webkitExitFullscreen).call(document);
            else if (root.requestFullscreen) root.requestFullscreen();
          } else if (srcBound || root.classList.contains('is-ready')) {
            toggle();
          }
          lastTap = now;
        });
      }
    }

    document.addEventListener('visibilitychange', function () {
      if (document.hidden && !media.paused && kind === 'video' && !document.pictureInPictureElement) {
        /* keep playing audio in background; pause video to save battery only if tab hidden long — skip aggressive pause */
      }
      if (document.hidden) savePos(resourceId, media.currentTime || 0);
    });

    if ('IntersectionObserver' in window && kind === 'video') {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting && !media.paused && !document.pictureInPictureElement) {
            /* do not auto-pause — students often scroll while listening; only save */
            savePos(resourceId, media.currentTime || 0);
          }
        });
      }, { threshold: 0.05 });
      io.observe(root);
    }

    if (resumeAt > RESUME_MIN) {
      root.addEventListener('nmp:first-play', function () {}, { once: true });
    }

    root._nmp = {
      play: play,
      pause: pause,
      toggle: toggle,
      media: media
    };
  }

  function initEmbed(root) {
    var embed = $('.nmp-embed', root);
    var poster = $('[data-nmp-embed-play]', root);
    var embedUrl = root.getAttribute('data-embed') || '';
    if (!embed || !embedUrl) return;

    function load() {
      if (embed.classList.contains('is-loaded')) return;
      var iframe = document.createElement('iframe');
      iframe.src = embedUrl;
      iframe.title = root.getAttribute('data-title') || 'Video';
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen';
      iframe.allowFullscreen = true;
      iframe.loading = 'lazy';
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      embed.appendChild(iframe);
      embed.classList.add('is-loaded');
      root.classList.add('is-ready');
    }

    if (poster) poster.addEventListener('click', load);
    else load();
  }

  function boot() {
    document.querySelectorAll('[data-nmp]').forEach(initPlayer);

    document.querySelectorAll('[data-action="scroll-to-media"]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        var target = document.getElementById('rd-media');
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        target.focus({ preventScroll: true });
        if (target._nmp && target.getAttribute('data-kind') !== 'embed') {
          /* gentle: don't autoplay until user hits play inside player */
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
