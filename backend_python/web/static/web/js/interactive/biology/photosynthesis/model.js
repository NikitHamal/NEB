// Limiting-factor model (Blackman): the slowest of light, water, CO2 and the enzyme temperature
// response sets the rate. Light is a lamp at distance d, so intensity falls as 1/d².
export const MAX_BUBBLES = 60;

export const FACTORS = [
  { id: 'light', label: 'Light', color: '#facc15' },
  { id: 'water', label: 'Water', color: '#38bdf8' },
  { id: 'co2', label: 'Carbon dioxide', color: '#a3a3a3' },
  { id: 'temperature', label: 'Temperature', color: '#fb923c' },
];

export const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));

export function lightAt(distanceCm) {
  return 2000 * (10 / distanceCm) ** 2;
}

export function temperatureResponse(c) {
  if (c <= 25) return clamp(1 - ((c - 25) / 21) ** 2);
  return clamp(1 - ((c - 25) / 17) ** 2);
}

export function evaluate(levels, opts = {}) {
  const ppfd = lightAt(levels.distance) * (levels.lamp ? 1 : 0) + 15;
  const light = clamp(ppfd / (ppfd + 260));
  const water = opts.submerged ? 1 : clamp((levels.water - 0.12) / 0.78);
  const dissolved = levels.bicarb + 0.02;
  const co2 = clamp(dissolved / (dissolved + 0.22));
  const temperature = temperatureResponse(levels.temperature);
  const responses = { light, water, co2, temperature };
  const order = Object.entries(responses).sort((a, b) => a[1] - b[1]);
  const rate = clamp(order[0][1]);
  const limiting = FACTORS.find((f) => f.id === order[0][0]);
  return {
    rate, ppfd, responses,
    limiting: rate > 0.97 ? null : limiting,
    bubbles: rate * MAX_BUBBLES,
    stomata: clamp(Math.min(water * 1.05, 0.25 + light * 0.85)),
  };
}

export const EQUATION = '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂';
