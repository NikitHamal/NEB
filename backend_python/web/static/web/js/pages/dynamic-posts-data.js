/* Dynamic posts lab data. Mirrors app/src/main/java/com/neb/ians/ui/screens/lab/DynamicLooks.kt:
   same looks, samples and feed mix, so what you pick here is what the app shows. Change both together. */
window.NebDP = (function () {
  'use strict';
  function L(id, name, bg, ink, accent, soft, font, pattern, cap, bar, r, extra) {
    var o = { id: id, name: name, bg: bg, ink: ink, accent: accent, soft: soft, font: font, pattern: pattern, cap: cap, bar: bar, r: r, tall: false, center: false, divider: 'line', mark: true };
    for (var k in extra) o[k] = extra[k];
    return o;
  }
  var LOOKS = [
    L('paper', 'Paper', '#FBF8F1', '#2B2620', '#B4532A', '#EFE7D6', 'serif', 'lines', true, true, 28, { divider: 'dots' }),
    L('ink', 'Ink', '#15171A', '#EDEBE6', '#E9B949', '#24272C', 'serif', 'rings', true, true, 28, { tall: true }),
    L('garden', 'Garden', '#EAF3E4', '#1F3322', '#2F7D46', '#D3E6C9', 'sans', 'waves', false, true, 32, { divider: 'wave' }),
    L('sunrise', 'Sunrise', '#FFF0E0', '#3A2414', '#E2622B', '#FFDDBA', 'sans', 'blobs', false, false, 36, { tall: true, center: true }),
    L('blueprint', 'Blueprint', '#E6EEF7', '#14283D', '#1E5F9E', '#CADBEC', 'mono', 'grid', false, true, 16, {}),
    L('rose', 'Rose', '#FBEAEC', '#3A1D22', '#C03A52', '#F5CFD5', 'serif', 'dots', true, false, 32, { center: true, divider: 'dots' }),
    L('chalk', 'Chalk', '#1E2B25', '#E8EFE6', '#F2D16B', '#2C3D35', 'mono', 'confetti', false, true, 20, {}),
    L('citrus', 'Citrus', '#FFF8D6', '#33300E', '#9A7B00', '#F7EBA0', 'sans', 'stripes', false, false, 24, { tall: true }),
    L('ocean', 'Ocean', '#E3F3F2', '#0E3231', '#0F7B7B', '#C3E4E2', 'sans', 'waves', false, true, 32, { divider: 'wave' }),
    L('mono', 'Mono', '#FFFFFF', '#111111', '#111111', '#EDEDED', 'serif', 'none', true, true, 12, {}),
    L('default', 'Default', '', '', '', '', 'sans', 'none', false, true, 24, {})
  ];
  var SAMPLES = [
    { key: 'story', label: 'Story', tag: 'Study tips', title: 'How I stopped dreading Maths in Class 10',
      lead: 'Last year I could not finish a paper in time. Then I changed three small things, and the marks followed. Here is the plan I wish someone had handed me.',
      mark: 'changed three small things', callout: 'Time yourself from week one, not week ten.',
      quote: 'Do one chapter badly before you do one chapter perfectly.', kind: 'steps',
      items: ['Solve the last five years of papers', 'Keep a mistakes notebook', 'Teach one friend each Sunday'],
      outro: 'None of this is clever. It is repetition with a little honesty, and it works because you can see progress every week.', min: 3, author: 'Anita Gurung' },
    { key: 'guide', label: 'Guide', tag: 'Scholarships', title: 'Your first month checklist for a scholarship form',
      lead: 'Most forms are rejected for missing papers, not weak marks. Keep one folder, tick as you go, and you will never panic on the last day.',
      mark: 'missing papers', callout: 'Scan every paper at 200 dpi or more.',
      quote: 'A complete form beats a perfect essay.', kind: 'checks',
      items: ['Citizenship and birth certificate', 'SEE and +2 mark sheets', 'Recommendation letter', 'Passport size photos', 'Bank statement or income proof'],
      outro: 'Save the folder to your phone and your email. You will reuse it for every form that follows.', min: 4, author: 'Bibek Thapa' },
    { key: 'notice', label: 'Notice', tag: 'Announcement', title: 'Free model test this Saturday for Class 12',
      lead: 'Join us for a full length Physics and Chemistry model test, checked by teachers, with a solved paper shared the same evening.',
      mark: 'checked by teachers', callout: 'Bring a pen, a calculator and a bottle of water.',
      quote: 'Practice under exam rules, once, and the real day feels familiar.', kind: 'steps',
      items: ['Register before Friday 6 pm', 'Reach the hall by 9 am', 'Collect your marked sheet on Monday'],
      outro: 'Seats are limited to the first 120 students.', min: 1, author: 'NEBians Team' }
  ];
  var MIX = [[0, 'paper'], [2, 'default'], [1, 'chalk'], [2, 'sunrise'], [0, 'ocean'], [1, 'citrus'], [0, 'mono'], [2, 'ink']];
  return {
    LOOKS: LOOKS, SAMPLES: SAMPLES, MIX: MIX,
    PATTERNS: ['none', 'dots', 'lines', 'grid', 'waves', 'rings', 'blobs', 'stripes', 'confetti'],
    SWATCHES: ['#B4532A', '#E9B949', '#2F7D46', '#E2622B', '#1E5F9E', '#C03A52', '#6B4E9B', '#0F7B7B']
  };
})();
