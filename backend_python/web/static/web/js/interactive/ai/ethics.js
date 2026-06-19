import { createCanvas2D, pointerPos } from '../core/canvas2d.js';
import { createPanel, createHud, showInfoCard } from '../core/sim-ui.js';
import { panelBg, labelText, roundRect, drawTable } from '../biology/bio-utils.js';

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
  const sim = createCanvas2D(stage);
  const hud = createHud(stage);
  const scoreBadge = hud.badge('Score: 0/0', '#a3e635');

  let idx = 0;
  let answered = new Array(SCENARIOS.length).fill(null); // index of chosen option
  let score = 0; let total = 0;

  function current() { return SCENARIOS[idx]; }

  const panel = createPanel(stage, { title: 'AI Ethics & Your Future' });
  panel.info('AI is powerful, but it inherits human bias and raises hard questions about accountability and privacy. Read each scenario, choose the best response, and learn the lesson.');
  panel.button({ label: 'Previous', icon: 'arrow_back', onClick: () => { idx = (idx - 1 + SCENARIOS.length) % SCENARIOS.length); } });
  panel.button({ label: 'Next scenario', icon: 'arrow_forward', onClick: () => { idx = (idx + 1) % SCENARIOS.length; } });
  panel.button({ label: 'Reset score', icon: 'refresh', variant: 'ghost', onClick: () => { answered = new Array(SCENARIOS.length).fill(null); score = 0; total = 0; } });
  panel.divider();
  const scoreOut = panel.readout({ label: 'Your score', value: '0/0' });
  panel.button({ label: 'Why does bias happen?', icon: 'menu_book', variant: 'ghost', onClick: () => {
    showInfoCard(stage, {
      title: 'AI is a mirror',
      body: 'A model can only learn from the data it is given — and that data was made by humans, complete with our prejudices. The AI is not neutral; it reflects society back, magnified. Diverse data and diverse teams are the first defence.',
      color: '#6366F1',
    });
  } });

  function updateScore() {
    scoreBadge.set(`Score: ${score}/${total}`);
    scoreOut.set(`${score}/${total}`);
  }

  function chooseOption(optIdx) {
    if (answered[idx] !== null) return; // already answered this one
    answered[idx] = optIdx;
    const opt = current().options[optIdx];
    total++;
    if (opt.correct) score++;
    updateScore();
    showInfoCard(stage, {
      title: opt.correct ? 'Correct ✓' : 'Not quite',
      body: opt.explain + '\n\n' + current().lesson,
      color: opt.correct ? '#a3e635' : '#fbbf24',
    });
  }

  function geom(w, h) {
    return { x: 20, y: 20, w: w - 40, h: h - 100 };
  }

  function onClick(e) {
    const p = pointerPos(sim.canvas, e);
    const g = geom(sim.width, sim.height);
    const sc = current();
    // option boxes
    const optY = g.y + 130;
    sc.options.forEach((opt, i) => {
      const oy = optY + i * 56;
      if (p.x >= g.x + 16 && p.x <= g.x + g.w - 16 && p.y >= oy && p.y <= oy + 48) {
        chooseOption(i);
      }
    });
  }
  sim.canvas.addEventListener('click', onClick);

  sim.setUpdate((ctx) => {
    const { width: w, height: h } = sim;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#070a14'; ctx.fillRect(0, 0, w, h);
    const g = geom(w, h);
    panelBg(ctx, g.x, g.y, g.w, g.h);

    const sc = current();
    // progress dots
    SCENARIOS.forEach((s, i) => {
      const dx = g.x + 20 + i * 22;
      const dy = g.y + 20;
      ctx.fillStyle = i === idx ? '#a3e635' : answered[i] !== null ? '#34d399' : '#334155';
      ctx.beginPath(); ctx.arc(dx, dy, 7, 0, Math.PI * 2); ctx.fill();
    });

    labelText(ctx, `Scenario ${idx + 1} of ${SCENARIOS.length}: ${sc.title}`, g.x + 20, g.y + 56,
      { color: '#e2e8f0', size: 16 });
    // description (wrap)
    wrapText(ctx, sc.desc, g.x + 20, g.y + 86, g.w - 40, 20, { color: '#94a3b8', size: 12 });

    // options
    const optY = g.y + 130;
    sc.options.forEach((opt, i) => {
      const oy = optY + i * 56;
      const answeredThis = answered[idx] !== null;
      const isChosen = answered[idx] === i;
      let bg = 'rgba(99,102,241,0.10)'; let border = '#475569';
      if (answeredThis) {
        if (opt.correct) { bg = 'rgba(52,211,153,0.18)'; border = '#34d399'; }
        else if (isChosen) { bg = 'rgba(248,113,113,0.18)'; border = '#f87171'; }
        else { bg = 'rgba(71,85,105,0.10)'; border = '#334155'; }
      }
      ctx.fillStyle = bg; ctx.strokeStyle = border; ctx.lineWidth = 1.5;
      roundRect(ctx, g.x + 16, oy, g.w - 32, 48, 8); ctx.fill(); ctx.stroke();
      const letter = String.fromCharCode(65 + i);
      ctx.fillStyle = border; ctx.font = '700 14px Poppins, sans-serif';
      ctx.fillText(letter, g.x + 30, oy + 28);
      wrapText(ctx, opt.label, g.x + 54, oy + 18, g.w - 100, 16, { color: '#e2e8f0', size: 13 });
      if (answeredThis && opt.correct) {
        ctx.fillStyle = '#34d399'; ctx.font = '700 14px Poppins, sans-serif';
        ctx.fillText('✓', g.x + g.w - 36, oy + 28);
      }
    });

    // lesson if answered
    if (answered[idx] !== null) {
      const ly = optY + sc.options.length * 56 + 12;
      panelBg(ctx, g.x + 16, ly, g.w - 32, 50);
      labelText(ctx, '💡 Lesson', g.x + 28, ly + 18, { color: '#fbbf24', size: 11 });
      wrapText(ctx, sc.lesson, g.x + 28, ly + 36, g.w - 60, 14, { color: '#e2e8f0', size: 12 });
    }
  });

  sim.start();
  updateScore();

  return {
    dispose() {
      sim.canvas.removeEventListener('click', onClick);
      panel.dispose(); hud.dispose(); sim.dispose();
    },
  };
}

function wrapText(ctx, text, x, y, maxW, lineH, opts = {}) {
  ctx.font = `${opts.weight || 500} ${opts.size || 12}px Poppins, sans-serif`;
  ctx.fillStyle = opts.color || '#e2e8f0';
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  const words = text.split(/\s+/);
  let line = ''; let cy = y;
  for (let i = 0; i < words.length; i++) {
    const test = line + (line ? ' ' : '') + words[i];
    if (ctx.measureText(test).width > maxW && line) {
      ctx.fillText(line, x, cy); line = words[i]; cy += lineH;
    } else { line = test; }
  }
  if (line) ctx.fillText(line, x, cy);
}
