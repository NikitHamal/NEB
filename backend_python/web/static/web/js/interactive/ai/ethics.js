/**
 * AI in your life — a hiring model learns from past decisions that were biased against group B.
 * Both groups have the same spread of skill, but a logistic-regression model trained on those
 * past decisions (by gradient descent, right here) reproduces the bias. Hide the group from the
 * model and it can still find it through a proxy (home area); only fixing the data removes it.
 * Tap an applicant to see their case. Four real dilemmas follow in the panel.
 */
import { createKit, T, Spring, fmt, text, withAlpha, card } from '../core/kit2d.js';
import { createPanel, createHud } from '../core/sim-ui.js';

const SCENARIOS = [
  {
    id: 'hiring', title: 'AI résumé screener',
    desc: 'A company trains an AI to rank job applicants from past hiring data. But the company historically hired mostly men. What happens?',
    options: [
      { label: 'The AI will be perfectly fair', correct: false,
        explain: 'No — the AI learns the patterns in its data. If past hiring favoured men, the AI will too, because that is the pattern it was trained on.' },
      { label: 'The AI will favour men, copying the bias', correct: true,
        explain: 'Correct. The model faithfully reproduces the bias in its training data. Without intervention it amplifies existing prejudice.' },
      { label: 'The AI refuses to rank anyone', correct: false,
        explain: 'No — the model has no concept of fairness unless humans build it in. It simply predicts from patterns.' },
    ],
    lesson: 'Bias enters AI through data. Diverse data, fairness audits, and human oversight are needed to counter it.',
  },
  {
    id: 'selfdriving', title: 'Self-driving car crash',
    desc: 'A self-driving car makes a decision per second. If it crashes and injures someone, who is responsible?',
    options: [
      { label: 'The car manufacturer', correct: false,
        explain: 'Partly — but the law is still unclear. There is no single agreed answer yet.' },
      { label: 'The programmer who wrote the AI', correct: false,
        explain: 'Partly — but millions of lines of code and learned weights make blame hard to pin on any one person.' },
      { label: 'It is an unsolved accountability problem', correct: true,
        explain: 'Correct. Our laws were built around human decisions. AI that acts millions of times per second does not fit, and accountability is an open problem.' },
    ],
    lesson: 'Accountability for AI decisions is an unsolved ethical and legal problem. Humans must stay in the loop for high-stakes choices.',
  },
  {
    id: 'medical', title: 'AI diagnoses an X-ray',
    desc: 'A hospital uses AI to flag possible cancer in X-rays. The AI is faster than any doctor. Should they trust it fully?',
    options: [
      { label: 'Yes — it is faster, so always trust it', correct: false,
        explain: 'No. AI can be confidently wrong, and a false negative here could cost a life. Trust must be earned, not assumed.' },
      { label: 'Use it as a tool, with doctors checking', correct: true,
        explain: 'Correct. Doctor-plus-AI catches more cancers than either alone. The AI augments the human; it does not replace the judgement.' },
      { label: 'Never use AI in medicine', correct: false,
        explain: 'No — used carefully, AI genuinely saves lives. The key is thoughtful use, not refusal.' },
    ],
    lesson: 'AI is a powerful tool that augments humans. Human-plus-AI usually beats either alone — provided we check the output.',
  },
  {
    id: 'privacy', title: 'Free chatbot reads your data',
    desc: 'A free AI assistant improves by learning from everything you type, including private messages. Acceptable?',
    options: [
      { label: 'Yes — it is free, so fair trade', correct: false,
        explain: 'Not necessarily. "Free" can mean paying with your personal data, which may be stored, shared, or leaked.' },
      { label: 'Only if you understand and agree', correct: true,
        explain: 'Correct. Informed consent matters. You should know what is collected, who sees it, and what it is used to decide about you.' },
      { label: 'AI cannot learn from private data', correct: false,
        explain: 'False. Many models are trained on user input. The question is whether you agreed to that.' },
    ],
    lesson: 'Asking who owns your data, who can see it, and what it decides about you is now basic digital literacy.',
  },
];
export default function init(stage) {
  const k = createKit(stage, { trackPointer: true, label: 'A hiring model trained on biased past decisions, with selection rates by group' });
  const hud = createHud(stage);
  const badge = hud.badge('Raise the bias in the past data and retrain', '#db2777');

  const NA = 240;
  const skill = new Float64Array(NA), area = new Float64Array(NA), grp = new Uint8Array(NA), hired = new Uint8Array(NA), score = new Float64Array(NA);
  const w = new Float64Array(4);
  let bias = 1.6, useGroup = true, useArea = true, picked = -1, rateA = 0, rateB = 0;
  const barA = new Spring(0, 120, 16), barB = new Spring(0, 120, 16);

  const panel = createPanel(stage, { title: 'Bias in, bias out' });
  panel.slider({ label: 'Bias in the past hiring decisions', min: 0, max: 3, step: 0.1, value: bias, format: (v) => (v === 0 ? 'none' : v.toFixed(1)), onChange: (v) => { bias = v; build(); } });
  panel.toggle({ label: 'Model may see the group', value: true, onChange: (v) => { useGroup = v; train(); } });
  panel.toggle({ label: 'Model may see the home area (a proxy)', value: true, onChange: (v) => { useArea = v; train(); } });
  const st = panel.stats([{ key: 'a', label: 'Group A selected' }, { key: 'b', label: 'Group B selected' }, { key: 'ratio', label: 'B ÷ A (fair ≥ 0.8)' }, { key: 'w', label: 'Weight on group' }]);
  panel.section('Real dilemmas');
  const qWrap = document.createElement('div'); qWrap.className = 'ix-ctrl-row'; panel.body.appendChild(qWrap);
  let qi = 0;
  function showQ() {
    const s = SCENARIOS[qi];
    qWrap.innerHTML = '';
    const h = document.createElement('div'); h.className = 'ix-ctrl-label'; h.style.fontWeight = '700'; h.textContent = `${qi + 1}/${SCENARIOS.length} · ${s.title}`;
    const p = document.createElement('p'); p.className = 'ix-ctrl-info'; p.textContent = s.desc;
    const box = document.createElement('div'); box.className = 'k2-chips'; box.style.flexDirection = 'column'; box.style.alignItems = 'stretch';
    const out = document.createElement('p'); out.className = 'ix-ctrl-info';
    s.options.forEach((o) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'k2-chip'; b.style.justifyContent = 'flex-start'; b.style.whiteSpace = 'normal'; b.style.textAlign = 'left'; b.style.lineHeight = '1.3'; b.textContent = o.label;
      b.addEventListener('click', () => { [...box.children].forEach((c) => c.classList.remove('is-on')); b.classList.add('is-on'); b.style.background = o.correct ? '#16a34a' : '#e5484d'; b.style.borderColor = b.style.background; out.textContent = `${o.explain} ${o.correct ? s.lesson : ''}`; });
      box.appendChild(b);
    });
    const next = document.createElement('button'); next.type = 'button'; next.className = 'ix-ctrl-btn ix-ctrl-btn-ghost'; next.textContent = 'Next dilemma';
    next.addEventListener('click', () => { qi = (qi + 1) % SCENARIOS.length; showQ(); });
    qWrap.append(h, p, box, out, next);
  }
  showQ();

  function build() {
    let s = 12345; const r = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
    for (let i = 0; i < NA; i++) {
      grp[i] = i % 2; skill[i] = Math.min(1, Math.max(0, 0.5 + (r() + r() + r() - 1.5) * 0.45));
      area[i] = Math.min(1, Math.max(0, (grp[i] ? 0.3 : 0.7) + (r() - 0.5) * 0.5));
      const z = 7 * (skill[i] - 0.55) + (grp[i] ? -bias : bias) * 0.9;
      hired[i] = r() < 1 / (1 + Math.exp(-z)) ? 1 : 0;
    }
    train();
  }
  function feat(i, out) { out[0] = skill[i] - 0.5; out[1] = useGroup ? (grp[i] ? -0.5 : 0.5) : 0; out[2] = useArea ? area[i] - 0.5 : 0; out[3] = 1; return out; }
  const F = new Float64Array(4), G = new Float64Array(4);
  function train() {
    w.fill(0);
    for (let it = 0; it < 400; it++) {
      G.fill(0);
      for (let i = 0; i < NA; i++) { feat(i, F); let z = 0; for (let j = 0; j < 4; j++) z += w[j] * F[j]; const p = 1 / (1 + Math.exp(-z)), e = p - hired[i]; for (let j = 0; j < 4; j++) G[j] += e * F[j]; }
      for (let j = 0; j < 4; j++) w[j] -= 1.5 * G[j] / NA;
    }
    let sa = 0, na = 0, sb = 0, nb = 0;
    for (let i = 0; i < NA; i++) { feat(i, F); let z = 0; for (let j = 0; j < 4; j++) z += w[j] * F[j]; score[i] = 1 / (1 + Math.exp(-z)); const sel = score[i] > 0.5; if (grp[i]) { nb++; if (sel) sb++; } else { na++; if (sel) sa++; } }
    rateA = sa / na; rateB = sb / nb; barA.to(rateA); barB.to(rateB); k.animate(true);
  }

  let cx = 0, cy = 0, cw = 0, ch = 0, bx = 0, byy = 0;
  k.onResize((W, H) => {
    if (k.small) { cx = 34; cy = 44; cw = W - 48; ch = H * 0.52; bx = 14; byy = cy + ch + 34; }
    else { cx = 50; cy = 50; cw = W * 0.58; ch = H - 100; bx = cx + cw + 30; byy = 60; }
  });
  const PX = (v) => cx + v * cw, PY = (v) => cy + ch - v * ch;
  k.drag({
    hit: (x, y, s) => { for (let i = 0; i < NA; i++) if (Math.hypot(x - PX(skill[i]), y - PY(area[i])) < 6 + s) return 1; return false; },
    down: (x, y) => { let bd = 1e9; for (let i = 0; i < NA; i++) { const d = Math.hypot(x - PX(skill[i]), y - PY(area[i])); if (d < bd) { bd = d; picked = i; } } k.invalidate(); },
    cursor: 'pointer', cursorActive: 'pointer',
  });

  k.frame((ctx, dt, W, H) => {
    const anim = barA.step(dt) | barB.step(dt);
    ctx.fillStyle = '#f7f8fd'; ctx.fillRect(0, 0, W, H);
    card(ctx, cx - 8, cy - 8, cw + 16, ch + 16, 12);
    // model's decision boundary in (skill, area) for each group
    for (let g = 0; g < 2; g++) {
      const gv = useGroup ? (g ? -0.5 : 0.5) : 0;
      ctx.strokeStyle = g ? withAlpha('#db2777', 0.8) : withAlpha('#2563eb', 0.8); ctx.lineWidth = 2; ctx.setLineDash(g ? [6, 4] : []);
      ctx.beginPath();
      for (let t = 0; t <= 20; t++) { const a = t / 20, ae = useArea ? a - 0.5 : 0; const s0 = -(w[1] * gv + w[2] * ae + w[3]) / (w[0] || 1e-6) + 0.5; const X = PX(Math.min(1.05, Math.max(-0.05, s0))), Y = PY(a); if (t) ctx.lineTo(X, Y); else ctx.moveTo(X, Y); }
      ctx.stroke(); ctx.setLineDash([]);
    }
    for (let i = 0; i < NA; i++) {
      const X = PX(skill[i]), Y = PY(area[i]), c = grp[i] ? '#db2777' : '#2563eb';
      ctx.globalAlpha = hired[i] ? 1 : 0.35;
      if (grp[i]) { ctx.fillStyle = c; ctx.beginPath(); ctx.moveTo(X, Y - 5); ctx.lineTo(X + 4.5, Y + 4); ctx.lineTo(X - 4.5, Y + 4); ctx.closePath(); ctx.fill(); }
      else { ctx.fillStyle = c; ctx.beginPath(); ctx.arc(X, Y, 4, 0, Math.PI * 2); ctx.fill(); }
      ctx.globalAlpha = 1;
      if (i === picked) { ctx.strokeStyle = T.ink; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(X, Y, 9, 0, Math.PI * 2); ctx.stroke(); }
    }
    text(ctx, 'skill test score →', cx + cw, cy + ch + 24, T.ink2, 10.5, 600, 'right');
    ctx.save(); ctx.translate(cx - 24, cy + ch / 2); ctx.rotate(-Math.PI / 2); text(ctx, 'home area (a proxy for group)', 0, 0, T.ink2, 10.5, 600, 'center'); ctx.restore();
    if (!k.small) text(ctx, 'solid = hired in the past · faded = rejected · blue line / pink dashes = the model\'s pass mark for A / B', cx, cy + ch + 24, T.mute, 10, 600);
    // selection bars
    const bw = k.small ? (W - 28) / 2 - 10 : W - bx - 24;
    const bars = [['Group A', barA.x, '#2563eb'], ['Group B', barB.x, '#db2777']];
    for (let i = 0; i < 2; i++) {
      const [lab, v, col] = bars[i], x0 = k.small ? bx + i * (bw + 20) : bx, y0 = k.small ? byy : byy + i * 60;
      text(ctx, `${lab}: ${fmt(v * 100, 0)} % selected`, x0, y0, T.ink, 11.5, 700);
      ctx.fillStyle = T.line2; ctx.beginPath(); ctx.roundRect(x0, y0 + 10, bw, 14, 7); ctx.fill();
      ctx.fillStyle = col; ctx.beginPath(); ctx.roundRect(x0, y0 + 10, bw * v, 14, 7); ctx.fill();
    }
    if (!k.small && picked >= 0) {
      const y0 = byy + 140;
      card(ctx, bx, y0, bw, 130, 12);
      text(ctx, `Applicant #${picked + 1} · group ${grp[picked] ? 'B' : 'A'}`, bx + 12, y0 + 22, T.ink, 11.5, 700);
      text(ctx, `skill ${fmt(skill[picked] * 100, 0)} / 100`, bx + 12, y0 + 46, T.ink2, 10.5, 600);
      text(ctx, `past decision: ${hired[picked] ? 'hired' : 'rejected'}`, bx + 12, y0 + 66, T.ink2, 10.5, 600);
      text(ctx, `model score: ${fmt(score[picked] * 100, 0)} % → ${score[picked] > 0.5 ? 'interview' : 'reject'}`, bx + 12, y0 + 86, score[picked] > 0.5 ? T.green : T.red, 11, 700);
      text(ctx, 'Both groups have the same spread of skill.', bx + 12, y0 + 112, T.mute, 10, 500);
    }
    const ratio = rateA > 0 ? rateB / rateA : 1;
    st.a.set(`${fmt(rateA * 100, 0)} %`); st.b.set(`${fmt(rateB * 100, 0)} %`); st.ratio.set(fmt(ratio, 2)); st.w.set(useGroup ? fmt(w[1], 2) : 'hidden');
    badge.set(ratio < 0.8 ? (useGroup ? 'The model copied the bias in the past decisions' : useArea ? 'Group hidden, but home area still leaks it: bias via a proxy' : 'Still unfair: the past labels themselves are biased') : 'Selection rates are close: much fairer');
    k.animate(!!anim);
  });

  build();
  k.debug = { rates: () => [rateA, rateB], pick: () => [PX(skill[3]), PY(area[3])] };
  return { dispose() { k.dispose(); panel.dispose(); hud.dispose(); } };
}
