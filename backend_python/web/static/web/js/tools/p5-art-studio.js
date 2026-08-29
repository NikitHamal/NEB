(function () {
  'use strict';

  var worker = null;
  var workerReady = false;
  var currentP5Instance = null;
  var isLooping = true;
  var currentArtCode = '';

  var P5_NEEDLE_TOOLS = JSON.stringify([
    {
      name: 'generate_p5_art',
      description: 'Generate dynamic 2D/3D paintings, drawings, and generative art using p5.js canvas.',
      parameters: {
        type: 'object',
        properties: {
          prompt: { type: 'string', description: 'art description or topic e.g. cosmic nebula, flow field, mandala, sunset wave' },
          style: { type: 'string', enum: ['generative', 'fractal', 'landscape', 'pattern', 'animated', 'abstract', ''], description: 'artistic technique' },
          color_palette: { type: 'string', enum: ['vibrant', 'neon', 'pastel', 'monochrome', 'cyberpunk', 'warm', 'cool', ''], description: 'color scheme' },
          complexity: { type: 'string', enum: ['low', 'medium', 'high', 'extreme', ''], description: 'level of visual detail' },
          code: { type: 'string', description: 'optional custom p5.js sketch code' },
        },
        required: ['prompt'],
      },
    },
  ]);

  function init() {
    var genBtn = document.getElementById('p5GenerateBtn');
    var promptInput = document.getElementById('p5PromptInput');
    var playPauseBtn = document.getElementById('p5PlayPauseBtn');
    var reseedBtn = document.getElementById('p5ReseedBtn');
    var saveBtn = document.getElementById('p5SaveBtn');
    var codeToggleBtn = document.getElementById('p5CodeToggleBtn');
    var runCodeBtn = document.getElementById('p5RunCodeBtn');

    if (genBtn) genBtn.addEventListener('click', handleGenerate);

    document.querySelectorAll('.p5-sug-chip').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var p = btn.getAttribute('data-prompt');
        var s = btn.getAttribute('data-style');
        var pal = btn.getAttribute('data-palette');

        if (promptInput && p) promptInput.value = p;
        var styleSel = document.getElementById('p5StyleSelect');
        var palSel = document.getElementById('p5PaletteSelect');
        if (styleSel && s) styleSel.value = s;
        if (palSel && pal) palSel.value = pal;

        handleGenerate();
      });
    });

    if (playPauseBtn) {
      playPauseBtn.addEventListener('click', function () {
        if (!currentP5Instance) return;
        if (isLooping) {
          currentP5Instance.noLoop();
          isLooping = false;
          playPauseBtn.innerHTML = '<span class="material-symbols-outlined">play_arrow</span> Play';
        } else {
          currentP5Instance.loop();
          isLooping = true;
          playPauseBtn.innerHTML = '<span class="material-symbols-outlined">pause</span> Pause';
        }
      });
    }

    if (reseedBtn) {
      reseedBtn.addEventListener('click', function () {
        if (!currentP5Instance) return;
        currentP5Instance.noiseSeed(Math.floor(Math.random() * 10000));
        currentP5Instance.randomSeed(Math.floor(Math.random() * 10000));
        if (typeof currentP5Instance.setup === 'function') currentP5Instance.setup();
        currentP5Instance.redraw();
      });
    }

    if (saveBtn) {
      saveBtn.addEventListener('click', function () {
        if (!currentP5Instance) return;
        currentP5Instance.saveCanvas('p5-needle-art', 'png');
      });
    }

    if (codeToggleBtn) {
      codeToggleBtn.addEventListener('click', function () {
        var box = document.getElementById('p5CodeBox');
        if (box) {
          box.style.display = box.style.display === 'none' ? 'block' : 'none';
        }
      });
    }

    if (runCodeBtn) {
      runCodeBtn.addEventListener('click', function () {
        var textarea = document.getElementById('p5CodeTextarea');
        if (textarea && textarea.value.trim()) {
          renderCanvasCode(textarea.value.trim());
        }
      });
    }

    initNeedleModel();
  }

  function initNeedleModel() {
    var statusEl = document.getElementById('p5ModelStatus');
    if (statusEl) statusEl.textContent = 'Loading Needle 2...';

    try {
      worker = new window.Worker('/static/web/js/needle2/needle.worker.js?v=3');
      worker.addEventListener('message', function (e) {
        var msg = e.data;
        if (!msg) return;
        if (msg.type === 'ready') {
          workerReady = true;
          if (statusEl) statusEl.textContent = 'Needle 2 Local AI Ready';
        }
      });
      worker.postMessage({ type: 'initialize', tools: P5_NEEDLE_TOOLS, snapshotNamespace: 'p5-art-v1' });
    } catch (e) {
      console.error('Needle worker initialization error:', e);
      if (statusEl) statusEl.textContent = 'Needle 2 Cloud Mode';
    }
  }

  function handleGenerate() {
    var promptInput = document.getElementById('p5PromptInput');
    var prompt = promptInput ? promptInput.value.trim() : '';
    if (!prompt) prompt = 'glowing cosmic nebula';

    var style = (document.getElementById('p5StyleSelect') || {}).value || 'generative';
    var palette = (document.getElementById('p5PaletteSelect') || {}).value || 'vibrant';
    var complexity = (document.getElementById('p5ComplexitySelect') || {}).value || 'medium';

    var titleEl = document.getElementById('p5ArtTitle');
    var tagEl = document.getElementById('p5ArtStyleTag');
    if (titleEl) titleEl.textContent = prompt.charAt(0).toUpperCase() + prompt.slice(1);
    if (tagEl) tagEl.textContent = style.toUpperCase() + ' · ' + palette.toUpperCase();

    fetch('/ajax/neby-assist/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      credentials: 'same-origin',
      body: JSON.stringify({
        tool: 'generate_p5_art',
        args: {
          prompt: prompt,
          style: style,
          color_palette: palette,
          complexity: complexity,
        },
      }),
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data && data.result && data.result.code) {
          currentArtCode = data.result.code;
          renderCanvasCode(currentArtCode);
        }
      })
      .catch(function (err) {
        console.error('Error generating artwork:', err);
      });
  }

  function renderCanvasCode(code) {
    var viewport = document.getElementById('p5CanvasViewport');
    var emptyState = document.getElementById('p5EmptyState');
    var codeArea = document.getElementById('p5CodeTextarea');

    if (emptyState) emptyState.style.display = 'none';
    if (codeArea) codeArea.value = code;

    if (currentP5Instance) {
      try { currentP5Instance.remove(); } catch (e) {}
      currentP5Instance = null;
    }

    viewport.innerHTML = '';

    try {
      var sketchFn = new Function('p', 'container',
        'var setup, draw;\n' +
        'with (p) {\n' +
        '  ' + code + '\n' +
        '  if (typeof setup === "function") p.setup = setup;\n' +
        '  if (typeof draw === "function") p.draw = draw;\n' +
        '  var origSetup = p.setup;\n' +
        '  p.setup = function() {\n' +
        '    var w = container.clientWidth || 600;\n' +
        '    var h = container.clientHeight || 440;\n' +
        '    p.createCanvas(w, h);\n' +
        '    if (origSetup && origSetup !== p.setup) origSetup.call(p);\n' +
        '  };\n' +
        '}'
      );

      currentP5Instance = new window.p5(function (p) {
        sketchFn(p, viewport);
      }, viewport);

      isLooping = true;
      var playPauseBtn = document.getElementById('p5PlayPauseBtn');
      if (playPauseBtn) {
        playPauseBtn.innerHTML = '<span class="material-symbols-outlined">pause</span> Pause';
      }
    } catch (e) {
      console.error('Error rendering p5 canvas code:', e);
      viewport.innerHTML = '<div style="color:#ff5252;padding:20px;text-align:center;">Syntax error in p5.js sketch code.</div>';
    }
  }

  function getCsrfToken() {
    var match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
