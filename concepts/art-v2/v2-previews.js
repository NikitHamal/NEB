/* NEBians M3X Art Library v2 — Live In-App Previews, Custom Studio & V1 vs V2 Side-by-Side Comparison. */
(function (g) {
  'use strict';
  var V = g.NebArtV2;

  function avSvg(letter, shape, pal, mode) {
    var T = V.palette(pal, mode);
    return '<svg class="pc-av" viewBox="0 0 100 100" aria-hidden="true"><path d="' + V.shapeD(shape, 50, 50, 46, 0) + '" fill="' + T[2] + '"/><text x="50" y="52" text-anchor="middle" dominant-baseline="central" font-size="38" font-weight="600" fill="' + T[5] + '">' + letter + '</text></svg>';
  }

  /* 1. Render In-App Preview Showcase (Profiles v3, Resource Cards, 3D Labs, Books, Empty States) */
  V.renderInApp = function (mode, salt) {
    var s = salt * 131;
    var profiles = [
      { name: 'Aarav Adhikari', role: 'Grade 12 Science · St. Xavier\'s', badge: 'school', letter: 'A', shape: 'cookie', pal: 'brand', lay: 'roleStudent', seed: 101 + s, vf: true, cta: 'Follow' },
      { name: 'Dr. Prativa Sharma', role: 'Senior Physics Lecturer', badge: 'auto_stories', letter: 'P', shape: 'sunny', pal: 'teal', lay: 'roleTeacher', seed: 118 + s, vf: true, cta: 'Call' },
      { name: 'Kathmandu Model College', role: 'Bagbazar, Kathmandu · NEB & BCA', badge: 'account_balance', letter: 'K', shape: 'squircle', pal: 'amber', lay: 'roleInstitution', seed: 135 + s, vf: true, cta: 'Call' }
    ];
    var resources = [
      { title: 'Wave Optics, Interference & Diffraction Complete Derivation Notes', subj: 'Physics', type: 'Notes', meta: 'Grade 12 · 28 pages · PDF', by: 'Dr. Prativa Sharma', views: '4.8k', seed: 1001 + s },
      { title: 'Volumetric Titration, Organic Reaction Mechanisms & Past Solutions', subj: 'Chemistry', type: 'Solved paper', meta: 'Grade 12 · 2081 Set A', by: 'Rohan Thapa', views: '3.2k', seed: 1009 + s },
      { title: 'DNA Replication, Molecular Genetics & Cell Division Master Guide', subj: 'Biology', type: 'Revision guide', meta: 'Grade 12 · 34 diagrams', by: 'Asha Gurung', views: '5.1k', seed: 1017 + s },
      { title: 'Integration by Parts, Differential Equations & Vector Calculus', subj: 'Mathematics', type: 'Formula book', meta: 'Grade 12 · 110 solved', by: 'Bikash KC', views: '6.4k', seed: 1025 + s },
      { title: 'C Programming Pointers, Data Structures & DBMS SQL Queries', subj: 'Computer Science', type: 'Lab manual', meta: 'Grade 12 / BCA · 42 programs', by: 'Nikit Hamal', views: '7.9k', seed: 1033 + s },
      { title: 'Macroeconomic Indicators, Nepal Rastra Bank Monetary Policy & Trade', subj: 'Economics', type: 'Model set', meta: 'Grade 12 · 5 full sets', by: 'Sujata Karki', views: '2.7k', seed: 1065 + s }
    ];
    var html = '<div class="sec-h"><span>Profiles v3 — Role-tailored M3X covers & frameless expressive avatars</span></div><div class="mock-grid">';
    profiles.forEach(function (p) {
      html += '<article class="pcard"><div class="pc-cov">' + V.make({ kind: 'cover', seed: p.seed, layout: p.lay, palette: p.pal, mode: mode }) + '</div>' +
        '<div class="pc-body"><div class="pc-top">' + avSvg(p.letter, p.shape, p.pal, mode) + '<button class="btn ' + (p.cta === 'Call' ? 't' : 'f') + ' sm"><span class="ms">' + (p.cta === 'Call' ? 'call' : 'person_add') + '</span>' + p.cta + '</button></div>' +
        '<div class="pc-name">' + p.name + (p.vf ? '<span class="ms f" style="color:var(--md-primary)">verified</span>' : '') + '</div>' +
        '<div class="pc-role"><span class="ms" style="font-size:16px">' + p.badge + '</span>' + p.role + '</div></div></article>';
    });
    html += '</div><div class="sec-h"><span>Library Resource Cards — Bespoke subject scene thumbnails with Read action</span></div><div class="mock-grid">';
    resources.forEach(function (r) {
      html += '<article class="rcard"><div class="rc-art">' + V.make({ kind: 'thumb', seed: r.seed, subject: r.subj, mode: mode }) + '<span class="rc-type">' + r.type + '</span></div>' +
        '<div class="rc-body"><div style="display:flex;align-items:center;gap:6px"><span class="pill"><span class="ms" style="font-size:15px">' + V.glyphFor(r.subj) + '</span>' + r.subj + '</span><small style="color:var(--md-on-surface-variant);font-size:.74rem">' + r.meta + '</small></div>' +
        '<div class="rc-title">' + r.title + '</div>' +
        '<div class="rc-foot"><span>' + r.by + ' · ' + r.views + ' reads</span><button class="btn t sm"><span class="ms" style="font-size:16px">menu_book</span>Read</button></div></div></article>';
    });
    html += '</div><div class="sec-h"><span>3D Interactive Labs & Career Pathways</span></div><div class="mock-grid">';
    ['Physics', 'Chemistry', 'Space & Astronomy'].forEach(function (sub, i) {
      html += '<article class="rcard"><div class="rc-art" style="aspect-ratio:20/9">' + V.make({ kind: 'lab', seed: 2601 + i * 2 + s, subject: sub, mode: mode }) + '<span class="rc-type">3D Interactive Lab</span></div>' +
        '<div class="rc-body"><div class="rc-title">' + sub + ' Virtual Simulation Bench</div><div class="rc-foot"><span>WebGL 2.0 · Fullscreen ready</span><button class="btn f sm"><span class="ms" style="font-size:16px">view_in_ar</span>Launch lab</button></div></div></article>';
    });
    html += '</div>';
    return html;
  };

  /* 2. Render V1 vs V2 Side-by-Side Comparison */
  V.renderCompare = function (mode, salt) {
    var N1 = g.NebArt, s = salt * 89;
    var cases = [
      { label: 'Physics Resource Thumbnail', kind: 'thumb', subject: 'Physics', seed: 12 + s, why: 'V2 draws an optical prism dispersing 4 flat-tonal spectrum beams + wave packet instead of abstract circles.' },
      { label: 'Chemistry Resource Thumbnail', kind: 'thumb', subject: 'Chemistry', seed: 24 + s, why: 'V2 draws a volumetric Erlenmeyer flask with liquid meniscus + hexagonal benzene molecular lattice.' },
      { label: 'Biology Resource Thumbnail', kind: 'thumb', subject: 'Biology', seed: 36 + s, why: 'V2 draws a twisted DNA double-helix base-pair ladder + cellular organelle cross-section.' },
      { label: 'Computer Science Thumbnail', kind: 'thumb', subject: 'Computer Science', seed: 48 + s, why: 'V2 draws a framed code editor window with flat syntax pills + binary tree node-edge graph.' },
      { label: 'Nepal / School Heritage Banner', kind: 'school', subject: 'Nepali', layout: 'nepalHimalaya', seed: 60 + s, why: 'V2 draws layered Machhapuchhre / Everest ridgelines with sunlit snow facets & terraced valleys.' },
      { label: 'Mathematics Textbook Cover', kind: 'book', subject: 'Mathematics', seed: 72 + s, why: 'V2 renders a framed Swiss/MIT-Press textbook plate with Fibonacci spiral & Riemann integral bars.' }
    ];
    var html = '<div class="sec-h"><span>Direct Comparison — Previous Agent V1 vs New M3X Art Library V2</span></div><div class="mock-grid" style="grid-template-columns:repeat(auto-fit,minmax(440px,1fr))">';
    cases.forEach(function (c) {
      var svg1 = N1 ? N1.make({ kind: c.kind, seed: c.seed, subject: c.subject, mode: mode }) : '';
      var svg2 = V.make({ kind: c.kind, seed: c.seed, subject: c.subject, layout: c.layout, mode: mode });
      html += '<article class="pcard" style="padding:18px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><b style="font-size:.92rem">' + c.label + '</b><span class="pill">' + c.subject + '</span></div>' +
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">' +
        '<div><small style="display:block;margin-bottom:6px;font-weight:600;color:var(--md-on-surface-variant)">V1 (Abstract pattern)</small><div style="border-radius:16px;overflow:hidden;border:1px solid var(--md-outline-variant)">' + svg1 + '</div></div>' +
        '<div><small style="display:block;margin-bottom:6px;font-weight:600;color:var(--md-primary)">V2 (Domain scene + 8-tone M3X)</small><div style="border-radius:16px;overflow:hidden;border:1.5px solid var(--md-primary)">' + svg2 + '</div></div>' +
        '</div><p style="font-size:.78rem;color:var(--md-on-surface-variant);margin-top:10px;line-height:1.45">' + c.why + '</p></article>';
    });
    return html + '</div>';
  };
})(typeof window !== 'undefined' ? window : globalThis);
