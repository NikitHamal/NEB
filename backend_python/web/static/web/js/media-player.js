(function () {
  'use strict';

  var SPEEDS = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2];
  var SEEK_STEP = 10;
  var SAVE_INTERVAL_MS = 2500;
  var RESUME_MIN = 8;
  var RESUME_END_PAD = 12;
  var UI_IDLE_MS = 2600;

  function $(sel, root) {
    return (root || document).querySelector(sel);
  }

  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
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
    var playGestures = $$('[data-nmp-big-play]', root);
    var muteBtn = $('[data-nmp-mute]', root);
    var fsBtn = $('[data-nmp-fs]', root);
    var pipBtn = $('[data-nmp-pip]', root);
    var backBtn = $('[data-nmp-back]', root);
    var fwdBtn = $('[data-nmp-fwd]', root);
    var progress = $('[data-nmp-progress]', root);
    var fill = $('[data-nmp-fill]', root);
    var bufEl = $('[data-nmp-buf]', root);
    var thumb = $('[data-nmp-thumb]', root);
    var hoverEl = $('[data-nmp-hover]', root);
    var tipEl = $('[data-nmp-tip]', root);
    var flashEl = $('[data-nmp-flash]', root);
    var retryBtn = $('[data-nmp-retry]', root);
    var timeCur = $('[data-nmp-current]', root);
    var timeDur = $('[data-nmp-duration]', root);
    var metaDur = $('[data-nmp-meta-duration]', root);
    var volRange = $('[data-nmp-volume]', root);
    var speedWrap = $('[data-nmp-speed]', root);
    var speedBtn = speedWrap ? $('[data-nmp-speed-btn]', speedWrap) : null;
    var speedMenu = speedWrap ? $('[data-nmp-speed-menu]', speedWrap) : null;
    var resumeEl = $('[data-nmp-resume]', root);
    var centerGesture = $('[data-nmp-center-gesture]', root);
    var tapLeft = $('[data-nmp-tap-left]', root);
    var tapRight = $('[data-nmp-tap-right]', root);
    var isRemainingTimeMode = false;

    var srcBound = false;
    var dragging = false;
    var raf = 0;
    var lastSave = 0;
    var savedSpeed = 1;
    var resumeAt = loadPos(resourceId);
    var usedResume = false;

    function flashCenterGesture(iconType) {
      if (!centerGesture) return;
      var gPlay = $('.nmp-gesture-play', centerGesture);
      var gPause = $('.nmp-gesture-pause', centerGesture);
      if (gPlay && gPause) {
        gPlay.style.display = iconType === 'play' ? 'block' : 'none';
        gPause.style.display = iconType === 'pause' ? 'block' : 'none';
      }
      centerGesture.classList.remove('is-pulsing');
      void centerGesture.offsetWidth;
      centerGesture.classList.add('is-pulsing');
      setTimeout(function () {
        centerGesture.classList.remove('is-pulsing');
      }, 350);
    }

    function setPlayUi(playing) {
      root.classList.toggle('is-playing', playing);
      if (playBtn) playBtn.setAttribute('aria-label', playing ? 'Pause' : 'Play');
      flashCenterGesture(playing ? 'play' : 'pause');
    }

    function setLoading(on) {
      root.classList.toggle('is-loading', !!on);
    }

    function applyAspectRatioFromDimensions(vw, vh) {
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

    function applyAspectRatio() {
      applyAspectRatioFromDimensions(media.videoWidth, media.videoHeight);
    }

    // The extracted frame carries the footage's own proportions, so the stage
    // can fit it before the video file answers anything.
    var posterEl = $('.nmp-poster-img', root);
    var posterUrl = (posterEl && posterEl.getAttribute('src')) || media.getAttribute('poster') || '';
    if (posterUrl) {
      var pImg = new Image();
      pImg.onload = function () {
        applyAspectRatioFromDimensions(pImg.naturalWidth, pImg.naturalHeight);
      };
      pImg.src = posterUrl;
    }

    if (media.videoWidth && media.videoHeight) {
      applyAspectRatio();
    } else {
      media.addEventListener('loadedmetadata', applyAspectRatio, { once: true });
    }

    /* The chrome answers to the pointer and then gets out of the way: a bar
       that never leaves covers the bottom of a lecture slide, and one that
       never comes back can't be reached. */
    var uiTimer = 0;

    function showUi(sticky) {
      root.classList.remove('is-ui-hidden');
      window.clearTimeout(uiTimer);
      if (sticky) return;
      uiTimer = window.setTimeout(function () {
        if (!media.paused && !media.ended && !root.classList.contains('has-error')) {
          root.classList.add('is-ui-hidden');
        }
      }, UI_IDLE_MS);
    }

    function holdUi() {
      window.clearTimeout(uiTimer);
      root.classList.remove('is-ui-hidden');
    }

    if (kind === 'video') {
      root.addEventListener('pointermove', function (e) {
        if (e.pointerType === 'touch') return;
        showUi();
      });
      root.addEventListener('pointerdown', function () { showUi(); });
      root.addEventListener('pointerleave', function () {
        if (!media.paused && !media.ended) root.classList.add('is-ui-hidden');
      });
      root.addEventListener('focusin', holdUi);
      root.addEventListener('focusout', function (e) {
        if (!root.contains(e.relatedTarget)) showUi();
      });
      root.addEventListener('mouseenter', function () { showUi(); });
    }

    function bindSrcSoon() {
      if (srcBound) return;
      if (!('IntersectionObserver' in window)) { bindSrc(); return; }
      var io = new IntersectionObserver(function (entries) {
        if (!entries.some(function (en) { return en.isIntersecting; })) return;
        io.disconnect();
        bindSrc();
      }, { rootMargin: '320px 0px' });
      io.observe(root);
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
      if (timeCur) {
        if (isRemainingTimeMode && d > 0) {
          timeCur.textContent = '-' + fmt(d - t);
        } else {
          timeCur.textContent = fmt(t);
        }
      }
      if (timeDur && isFinite(d) && d > 0) timeDur.textContent = fmt(d);
      if (metaDur && isFinite(d) && d > 0) metaDur.textContent = fmt(d);
      if (progress) {
        progress.setAttribute('aria-valuenow', Math.round(pct));
        progress.setAttribute('aria-valuetext', fmt(t) + ' of ' + (isFinite(d) && d > 0 ? fmt(d) : '0:00'));
      }

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
      showUi(true);
      hideResume();
      await bindSrc();
      /* The first press picks up where the last session stopped, however play
         was reached -- the big button, the bar, a stage tap or a keyboard key.
         Later presses respect the position the video is already at. */
      var target = (typeof from === 'number' && isFinite(from) && from > 0) ? from : 0;
      if (!target && !usedResume && resumeAt > RESUME_MIN) target = resumeAt;
      usedResume = true;
      if (target) {
        try { media.currentTime = target; } catch (e) {}
      }
      try {
        media.playbackRate = savedSpeed;
        await media.play();
        setPlayUi(true);
        startTick();
        showUi();
      } catch (e) {
        setPlayUi(false);
        holdUi();
        /* A refused gesture is not a broken file: AbortError (a seek during
           play) and NotAllowedError (autoplay policy) both leave the poster up
           so the viewer can press play themselves. */
        if (e && e.name !== 'AbortError' && e.name !== 'NotAllowedError') {
          showError();
        }
      } finally {
        setLoading(false);
      }
    }

    function pause() {
      media.pause();
      setPlayUi(false);
      holdUi();
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
        var vUp = $('.nmp-icon-vol-up', muteBtn);
        var vDown = $('.nmp-icon-vol-down', muteBtn);
        var vMute = $('.nmp-icon-vol-mute', muteBtn);
        var isM = m || media.volume === 0;
        if (vUp && vDown && vMute) {
          vMute.style.display = isM ? 'block' : 'none';
          vDown.style.display = !isM && media.volume < 0.5 ? 'block' : 'none';
          vUp.style.display = !isM && media.volume >= 0.5 ? 'block' : 'none';
        }
        muteBtn.setAttribute('aria-pressed', m ? 'true' : 'false');
      }
    }

    function showError() {
      holdUi();
      root.classList.add('has-error');
    }

    function clearError() {
      root.classList.remove('has-error');
    }

    if (retryBtn) {
      retryBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        clearError();
        setLoading(true);
        try { media.load(); } catch (err) { /* already loading */ }
        var back = media.currentTime || 0;
        play(back > RESUME_MIN ? back : 0);
      });
    }

    function flashSeek(delta) {
      var forwards = delta > 0;
      var targetTap = forwards ? tapRight : tapLeft;
      if (targetTap) {
        targetTap.classList.remove('is-active');
        void targetTap.offsetWidth;
        targetTap.classList.add('is-active');
        setTimeout(function () { targetTap.classList.remove('is-active'); }, 400);
      }
      if (flashEl) {
        flashEl.classList.toggle('is-right', forwards);
        flashEl.classList.toggle('is-left', !forwards);
        flashEl.classList.toggle('is-back', !forwards);
        var glyph = flashEl.querySelector('.material-symbols-outlined');
        if (glyph) glyph.textContent = forwards ? 'forward_10' : 'replay_10';
        flashEl.classList.remove('is-on');
        void flashEl.offsetWidth;
        flashEl.classList.add('is-on');
      }
      seekBy(delta);
      showUi();
    }

    function toggleFullscreen() {
      var doc = document;
      if (doc.fullscreenElement || doc.webkitFullscreenElement) {
        (doc.exitFullscreen || doc.webkitExitFullscreen).call(doc);
      } else {
        var req = root.requestFullscreen || root.webkitRequestFullscreen;
        if (req) req.call(root);
      }
    }

    function updateFullscreenUi() {
      if (!fsBtn) return;
      var isFs = !!(document.fullscreenElement || document.webkitFullscreenElement);
      var fsIcon = $('.nmp-icon-fs', fsBtn);
      var fsExit = $('.nmp-icon-fs-exit', fsBtn);
      if (fsIcon && fsExit) {
        fsIcon.style.display = isFs ? 'none' : 'block';
        fsExit.style.display = isFs ? 'block' : 'none';
      }
    }
    document.addEventListener('fullscreenchange', updateFullscreenUi);
    document.addEventListener('webkitfullscreenchange', updateFullscreenUi);

    if (progress && (tipEl || hoverEl)) {
      progress.addEventListener('pointermove', function (e) {
        if (e.pointerType === 'touch') return;
        var ratio = ratioFromEvent(e);
        if (tipEl) {
          tipEl.textContent = fmt(ratio * (media.duration || 0));
          tipEl.style.left = (ratio * 100) + '%';
        }
        if (hoverEl) hoverEl.style.width = (ratio * 100) + '%';
      });
    }

    if (playBtn) playBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      toggle();
    });

    playGestures.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        toggle();
      });
    });

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
      fsBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        toggleFullscreen();
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

    var qualityWrap = $('[data-nmp-quality]', root);
    var qualityBtn = qualityWrap ? $('[data-nmp-quality-btn]', qualityWrap) : null;
    var qualityMenu = qualityWrap ? $('[data-nmp-quality-menu]', qualityWrap) : null;
    var qualitiesList = [];

    try {
      var rawQ = root.getAttribute('data-qualities');
      if (rawQ) {
        qualitiesList = typeof rawQ === 'string' ? JSON.parse(rawQ) : rawQ;
      }
    } catch (e) {}

    /* Only variants the server found on disk. Guessing _720p/_480p/_360p URLs
       from the filename offered choices that 404'd when picked. */
    if (qualityWrap && qualityMenu && Array.isArray(qualitiesList) && qualitiesList.length > 1) {
      qualityWrap.style.display = '';
      while (qualityMenu.firstChild) qualityMenu.removeChild(qualityMenu.firstChild);
      qualitiesList.forEach(function (q, idx) {
        var btn = document.createElement('button');
        btn.className = 'nmp-speed-option' + (idx === 0 ? ' is-active' : '');
        btn.setAttribute('data-url', q.url);
        btn.setAttribute('role', 'menuitem');
        btn.textContent = q.label;
        btn.addEventListener('click', function (e) {
          e.stopPropagation();
          qualityMenu.querySelectorAll('.nmp-speed-option').forEach(function (b) { b.classList.remove('is-active'); });
          btn.classList.add('is-active');
          if (qualityBtn) qualityBtn.textContent = q.label;
          qualityMenu.classList.remove('is-open');
          if (qualityBtn) qualityBtn.setAttribute('aria-expanded', 'false');

          var curTime = media.currentTime || 0;
          var wasPlaying = !media.paused;

          media.pause();
          while (media.firstChild) media.removeChild(media.firstChild);
          media.src = q.url;
          media.load();

          function onMetadata() {
            media.removeEventListener('loadedmetadata', onMetadata);
            if (curTime > 0 && isFinite(media.duration) && curTime < media.duration) {
              try { media.currentTime = curTime; } catch (err) {}
            }
            if (wasPlaying) {
              media.play().catch(function () {});
            }
          }
          media.addEventListener('loadedmetadata', onMetadata);
        });
        qualityMenu.appendChild(btn);
      });

      if (qualityBtn) {
        qualityBtn.addEventListener('click', function (e) {
          e.stopPropagation();
          if (speedMenu) speedMenu.classList.remove('is-open');
          var open = qualityMenu.classList.toggle('is-open');
          qualityBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
      }
      document.addEventListener('click', function () {
        qualityMenu.classList.remove('is-open');
        if (qualityBtn) qualityBtn.setAttribute('aria-expanded', 'false');
      });
    } else if (qualityWrap) {
      qualityWrap.style.display = 'none';
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
      startTick();
      setLoading(false);
    });
    media.addEventListener('pause', function () {
      setPlayUi(false);
      holdUi();
      savePos(resourceId, media.currentTime || 0);
    });
    media.addEventListener('ended', function () {
      setPlayUi(false);
      holdUi();
      clearPos(resourceId);
      resumeAt = 0;
      updateProgress();
    });
    media.addEventListener('waiting', function () { setLoading(true); holdUi(); });
    media.addEventListener('canplay', function () { setLoading(false); });
    /* 'playing' is the first decoded frame. Until then the poster stays up, so
       the stage is never an empty box while the file buffers. */
    media.addEventListener('playing', function () {
      setLoading(false);
      clearError();
      root.classList.add('is-seen');
      showUi();
    });
    media.addEventListener('timeupdate', function () {
      if (!raf) updateProgress();
    });
    media.addEventListener('loadedmetadata', function () {
      updateProgress();
      if (!usedResume) showResume();
    });
    media.addEventListener('error', function () {
      setLoading(false);
      if (srcBound) showError();
    });

    if (timeCur) {
      timeCur.style.cursor = 'pointer';
      timeCur.setAttribute('title', 'Click to toggle elapsed / remaining time');
      timeCur.addEventListener('click', function (e) {
        e.stopPropagation();
        isRemainingTimeMode = !isRemainingTimeMode;
        updateProgress();
      });
    }

    // Metadata arrives off the network, so the stage can match the real frame
    // aspect before anyone presses play.
    if (kind === 'video') bindSrcSoon();

    root.addEventListener('keydown', function (e) {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable)) return;
      var k = e.key;
      showUi();
      if (k === ' ' || k === 'k' || k === 'K') { toggle(); e.preventDefault(); }
      else if (k === 'ArrowLeft' || k === 'j' || k === 'J') { seekBy(-SEEK_STEP); e.preventDefault(); }
      else if (k === 'ArrowRight' || k === 'l' || k === 'L') { seekBy(SEEK_STEP); e.preventDefault(); }
      else if (k === 'ArrowUp') {
        media.volume = Math.min(1, (media.volume || 0) + 0.1);
        if (volRange) volRange.value = media.volume;
        setMuted(false);
        e.preventDefault();
      }
      else if (k === 'ArrowDown') {
        media.volume = Math.max(0, (media.volume || 0) - 0.1);
        if (volRange) volRange.value = media.volume;
        setMuted(media.volume === 0);
        e.preventDefault();
      }
      else if (k === 'm' || k === 'M') { setMuted(!media.muted); e.preventDefault(); }
      else if ((k === 'f' || k === 'F') && kind === 'video' && fsBtn) { toggleFullscreen(); e.preventDefault(); }
      else if ((k === 'p' || k === 'P') && kind === 'video' && pipBtn) { pipBtn.click(); e.preventDefault(); }
      else if (k >= '0' && k <= '9') {
        var num = parseInt(k, 10);
        seekToRatio(num / 10);
        e.preventDefault();
      }
    });

    if (kind === 'video') {
      var stage = $('.nmp-stage', root);
      if (stage) {
        var lastTapAt = 0;
        var lastTapSide = '';
        stage.addEventListener('click', function (e) {
          if (e.target.closest('button, a, [data-nmp-progress], .nmp-resume')) return;
          var now = Date.now();
          var rect = stage.getBoundingClientRect();
          var x = e.clientX - rect.left;
          var side = x < rect.width / 3 ? 'left' : (x > rect.width * 2 / 3 ? 'right' : 'center');
          if (now - lastTapAt < 300 && side === lastTapSide) {
            lastTapAt = 0;
            if (side === 'left') flashSeek(-SEEK_STEP);
            else if (side === 'right') flashSeek(SEEK_STEP);
            else toggleFullscreen();
            return;
          }
          lastTapAt = now;
          lastTapSide = side;
          if (srcBound) toggle();
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
