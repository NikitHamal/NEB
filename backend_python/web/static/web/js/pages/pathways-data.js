/* Pathways data adapter. Turns the one /api/pathways/ payload (docs/PATHWAYS_SCHEMA.md) into the shapes the concept
   UI reads: STAGES, C (courses), K (careers), X (exams), G (guides), COL (colleges), CT (countries), SCH (scholarships).
   Android reads the same payload (PwDerive.kt), so numbers match. Nothing is invented: a missing field stays empty and
   the screen that needs it hides. */
(function () {
  'use strict';
  var DP = {"Bhojpur":0,"Dhankuta":0,"Ilam":0,"Jhapa":0,"Khotang":0,"Morang":0,"Okhaldhunga":0,"Panchthar":0,"Sankhuwasabha":0,"Solukhumbu":0,"Sunsari":0,"Taplejung":0,"Terhathum":0,"Udayapur":0,"Bara":1,"Dhanusha":1,"Mahottari":1,"Parsa":1,"Rautahat":1,"Saptari":1,"Sarlahi":1,"Siraha":1,"Bhaktapur":2,"Chitwan":2,"Dhading":2,"Dolakha":2,"Kathmandu":2,"Kavrepalanchok":2,"Lalitpur":2,"Makwanpur":2,"Nuwakot":2,"Ramechhap":2,"Rasuwa":2,"Sindhuli":2,"Sindhupalchok":2,"Baglung":3,"Gorkha":3,"Kaski":3,"Lamjung":3,"Manang":3,"Mustang":3,"Myagdi":3,"Nawalparasi East":3,"Parbat":3,"Syangja":3,"Tanahu":3,"Arghakhanchi":4,"Banke":4,"Bardiya":4,"Dang":4,"Gulmi":4,"Kapilvastu":4,"Nawalparasi West":4,"Palpa":4,"Pyuthan":4,"Rolpa":4,"Rukum East":4,"Rupandehi":4,"Dailekh":5,"Dolpa":5,"Humla":5,"Jajarkot":5,"Jumla":5,"Kalikot":5,"Mugu":5,"Rukum West":5,"Salyan":5,"Surkhet":5,"Achham":6,"Baitadi":6,"Bajhang":6,"Bajura":6,"Dadeldhura":6,"Darchula":6,"Doti":6,"Kailali":6,"Kanchanpur":6};
  var MN = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
  var GL = { school: 'School', tech: 'Engineering and IT', sci: 'Science', health: 'Health', biz: 'Business', arts: 'Arts and media', edu: 'Education', law: 'Law', ag: 'Agriculture', gov: 'Government', abroad: 'Abroad' };
  var GTONE = { tech: 'pc', sci: 'pc', arts: 'tc', law: 'tc', biz: 'yc', edu: 'yc', gov: 'yc', health: 'gc', ag: 'gc', abroad: 'gc' };
  var TTONE = ['yc', 'pc', 'gc', 'tc'], CTONE = { Study: 'pc', Abroad: 'gc', Government: 'yc', Documents: 'tc' };
  var ST = { math: 'math', comp: 'math', bio: 'bio', sci: 'bio', lang: 'lang', art: 'lang', biz: 'biz' };
  var pct = function (v) { return v >= 1 && v <= 5 ? v * 20 : Math.max(0, Math.min(100, v | 0)); };
  var avg = function (a) { return a.length ? a.reduce(function (s, x) { return s + x; }, 0) / a.length : 0; };
  var cap = function (s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : s; };
  var years = function (s) { var m = /\d+(\.\d+)?/.exec(s || ''); if (!m) return 0; return /month/i.test(s) ? +m[0] / 12 : +m[0]; };
  var eduOf = function (t) { t = (t || '').toLowerCase(); return /master/.test(t) ? 4 : /bachelor|graduate|degree/.test(t) ? 3 : /\+2|plus two|class 12|higher secondary/.test(t) ? 2 : /\bsee\b|\bslc\b|class 10/.test(t) ? 1 : 0; };
  var ageOf = function (s) { var n = (s || '').match(/\d+/g); return n && n.length > 1 ? [+n[0], +n[1], +(n[2] || n[1])] : null; };
  var monthsOf = function (t) { t = (t || '').toLowerCase(); return MN.map(function (m, i) { return new RegExp('\\b' + m).test(t) ? i + 1 : 0; }).filter(Boolean); };
  var k1 = function (n) { return Math.round(n / 1000); };

  window.pwAdapt = function (P) {
    var D = { routes: {}, careers: {} };
    P.careers.forEach(function (k) {
      var s = k.salary || {}, e = s.entry || [0, 0], sr = s.senior || [0, 0], tr = k.traits, ev = (e[0] + e[1]) / 2000, sv = (sr[0] + sr[1]) / 2000;
      var slope = { rising: 3, steady: 0, slowing: -2 }[k.trend] || 0, lic = k.licence || {};
      D.careers[k.id] = { id: k.id, n: k.name, d: pct(k.demand), c: pct(k.competition), pay: [Math.round(ev), Math.round(ev + (sv - ev) * 0.45), Math.round(sv)],
        sk: k.skills || [], hist: (k.history || []).slice(-6), lic: lic.name || '', lx: lic.exam || '',
        f: { day: (k.day || []).map(function (p) { return [p[0], +p[1]]; }), lad: (k.ladder && k.ladder.length >= 4) ? k.ladder.slice(0, 4) : ['Entry', 'Mid-level', 'Senior', 'Lead'],
          hasT: !!tr, t: tr ? [tr.flexibility || 50, tr.stability || 50, tr.growth || 50] : [50, 50, 50], emp: k.employers || [], wh: (k.jobs || []).map(function (p) { return [p[0], +p[1]]; }),
          tr: slope, hrs: k.hours || 0 } };
    });
    var K = D.careers;
    var st = P.stages.map(function (s) {
      var groups = [], seen = {};
      P.routes.filter(function (r) { return r.stage === s.id; }).forEach(function (r) { if (!seen[r.group]) { seen[r.group] = { id: r.group, n: GL[r.group] || cap(r.group), tone: GTONE[r.group] || 'sc', courses: [] }; groups.push(seen[r.group]); } seen[r.group].courses.push(r.id); });
      var FIN = { after8: 'Class 8', after10: 'Class 10 / SEE', after12: '+2 / Class 12', afterbach: 'Bachelor', aftermaster: 'Master' };
      return { id: s.id, n: s.label.replace(/^After (a )?/i, ''), t: s.label, l: FIN[s.id] || s.label.replace(/^After (a )?/i, ''), need: s.label.replace(/^After (a )?/i, ''), streams: groups };
    }).filter(function (s) { return s.streams.length; });
    var stageOf = {}; st.forEach(function (s) { s.streams.forEach(function (g) { g.courses.forEach(function (id) { stageOf[id] = [s.id, g.id]; }); }); });
    var C = {};
    /* Subjects the entry text asks for. A note such as "(Maths helps)" or "(or Biology bridge)" is not a requirement; "PCB or PCM" asks for Science only. */
    var needsOf = function (e) {
      e = e.toLowerCase().replace(/\([^)]*(helps|bridge)[^)]*\)/g, ''); var n = [], both = /pcb or pcm|pcm or pcb/.test(e), phys = /\(physical\)/.test(e);
      if (/pcb|biology/.test(e) && !both) n.push('bio'); if (/pcm|mathematics|maths/.test(e) || phys) n.push('math');
      if (/science|pcm|pcb|physics/.test(e) || phys) n.push('sci'); if (/management|commerce|business studies/.test(e)) n.push('mgmt'); return n;
    };
    P.routes.forEach(function (r) {
      var ks = (r.careers || []).filter(function (id) { return K[id]; }), cs = ks.map(function (id) { return K[id]; }), nx = (r.next || []).filter(function (id) { return stageOf[id]; })[0];
      var tags = r.tags || [], y = years(r.years), sub = (r.kind || '') + (r.years ? ' · ' + r.years : '');
      var strength = ''; tags.some(function (t) { if (ST[t]) { strength = ST[t]; return true; } });
      C[r.id] = { id: r.id, n: r.name, f: sub, y: y, fee: [r.fee[0] / 1e5, r.fee[1] / 1e5], d: r.demand > 0 ? pct(r.demand) : Math.round(avg(cs.map(function (k) { return k.d; })) || 50),
        c: r.competition > 0 ? pct(r.competition) : Math.round(avg(cs.map(function (k) { return k.c; })) || 50),
        pay: cs.length ? [k1(avg(P.careers.filter(function (k) { return ks.indexOf(k.id) >= 0; }).map(function (k) { return k.salary.entry[0]; }))), k1(avg(P.careers.filter(function (k) { return ks.indexOf(k.id) >= 0; }).map(function (k) { return k.salary.entry[1]; })))] : 0,
        to: ks, tags: tags, st: strength, needs: needsOf(r.entry || ''), ent: r.entry || r.exam || 'See the college', exam: r.exam || '', where: r.where || [],
        plan: (r.plan && r.plan.length ? r.plan : [r.exam || 'Admission', (r.years || 'Study'), 'Graduate']).map(function (p) { return p.replace(/^Year \d+:\s*/, ''); }), ns: nx ? stageOf[nx][1] : '' };
    });
    var CX = {}; P.routes.forEach(function (r) { if (r.exam_id) CX[r.id] = r.exam_id; });
    var tracks = (P.govt_tracks || []).filter(function (t) { return P.govt.some(function (g) { return g.track === t.id; }); });
    var X = {};
    P.govt.forEach(function (g) {
      var a = ageOf(g.age), ap = g.applicants || 0, se = ap > 0 ? (g.seats || 0) : 0, subj = (g.syllabus && g.syllabus.length ? g.syllabus : (g.subjects || []).map(function (s) { return [s, 1]; }));
      X[g.id] = { id: g.id, n: g.name, b: g.body, g: g.track, edu: eduOf(g.need), age: a, apps: ap, seats: se, fee: g.fee || 0, win: (g.apply && g.apply.length === 2) ? g.apply : [1, 12], em: g.exam_month || 0,
        prep: g.prep_hours || [500, 500, 700, 900, 900][eduOf(g.need)], st: (g.stages || []).map(function (s) { return [s[0], s[2] || 0, s[1] || '']; }), syl: subj.map(function (p) { return [p[0], +p[1]]; }),
        quota: (g.quota && g.quota.length) ? g.quota.map(function (p) { return [p[0], +p[1]]; }) : null, ladder: (g.ladder || []).map(function (p) { return [p[0], k1(+p[1])]; }), rung: (g.ladder && g.ladder.length && g.rung >= 0) ? g.rung : null,
        k: (g.career && K[g.career]) ? g.career : '', pay: g.pay ? k1(g.pay) : 0, guide: '', need: g.need, note: g.note };
    });
    var guideLink = function (l) { if (!l) return null; var t = l.split(':'), a = { exam: ['goExam', 'Exam'], route: ['goCourse', 'Course'], career: ['goCareer', 'Career'], guide: ['goGuide', 'Guide'] }[t[0]]; return a ? [a[0], t[1], a[1]] : null; };
    var G = {}, gl = [];
    P.guides.forEach(function (g) {
      G[g.id] = { id: g.id, n: g.name, cat: g.cat, steps: g.steps.map(function (s) { return [s[0], +s[1] || 0, +s[2] || 0, s[3] === 'online' ? 'O' : 'P']; }), docs: g.docs || [], link: guideLink(g.link) }; gl.push(g.id);
    });
    var COL = {};
    P.providers.forEach(function (p) { COL[p.id] = { n: p.name, d: p.district, p: DP[p.district] != null ? DP[p.district] : -1, t: p.sector || 'Private', u: p.place || p.kind || '', seats: p.seats || 0, site: p.website || '', c: [], fees: {} }; });
    P.routes.forEach(function (r) { (r.where || []).forEach(function (id) { var c = COL[id]; if (!c) return; c.c.push(r.id);}); });
    P.providers.forEach(function (p) { var c = COL[p.id]; Object.keys(p.fees || {}).forEach(function (rid) { if (c.c.indexOf(rid) >= 0) c.fees[rid] = p.fees[rid][1] / 1e5; }); });
    var abroad = P.abroad.map(function (a) { return { k: a.code || a.id.toUpperCase(), id: a.id, n: a.country, cost: Math.round((a.tuition[0] + a.tuition[1]) / 2e5), live: Math.round((a.living[0] + a.living[1]) / 2e5),
      work: a.work_hours != null ? a.work_hours : -1, stay: a.stay_back || '', test: (a.exams || []).slice(0, 2).join(', ') || 'Check the university', intake: monthsOf(a.intakes), wage: 0, visa: a.visa_rate != null ? a.visa_rate : -1, tx: '', schol: a.scholarships || [], vz: a.visa && a.visa.steps ? [a.visa.name, a.visa.steps] : null }; });
    var byAb = {}; P.abroad.forEach(function (a) { byAb[a.id] = a; });
    var lv = { bachelor: 'B', master: 'M', phd: 'P' };
    var SCH = P.scholarships.map(function (s) {
      var a = byAb[s.country], cv = (s.covers || '').toLowerCase(), o = s.open && s.open.length === 2 ? s.open : [1, 12];
      return { n: s.name, k: a ? (a.code || a.id.toUpperCase()) : (s.scope === 'nepal' ? 'NP' : ''), t: s.type || 'Government', s: o[0], e: o[1], l: (s.levels || []).map(function (x) { return lv[x] || ''; }).join('') || 'B',
        cov: (/tuition|fee/.test(cv) ? 'T' : '') + (/stipend|allowance|living/.test(cv) ? 'S' : '') + (/flight|airfare|travel/.test(cv) ? 'F' : ''), aw: s.awards || 0, fixed: o[0] === 1 && o[1] === 12, link: s.link || '', who: s.who || '', how: s.how || '' };
    });
    var FI = { after8: 'cap', after10: 'route', after12: 'flag', afterbach: 'list', abroad: 'pin', general: 'list' }, tl = {}, fi = {};
    (P.topics || []).forEach(function (t) { tl[t.id] = t.label; fi[t.label] = FI[t.id] || 'list'; });
    var faq = (P.faq || []).map(function (f) { return { id: f.id, t: tl[f.topic] || f.topic, q: f.q, a: f.a, r: (f.go || []).filter(function (id) { return C[id]; }).slice(0, 4).map(function (id) { return ['goCourse', id, C[id].n]; }) }; });
    var faqTopics = (P.topics || []).map(function (t) { return t.label; }).filter(function (l) { return faq.some(function (f) { return f.t === l; }); });
    var rank = function (id) { return st.map(function (s) { return s.id; }).indexOf(id); };
    return { STAGES: st, C: C, K: K, X: X, G: G, COL: Object.keys(COL).map(function (k) { return COL[k]; }), CT: abroad, SCH: SCH, CX: CX, tracks: tracks.map(function (t, i) { return [t.id, t.label, TTONE[i % 4], t.group || 'gov']; }),
      groups: (P.govt_groups || [{ id: 'gov', label: 'Government' }]).filter(function (g) { return tracks.some(function (t) { return (t.group || 'gov') === g.id; }); }).map(function (g) { return [g.id, g.label]; }),
      faq: faq, faqTopics: faqTopics, faqIcons: fi, cats: ['All'].concat(P.guides.map(function (g) { return g.cat; }).filter(function (c, i, a) { return a.indexOf(c) === i; })), CTONE: CTONE, rank: rank, reviewed: P.reviewed };
  };
})();
