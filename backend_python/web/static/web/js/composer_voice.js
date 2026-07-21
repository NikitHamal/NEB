/*
 * NebVoiceComposer — voice-note recording for every comment bar on the site.
 *
 * attach(wrapper, hooks) upgrades a `.reply-input-wrapper` in place:
 *  - The send button morphs by state: empty text (and no staged attachments)
 *    shows a mic; with content it is the send arrow; while recording the
 *    trailing control is a "finish" (check) button.
 *  - Tapping the mic starts MediaRecorder and replaces the textarea with a
 *    live in-bar strip: pulsing red dot, timer, animated amplitude bars and
 *    pause / delete controls. Finish uploads nothing itself — hooks.onFile
 *    receives the File (voice_<ts>.webm|m4a) so the page can stage/upload it
 *    like any other attachment; delete discards the take.
 *
 * Hooks: {
 *   hasAttachments()  -> bool   (staged, non-uploading attachments exist)
 *   onFile(file, ms)            (finished take ready to stage)
 *   onError(message)
 * }
 */
(function () {
  'use strict';

  var MIME_CANDIDATES = [
    'audio/webm;codecs=opus',
    'audio/webm',
    'audio/mp4'
  ];
  var MAX_MS = 5 * 60 * 1000;
  var MIN_MS = 400;
  var BAR_COUNT = 18;

  function supported() {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder);
  }

  function pickMime() {
    if (!window.MediaRecorder || !MediaRecorder.isTypeSupported) return '';
    for (var i = 0; i < MIME_CANDIDATES.length; i++) {
      try { if (MediaRecorder.isTypeSupported(MIME_CANDIDATES[i])) return MIME_CANDIDATES[i]; } catch (e) {}
    }
    return '';
  }

  function extForMime(mime) {
    return (mime && mime.indexOf('mp4') >= 0) ? 'm4a' : 'webm';
  }

  function fmtVoiceTime(ms) {
    var s = Math.max(0, Math.floor(ms / 1000));
    var m = Math.floor(s / 60);
    var r = s % 60;
    return m + ':' + (r < 10 ? '0' : '') + r;
  }

  function fail(hooks, message) {
    if (hooks && typeof hooks.onError === 'function') hooks.onError(message);
    else if (typeof showSnackbar === 'function') showSnackbar(message);
  }

  function attach(wrapper, hooks) {
    hooks = hooks || {};
    if (!wrapper || wrapper.__voice) return wrapper ? wrapper.__voice : null;
    if (!supported()) return null;

    var textarea = wrapper.querySelector('textarea');
    var sendBtn = wrapper.querySelector('.reply-send-btn');
    if (!sendBtn) return null;
    var sendIcon = sendBtn.querySelector('.material-symbols-outlined');
    var sendWasSubmit = (sendBtn.getAttribute('type') || '').toLowerCase() === 'submit';

    // ----- Recording strip (hidden until recording) -----
    var strip = document.createElement('div');
    strip.className = 'voice-rec-strip';
    strip.style.display = 'none';
    strip.innerHTML =
      '<span class="voice-rec-dot"></span>' +
      '<span class="voice-rec-time">0:00</span>' +
      '<span class="voice-rec-bars"></span>' +
      '<button type="button" class="voice-rec-btn voice-rec-pause" title="Pause">' +
        '<span class="material-symbols-outlined">pause</span></button>' +
      '<button type="button" class="voice-rec-btn voice-rec-delete" title="Delete">' +
        '<span class="material-symbols-outlined">delete</span></button>';
    var barsWrap = strip.querySelector('.voice-rec-bars');
    for (var i = 0; i < BAR_COUNT; i++) {
      var bar = document.createElement('span');
      bar.className = 'voice-rec-bar';
      barsWrap.appendChild(bar);
    }
    wrapper.insertBefore(strip, sendBtn);

    var timeEl = strip.querySelector('.voice-rec-time');
    var pauseBtn = strip.querySelector('.voice-rec-pause');
    var pauseIcon = pauseBtn.querySelector('.material-symbols-outlined');
    var deleteBtn = strip.querySelector('.voice-rec-delete');

    var state = 'idle'; // idle | recording | paused
    var recorder = null, chunks = [], streamRef = null;
    var startedAt = 0, pausedAccum = 0, pauseStart = 0, elapsedMs = 0;
    var ticker = null, audioCtx = null, analyserRef = null, barEnv = 0.08;
    var mime = '';

    function nonUploadingAttachments() {
      if (typeof hooks.hasAttachments !== 'function') return false;
      try { return !!hooks.hasAttachments(); } catch (e) { return false; }
    }

    function hasContent() {
      return !!((textarea && textarea.value.trim().length) || nonUploadingAttachments());
    }

    function refresh() {
      if (state !== 'idle') return;
      var mic = !hasContent();
      sendBtn.dataset.mode = mic ? 'mic' : 'send';
      if (sendIcon) sendIcon.textContent = mic ? 'mic' : 'arrow_upward';
      sendBtn.setAttribute('type', mic ? 'button' : (sendWasSubmit ? 'submit' : 'button'));
      sendBtn.disabled = mic ? false : !hasContent();
      sendBtn.title = mic ? 'Record a voice note' : 'Send';
      wrapper.dataset.voiceInit = '1';
    }

    function setRecordingUI(recording) {
      wrapper.classList.toggle('recording', recording);
      strip.style.display = recording ? '' : 'none';
      if (textarea) textarea.style.display = recording ? 'none' : '';
      if (recording) {
        sendBtn.dataset.mode = 'recording';
        if (sendIcon) sendIcon.textContent = 'check';
        sendBtn.setAttribute('type', 'button');
        sendBtn.disabled = false;
        sendBtn.title = 'Add voice note';
      }
    }

    function elapsedNow() {
      var now = Date.now();
      var paused = state === 'paused' ? (now - pauseStart) : 0;
      return now - startedAt - pausedAccum - paused;
    }

    function tick() {
      elapsedMs = elapsedNow();
      timeEl.textContent = fmtVoiceTime(elapsedMs);
      drawBars();
      if (elapsedMs >= MAX_MS) finish();
    }

    function drawBars() {
      var bars = barsWrap.children;
      var level = 0.08;
      if (analyserRef && state === 'recording') {
        var data = new Uint8Array(analyserRef.fftSize);
        analyserRef.getByteTimeDomainData(data);
        var sum = 0;
        for (var i = 0; i < data.length; i += 8) {
          var v = (data[i] - 128) / 128;
          sum += v * v;
        }
        level = Math.min(1, Math.sqrt(sum / (data.length / 8)) * 4);
      }
      barEnv = barEnv * 0.72 + level * 0.28;
      for (var j = 0; j < bars.length; j++) {
        var phase = (Date.now() / 130) + j * 0.9;
        var jitter = (Math.sin(phase) + Math.sin(phase * 0.63)) * 0.25;
        var h = Math.max(0.12, Math.min(1, barEnv * 1.2 + jitter * barEnv + 0.10));
        bars[j].style.transform = 'scaleY(' + h.toFixed(3) + ')';
        bars[j].classList.toggle('inactive', state === 'paused');
      }
    }

    function start() {
      if (state !== 'idle') return;
      navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
        streamRef = stream;
        mime = pickMime();
        var opts = mime ? { mimeType: mime } : undefined;
        try {
          recorder = new MediaRecorder(stream, opts);
        } catch (e) {
          try { recorder = new MediaRecorder(stream); } catch (e2) {
            fail(hooks, 'Voice recording is not supported in this browser.');
            stream.getTracks().forEach(function (t) { t.stop(); });
            streamRef = null;
            return;
          }
        }
        chunks = [];
        recorder.ondataavailable = function (ev) {
          if (ev.data && ev.data.size) chunks.push(ev.data);
        };
        startedAt = Date.now();
        pausedAccum = 0;
        pauseStart = 0;
        elapsedMs = 0;
        barEnv = 0.08;
        // Amplitude meter (best effort — bars still animate without it).
        try {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
          var src = audioCtx.createMediaStreamSource(stream);
          var analyser = audioCtx.createAnalyser();
          analyser.fftSize = 512;
          src.connect(analyser);
          analyserRef = analyser;
        } catch (e) { analyserRef = null; }
        recorder.start(200);
        state = 'recording';
        pauseIcon.textContent = 'pause';
        pauseBtn.title = 'Pause';
        timeEl.textContent = '0:00';
        setRecordingUI(true);
        ticker = setInterval(tick, 120);
      }).catch(function () {
        fail(hooks, 'Microphone permission is needed to record voice notes.');
      });
    }

    function cleanupCapture() {
      if (ticker) { clearInterval(ticker); ticker = null; }
      if (streamRef) { streamRef.getTracks().forEach(function (t) { t.stop(); }); streamRef = null; }
      if (audioCtx) { try { audioCtx.close(); } catch (e) {} audioCtx = null; }
      analyserRef = null;
      recorder = null;
    }

    function resetToIdle() {
      state = 'idle';
      setRecordingUI(false);
      refresh();
    }

    function finish() {
      if (state === 'idle' || !recorder) return;
      var rec = recorder;
      var dur = elapsedMs;
      rec.onstop = function () {
        cleanupCapture();
        if (dur < MIN_MS || !chunks.length) {
          fail(hooks, 'Recording too short.');
          resetToIdle();
          return;
        }
        var type = mime || (chunks[0] && chunks[0].type) || 'audio/webm';
        var blob = new Blob(chunks, { type: type });
        var name = 'voice_' + Date.now() + '.' + extForMime(type);
        var file;
        try { file = new File([blob], name, { type: type }); }
        catch (e) { blob.name = name; file = blob; }
        resetToIdle();
        if (typeof hooks.onFile === 'function') hooks.onFile(file, dur);
      };
      try { rec.stop(); } catch (e) {
        cleanupCapture();
        resetToIdle();
      }
    }

    function discard() {
      if (state === 'idle' || !recorder) return;
      var rec = recorder;
      rec.onstop = function () { cleanupCapture(); };
      try { rec.stop(); } catch (e) { cleanupCapture(); }
      resetToIdle();
    }

    function togglePause() {
      if (!recorder) return;
      try {
        if (state === 'recording') {
          recorder.pause();
          pauseStart = Date.now();
          state = 'paused';
          pauseIcon.textContent = 'play_arrow';
          pauseBtn.title = 'Resume';
        } else if (state === 'paused') {
          recorder.resume();
          pausedAccum += Date.now() - pauseStart;
          pauseStart = 0;
          state = 'recording';
          pauseIcon.textContent = 'pause';
          pauseBtn.title = 'Pause';
        }
      } catch (e) { /* pause unsupported — keep recording */ }
    }

    // Send-button morphing: mic click starts recording; check finishes.
    sendBtn.addEventListener('click', function (e) {
      var mode = sendBtn.dataset.mode || 'send';
      if (mode === 'mic') { e.preventDefault(); e.stopPropagation(); start(); }
      else if (mode === 'recording') { e.preventDefault(); e.stopPropagation(); finish(); }
    }, true);

    pauseBtn.addEventListener('click', function (e) { e.preventDefault(); togglePause(); });
    deleteBtn.addEventListener('click', function (e) { e.preventDefault(); discard(); });
    if (textarea) textarea.addEventListener('input', refresh);

    var inst = { refresh: refresh, isRecording: function () { return state !== 'idle'; }, start: start, discard: discard };
    wrapper.__voice = inst;
    refresh();
    return inst;
  }

  window.NebVoiceComposer = { attach: attach, supported: supported };
})();
