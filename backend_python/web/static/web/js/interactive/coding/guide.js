const MOOD_COLORS = {
  happy: { body: '#3B82F6', cheek: '#93C5FD' },
  thinking: { body: '#8B5CF6', cheek: '#C4B5FD' },
  celebrate: { body: '#F59E0B', cheek: '#FCD34D' },
  sad: { body: '#64748B', cheek: '#CBD5E1' },
};

export function createGuide(stage, opts = {}) {
  const name = opts.name || 'Neby';
  const wrap = document.createElement('div');
  wrap.className = 'ix-guide';

  const bubble = document.createElement('div');
  bubble.className = 'ix-guide-bubble';
  const bubbleName = document.createElement('span');
  bubbleName.className = 'ix-guide-name';
  bubbleName.textContent = name;
  const bubbleText = document.createElement('span');
  bubbleText.className = 'ix-guide-text';
  bubble.appendChild(bubbleName);
  bubble.appendChild(bubbleText);

  const char = document.createElement('div');
  char.className = 'ix-guide-char';
  char.innerHTML = [
    '<svg viewBox="0 0 64 64" aria-hidden="true">',
    '<ellipse class="gd-shadow" cx="32" cy="58" rx="14" ry="3" fill="rgba(0,0,0,0.18)"/>',
    '<g class="gd-bob">',
    '<rect class="gd-body" x="14" y="14" width="36" height="32" rx="12" fill="#3B82F6"/>',
    '<circle class="gd-antenna" cx="32" cy="9" r="3.4" fill="#FCD34D"/>',
    '<rect x="30.6" y="10" width="2.8" height="6" rx="1.4" fill="#FCD34D"/>',
    '<rect x="19" y="20" width="26" height="16" rx="8" fill="#fff"/>',
    '<g class="gd-eyes">',
    '<circle class="gd-eye" cx="26" cy="28" r="3.2" fill="#0F172A"/>',
    '<circle class="gd-eye" cx="38" cy="28" r="3.2" fill="#0F172A"/>',
    '<circle cx="27" cy="27" r="1" fill="#fff"/>',
    '<circle cx="39" cy="27" r="1" fill="#fff"/>',
    '</g>',
    '<path class="gd-mouth" d="M27 39 Q32 43 37 39" stroke="#0F172A" stroke-width="2" fill="none" stroke-linecap="round"/>',
    '<circle class="gd-cheek" cx="19.5" cy="33" r="2.4" fill="#93C5FD"/>',
    '<circle class="gd-cheek" cx="44.5" cy="33" r="2.4" fill="#93C5FD"/>',
    '<rect class="gd-arm gd-arm-l" x="9" y="26" width="6" height="12" rx="3" fill="#3B82F6"/>',
    '<rect class="gd-arm gd-arm-r" x="49" y="26" width="6" height="12" rx="3" fill="#3B82F6"/>',
    '<rect x="22" y="46" width="7" height="8" rx="3" fill="#2563EB"/>',
    '<rect x="35" y="46" width="7" height="8" rx="3" fill="#2563EB"/>',
    '</g>',
    '</svg>',
  ].join('');

  wrap.appendChild(char);
  wrap.appendChild(bubble);
  stage.appendChild(wrap);

  const bodyParts = char.querySelectorAll('.gd-body, .gd-arm');
  const cheeks = char.querySelectorAll('.gd-cheek');
  const mouth = char.querySelector('.gd-mouth');
  const eyesG = char.querySelector('.gd-eyes');

  let blinkTimer = 0;
  function scheduleBlink() {
    blinkTimer = window.setTimeout(() => {
      eyesG.classList.add('gd-blink');
      window.setTimeout(() => {
        eyesG.classList.remove('gd-blink');
        scheduleBlink();
      }, 160);
    }, 2200 + Math.random() * 2600);
  }
  scheduleBlink();

  let hideTimer = 0;
  let typeTimer = 0;

  function setMood(mood) {
    const m = MOOD_COLORS[mood] || MOOD_COLORS.happy;
    bodyParts.forEach((p) => p.setAttribute('fill', mood === 'happy' ? '#3B82F6' : m.body));
    cheeks.forEach((c) => c.setAttribute('fill', m.cheek));
    if (mood === 'celebrate') {
      mouth.setAttribute('d', 'M26 38 Q32 45 38 38');
      char.classList.add('gd-jump');
      window.setTimeout(() => char.classList.remove('gd-jump'), 900);
    } else if (mood === 'sad') {
      mouth.setAttribute('d', 'M27 41 Q32 37 37 41');
    } else if (mood === 'thinking') {
      mouth.setAttribute('d', 'M28 40 L36 40');
    } else {
      mouth.setAttribute('d', 'M27 39 Q32 43 37 39');
    }
  }

  function say(text, sopts = {}) {
    window.clearTimeout(hideTimer);
    window.clearInterval(typeTimer);
    setMood(sopts.mood || 'happy');
    wrap.classList.remove('ix-guide-hidden');
    bubble.classList.add('ix-guide-bubble-show');
    bubbleText.textContent = '';
    let i = 0;
    typeTimer = window.setInterval(() => {
      i += 2;
      bubbleText.textContent = text.slice(0, i);
      if (i >= text.length) window.clearInterval(typeTimer);
    }, 18);
    if (sopts.duration) {
      hideTimer = window.setTimeout(() => bubble.classList.remove('ix-guide-bubble-show'), sopts.duration);
    }
  }

  function hide() {
    bubble.classList.remove('ix-guide-bubble-show');
  }

  function dispose() {
    window.clearTimeout(blinkTimer);
    window.clearTimeout(hideTimer);
    window.clearInterval(typeTimer);
    wrap.remove();
  }

  return { el: wrap, say, hide, setMood, dispose };
}
