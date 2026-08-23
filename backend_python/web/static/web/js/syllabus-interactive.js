(function () {
  'use strict';

  var E_CHARGE = 1.602e-19;
  var E_MASS = 9.109e-31;
  var H = 6.626e-34;
  var EV = 1.602e-19;

  function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
  function num(v, fallback) { var n = Number(v); return Number.isFinite(n) ? n : fallback; }
  function fmt(v, digits) {
    if (!Number.isFinite(v)) return '—';
    var av = Math.abs(v);
    if ((av !== 0 && av < 0.001) || av >= 10000) return v.toExponential(digits == null ? 2 : digits);
    return v.toFixed(digits == null ? 2 : digits);
  }

  function rangeControl(label, min, max, step, value, unit) {
    var wrap = document.createElement('div');
    wrap.className = 'interactive-control';
    var lab = document.createElement('label');
    var name = document.createElement('span'); name.textContent = label;
    var out = document.createElement('span');
    lab.appendChild(name); lab.appendChild(out);
    var input = document.createElement('input');
    input.type = 'range'; input.min = min; input.max = max; input.step = step; input.value = value;
    function refresh() { out.textContent = input.value + (unit ? ' ' + unit : ''); }
    input.addEventListener('input', refresh); refresh();
    wrap.appendChild(lab); wrap.appendChild(input);
    return { wrap: wrap, input: input, valueLabel: out };
  }

  function selectControl(label, options, value) {
    var wrap = document.createElement('div'); wrap.className = 'interactive-control';
    var lab = document.createElement('label'); var name = document.createElement('span'); name.textContent = label; lab.appendChild(name);
    var sel = document.createElement('select');
    options.forEach(function (opt) {
      var option = document.createElement('option'); option.value = opt.value; option.textContent = opt.label;
      if (opt.value === value) option.selected = true;
      sel.appendChild(option);
    });
    wrap.appendChild(lab); wrap.appendChild(sel);
    return { wrap: wrap, input: sel };
  }

  function makeShell(target) {
    target.innerHTML = '';
    var shell = document.createElement('div'); shell.className = 'interactive-shell';
    var controls = document.createElement('div'); controls.className = 'interactive-controls';
    var stage = document.createElement('div'); stage.className = 'interactive-stage';
    var readout = document.createElement('div'); readout.className = 'interactive-readout';
    controls.appendChild(readout);
    shell.appendChild(controls); shell.appendChild(stage); target.appendChild(shell);
    return { shell: shell, controls: controls, stage: stage, readout: readout };
  }

  function metric(readout, label) {
    var box = document.createElement('div'); box.className = 'interactive-metric';
    var l = document.createElement('span'); l.textContent = label;
    var v = document.createElement('strong'); v.textContent = '—';
    box.appendChild(l); box.appendChild(v); readout.appendChild(box);
    return v;
  }

  function prependControls(shell, controls) {
    var readout = shell.readout;
    controls.forEach(function (c) { shell.controls.insertBefore(c.wrap, readout); });
  }

  function electronMagnetic(target, cfg) {
    var shell = makeShell(target);
    var b = rangeControl('Magnetic field B', 0.05, 0.5, 0.01, num(cfg.B, 0.2), 'T');
    var v = rangeControl('Electron speed v', 0.2, 2.0, 0.05, num(cfg.v_million, 1.0), '×10⁶ m/s');
    prependControls(shell, [b, v]);
    var radiusOut = metric(shell.readout, 'Orbit radius');
    var periodOut = metric(shell.readout, 'Cyclotron period');

    function draw() {
      var B = num(b.input.value, 0.2); var speed = num(v.input.value, 1) * 1e6;
      var r = E_MASS * speed / (E_CHARGE * B);
      var T = 2 * Math.PI * E_MASS / (E_CHARGE * B);
      radiusOut.textContent = fmt(r * 1e6, 2) + ' μm';
      periodOut.textContent = fmt(T * 1e9, 3) + ' ns';
      var rr = clamp(38 + r * 2.8e6, 42, 92);
      shell.stage.innerHTML = '<svg viewBox="0 0 360 230" role="img" aria-label="Electron circular path in a magnetic field">' +
        '<defs><marker id="arr-em" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>' +
        '<g style="color:var(--md-on-surface-variant);opacity:.55">' + Array.from({length:24}, function(_, i){ var x=25+(i%8)*44, y=22+Math.floor(i/8)*82; return '<circle cx="'+x+'" cy="'+y+'" r="7" fill="none" stroke="currentColor"/><circle cx="'+x+'" cy="'+y+'" r="1.8" fill="currentColor"/>'; }).join('') + '</g>' +
        '<circle cx="180" cy="115" r="'+rr+'" fill="none" stroke="var(--md-primary)" stroke-width="4"/>' +
        '<circle cx="'+(180+rr)+'" cy="115" r="7" fill="var(--md-primary)"/>' +
        '<path d="M '+(180+rr)+' 115 C '+(180+rr)+' '+(115-24)+' '+(180+rr-18)+' '+(115-35)+' '+(180+rr-35)+' '+(115-35)+'" fill="none" stroke="var(--md-primary)" stroke-width="3" marker-end="url(#arr-em)"/>' +
        '<text x="180" y="111" text-anchor="middle" fill="var(--md-on-surface)" font-size="13">B perpendicular to motion</text>' +
        '<text x="180" y="130" text-anchor="middle" fill="var(--md-on-surface-variant)" font-size="12">r = mv/(eB)</text>' +
        '</svg><div class="interactive-note">Increasing B tightens the orbit; increasing v makes the radius larger.</div>';
    }
    b.input.addEventListener('input', draw); v.input.addEventListener('input', draw); draw();
  }

  function photoelectric(target, cfg) {
    var shell = makeShell(target);
    var f = rangeControl('Light frequency f', 4, 12, 0.1, num(cfg.frequency_1e14, 8), '×10¹⁴ Hz');
    var phi = rangeControl('Work function φ', 1, 5, 0.1, num(cfg.work_function_ev, 2.2), 'eV');
    prependControls(shell, [f, phi]);
    var photonOut = metric(shell.readout, 'Photon energy');
    var keOut = metric(shell.readout, 'K.E. max');
    var stopOut = metric(shell.readout, 'Stopping potential');
    var thresholdOut = metric(shell.readout, 'Threshold frequency');
    function draw() {
      var freq = num(f.input.value, 8) * 1e14; var work = num(phi.input.value, 2.2);
      var photonEv = H * freq / EV; var ke = Math.max(0, photonEv - work); var f0 = work * EV / H;
      photonOut.textContent = fmt(photonEv, 2) + ' eV'; keOut.textContent = fmt(ke, 2) + ' eV';
      stopOut.textContent = fmt(ke, 2) + ' V'; thresholdOut.textContent = fmt(f0 / 1e14, 2) + ' ×10¹⁴ Hz';
      var emitted = ke > 0;
      shell.stage.innerHTML = '<svg viewBox="0 0 360 230" role="img" aria-label="Photoelectric effect diagram">' +
        '<defs><marker id="arr-pe" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="currentColor"/></marker></defs>' +
        '<rect x="125" y="145" width="180" height="38" rx="6" fill="var(--md-surface-container-high)" stroke="var(--md-outline)"/>' +
        '<text x="215" y="169" text-anchor="middle" fill="var(--md-on-surface)" font-size="13">metal surface</text>' +
        '<g style="color:var(--md-primary)"><path d="M42 42 L78 70 L42 98 L78 126 L112 145" fill="none" stroke="currentColor" stroke-width="4" marker-end="url(#arr-pe)"/></g>' +
        '<text x="40" y="28" fill="var(--md-on-surface)" font-size="12">photon hf</text>' +
        (emitted ? '<circle cx="205" cy="137" r="5" fill="var(--md-primary)"/><path d="M205 132 Q238 82 286 68" fill="none" stroke="var(--md-primary)" stroke-width="3" marker-end="url(#arr-pe)"/><text x="248" y="54" fill="var(--md-on-surface)" font-size="12">photoelectron</text>' : '<text x="215" y="92" text-anchor="middle" fill="var(--md-error)" font-size="13">hf &lt; φ: no emission</text>') +
        '</svg><div class="interactive-note">Einstein relation: hf = φ + K.E.<sub>max</sub>; when emission occurs, eV₀ = K.E.<sub>max</sub>.</div>';
    }
    f.input.addEventListener('input', draw); phi.input.addEventListener('input', draw); draw();
  }

  function youngDoubleSlit(target, cfg) {
    var shell = makeShell(target);
    var wave = rangeControl('Wavelength λ', 400, 700, 5, num(cfg.wavelength_nm, 550), 'nm');
    var D = rangeControl('Screen distance D', 0.5, 2.0, 0.05, num(cfg.screen_m, 1), 'm');
    var d = rangeControl('Slit separation d', 0.1, 1.0, 0.05, num(cfg.slit_mm, 0.5), 'mm');
    prependControls(shell, [wave, D, d]);
    var betaOut = metric(shell.readout, 'Fringe width β');
    var eqOut = metric(shell.readout, 'Relation'); eqOut.textContent = 'β = λD/d';
    function draw() {
      var lam = num(wave.input.value, 550) * 1e-9, dist = num(D.input.value, 1), sep = num(d.input.value, .5) * 1e-3;
      var beta = lam * dist / sep; betaOut.textContent = fmt(beta * 1e3, 2) + ' mm';
      var spacing = clamp(beta * 10000, 12, 42);
      var lines = ''; for (var x = 180; x < 342; x += spacing) lines += '<line x1="'+x+'" y1="25" x2="'+x+'" y2="205" stroke="var(--md-primary)" stroke-width="4" opacity=".75"/>';
      for (var x2 = 180-spacing; x2 > 150; x2 -= spacing) lines += '<line x1="'+x2+'" y1="25" x2="'+x2+'" y2="205" stroke="var(--md-primary)" stroke-width="4" opacity=".75"/>';
      shell.stage.innerHTML = '<svg viewBox="0 0 360 230"><line x1="55" y1="38" x2="55" y2="192" stroke="var(--md-on-surface)" stroke-width="5"/><rect x="51" y="84" width="9" height="10" fill="var(--md-surface-container-lowest)"/><rect x="51" y="136" width="9" height="10" fill="var(--md-surface-container-lowest)"/>' +
        '<line x1="325" y1="22" x2="325" y2="208" stroke="var(--md-on-surface)" stroke-width="3"/>' +
        '<path d="M60 89 Q150 70 325 115 M60 141 Q150 160 325 115" fill="none" stroke="var(--md-on-surface-variant)" stroke-width="1.5" opacity=".7"/>' + lines +
        '<text x="55" y="218" text-anchor="middle" fill="var(--md-on-surface-variant)" font-size="11">double slit</text><text x="325" y="218" text-anchor="middle" fill="var(--md-on-surface-variant)" font-size="11">screen</text></svg>';
    }
    [wave.input,D.input,d.input].forEach(function(i){i.addEventListener('input',draw);}); draw();
  }

  function singleSlit(target, cfg) {
    var shell = makeShell(target);
    var wave = rangeControl('Wavelength λ', 400, 700, 5, num(cfg.wavelength_nm, 600), 'nm');
    var a = rangeControl('Slit width a', 0.05, 0.5, 0.01, num(cfg.slit_mm, 0.2), 'mm');
    var D = rangeControl('Screen distance D', 0.5, 2, 0.05, num(cfg.screen_m, 1), 'm');
    prependControls(shell, [wave,a,D]);
    var widthOut = metric(shell.readout, 'Central maximum width');
    var minOut = metric(shell.readout, 'First minimum');
    function draw(){
      var lam=num(wave.input.value,600)*1e-9, slit=num(a.input.value,.2)*1e-3, dist=num(D.input.value,1);
      var central=2*lam*dist/slit, y1=lam*dist/slit; widthOut.textContent=fmt(central*1e3,2)+' mm'; minOut.textContent=fmt(y1*1e3,2)+' mm';
      var w=clamp(central*8000,32,130);
      shell.stage.innerHTML='<svg viewBox="0 0 360 230"><line x1="60" y1="35" x2="60" y2="195" stroke="var(--md-on-surface)" stroke-width="5"/><rect x="56" y="105" width="9" height="20" fill="var(--md-surface-container-lowest)"/><line x1="315" y1="25" x2="315" y2="205" stroke="var(--md-on-surface)" stroke-width="3"/><path d="M65 115 Q180 78 315 '+(115-w/2)+' M65 115 Q180 152 315 '+(115+w/2)+'" fill="none" stroke="var(--md-on-surface-variant)"/><rect x="307" y="'+(115-w/2)+'" width="16" height="'+w+'" fill="var(--md-primary)" opacity=".75"/><rect x="309" y="'+Math.max(27,115-w/2-35)+'" width="12" height="22" fill="var(--md-primary)" opacity=".28"/><rect x="309" y="'+Math.min(181,115+w/2+13)+'" width="12" height="22" fill="var(--md-primary)" opacity=".28"/><text x="315" y="218" text-anchor="middle" fill="var(--md-on-surface-variant)" font-size="11">diffraction pattern</text></svg>';
    }
    [wave.input,a.input,D.input].forEach(function(i){i.addEventListener('input',draw);}); draw();
  }

  function bohrAtom(target, cfg) {
    var shell = makeShell(target);
    var n = rangeControl('Principal quantum number n', 1, 6, 1, num(cfg.n, 1), ''); prependControls(shell,[n]);
    var radiusOut=metric(shell.readout,'Bohr radius'); var energyOut=metric(shell.readout,'Energy level');
    function draw(){ var nn=num(n.input.value,1); var r=.529*nn*nn; var e=-13.6/(nn*nn); radiusOut.textContent=fmt(r,3)+' Å'; energyOut.textContent=fmt(e,3)+' eV'; var rr=clamp(34+nn*15,48,120);
      shell.stage.innerHTML='<svg viewBox="0 0 360 230"><circle cx="180" cy="115" r="12" fill="var(--md-primary)"/><text x="180" y="120" text-anchor="middle" fill="var(--md-on-primary)" font-size="11">+</text>'+Array.from({length:nn},function(_,i){return '<circle cx="180" cy="115" r="'+(28+(i+1)*15)+'" fill="none" stroke="var(--md-outline)" stroke-width="1" opacity=".6"/>';}).join('')+'<circle cx="'+(180+rr)+'" cy="115" r="7" fill="var(--md-on-surface)"/><text x="180" y="215" text-anchor="middle" fill="var(--md-on-surface-variant)" font-size="12">rₙ ∝ n², Eₙ = −13.6/n² eV</text></svg>'; }
    n.input.addEventListener('input',draw); draw();
  }

  function radioactiveDecay(target, cfg) {
    var shell=makeShell(target); var half=rangeControl('Half-life T½',1,20,1,num(cfg.half_life,10),'time units'); var t=rangeControl('Elapsed time t',0,100,1,num(cfg.time,30),'units'); prependControls(shell,[half,t]);
    var fracOut=metric(shell.readout,'N/N₀ remaining'); var decayOut=metric(shell.readout,'Decay constant λ');
    function draw(){ var T=num(half.input.value,10), time=num(t.input.value,30), frac=Math.pow(2,-time/T), lambda=.693/T; fracOut.textContent=fmt(frac*100,2)+'%'; decayOut.textContent=fmt(lambda,4)+' /unit'; var points=[]; for(var i=0;i<=100;i++){var x=28+i*3.02, y=195-150*Math.pow(2,-i/T); points.push((i===0?'M':'L')+x+' '+y);} var tx=28+time*3.02, ty=195-150*frac;
      shell.stage.innerHTML='<svg viewBox="0 0 360 230"><line x1="28" y1="195" x2="338" y2="195" stroke="var(--md-outline)"/><line x1="28" y1="25" x2="28" y2="195" stroke="var(--md-outline)"/><path d="'+points.join(' ')+'" fill="none" stroke="var(--md-primary)" stroke-width="4"/><circle cx="'+tx+'" cy="'+ty+'" r="6" fill="var(--md-primary)"/><text x="38" y="39" fill="var(--md-on-surface-variant)" font-size="11">N/N₀</text><text x="320" y="214" fill="var(--md-on-surface-variant)" font-size="11">time</text></svg>'; }
    half.input.addEventListener('input',draw); t.input.addEventListener('input',draw); draw();
  }

  function pnJunction(target, cfg) {
    var shell=makeShell(target); var mode=selectControl('Bias mode',[{value:'forward',label:'Forward bias'},{value:'reverse',label:'Reverse bias'}],cfg.mode||'forward'); var volts=rangeControl('Applied voltage magnitude',0,10,.1,num(cfg.voltage,1),'V'); prependControls(shell,[mode,volts]);
    var widthOut=metric(shell.readout,'Depletion layer'); var flowOut=metric(shell.readout,'Current tendency');
    function draw(){ var forward=mode.input.value==='forward', V=num(volts.input.value,1), width=forward?clamp(60-V*5,16,60):clamp(55+V*5,55,110); widthOut.textContent=forward?'narrows':'widens'; flowOut.textContent=forward?'increases after knee':'very small until breakdown'; var left=180-width/2;
      shell.stage.innerHTML='<svg viewBox="0 0 360 230"><rect x="40" y="70" width="140" height="90" rx="6" fill="var(--md-primary-container)"/><rect x="180" y="70" width="140" height="90" rx="6" fill="var(--md-secondary-container)"/><rect x="'+left+'" y="70" width="'+width+'" height="90" fill="var(--md-surface-container-high)" opacity=".9"/><text x="105" y="120" text-anchor="middle" fill="var(--md-on-primary-container)" font-size="24">P</text><text x="255" y="120" text-anchor="middle" fill="var(--md-on-secondary-container)" font-size="24">N</text><text x="180" y="178" text-anchor="middle" fill="var(--md-on-surface-variant)" font-size="11">depletion region</text><text x="180" y="46" text-anchor="middle" fill="var(--md-on-surface)" font-size="13">'+(forward?'Forward bias lowers the barrier':'Reverse bias raises the barrier')+'</text></svg>'; }
    mode.input.addEventListener('change',draw); volts.input.addEventListener('input',draw); draw();
  }

  function thermoProcess(target, cfg) {
    var shell=makeShell(target); var process=selectControl('Process',[{value:'isothermal',label:'Isothermal (T constant)'},{value:'adiabatic',label:'Adiabatic (Q = 0)'}],cfg.process||'isothermal'); var ratio=rangeControl('Expansion ratio V₂/V₁',1.1,4,.1,num(cfg.volume_ratio,2),''); prependControls(shell,[process,ratio]);
    var workOut=metric(shell.readout,'Relative work'); var relationOut=metric(shell.readout,'State relation');
    function draw(){var R=num(ratio.input.value,2), ad=process.input.value==='adiabatic', gamma=1.4; var work=ad?(1-Math.pow(R,1-gamma))/(gamma-1):Math.log(R); workOut.textContent=fmt(work,3)+' (scaled)'; relationOut.textContent=ad?'PV^γ = constant':'PV = constant'; var pts=[]; for(var i=0;i<=90;i++){var x=60+i*2.75, V=1+(R-1)*i/90, P=ad?Math.pow(V,-gamma):1/V, y=190-130*P; pts.push((i===0?'M':'L')+x+' '+y);} shell.stage.innerHTML='<svg viewBox="0 0 360 230"><line x1="50" y1="195" x2="325" y2="195" stroke="var(--md-outline)"/><line x1="50" y1="30" x2="50" y2="195" stroke="var(--md-outline)"/><path d="'+pts.join(' ')+'" fill="none" stroke="var(--md-primary)" stroke-width="4"/><text x="56" y="42" fill="var(--md-on-surface-variant)" font-size="12">P</text><text x="316" y="214" fill="var(--md-on-surface-variant)" font-size="12">V</text><text x="185" y="55" text-anchor="middle" fill="var(--md-on-surface)" font-size="12">'+(ad?'adiabatic':'isothermal')+' expansion</text></svg>';}
    process.input.addEventListener('change',draw); ratio.input.addEventListener('input',draw); draw();
  }

  var renderers = {
    'electron-magnetic-field': electronMagnetic,
    'photoelectric-effect': photoelectric,
    'young-double-slit': youngDoubleSlit,
    'single-slit-diffraction': singleSlit,
    'bohr-atom': bohrAtom,
    'radioactive-decay': radioactiveDecay,
    'pn-junction': pnJunction,
    'thermodynamic-process': thermoProcess
  };

  function renderFormula(el) {
    var latex = el.getAttribute('data-latex') || el.textContent || '';
    if (window.katex) {
      try { window.katex.render(latex, el, { throwOnError: false, displayMode: true }); } catch (e) { /* leave raw text */ }
    }
  }

  function initInteractive(el) {
    if (el.dataset.initialized === '1') return;
    el.dataset.initialized = '1';
    var kind = el.getAttribute('data-interactive-kind'); var configId = el.getAttribute('data-config-id'); var cfg = {};
    if (configId) { var script = document.getElementById(configId); if (script) { try { cfg = JSON.parse(script.textContent || '{}'); } catch(e) { cfg = {}; } } }
    var renderer = renderers[kind];
    if (!renderer) { el.innerHTML = '<div class="interactive-loading">Interactive type not available yet.</div>'; return; }
    renderer(el, cfg);
  }

  function init(root) {
    root = root || document;
    root.querySelectorAll('.rich-formula').forEach(renderFormula);
    root.querySelectorAll('.syllabus-interactive').forEach(initInteractive);
    if (window.renderMathInElement) {
      try {
        window.renderMathInElement(root, {
          delimiters: [
            {left:'$$', right:'$$', display:true}, {left:'\\[', right:'\\]', display:true},
            {left:'$', right:'$', display:false}, {left:'\\(', right:'\\)', display:false}
          ],
          throwOnError: false
        });
      } catch (e) { /* no-op */ }
    }
  }

  window.NebiansSyllabus = { init: init };
})();
