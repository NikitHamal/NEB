/* Building blocks shared by every profile type. Icons are Material Symbols Outlined, never drawn by hand. */
window.S = { theme: 'light', self: false, art: 'v2' };
window.U = (function () {
  var N = window.NebArt, V2 = window.NebArtV2;
  var ROLE_MAP = { graph: 'roleStudent', orbit: 'roleTeacher', arches: 'roleInstitution', stack: 'roleContributor' };
  var U = {
    ms: function (n, c) { return '<span class="ms ' + (c || '') + '">' + n + '</span>'; },
    av: function (letter, shape, tone, c) {
      return '<svg class="av ' + (c || '') + ' ' + tone + '" viewBox="0 0 100 100" aria-hidden="true"><path d="' + N.shapeD(shape, 50, 50, 43, 0) + '"/><text x="50" y="52" text-anchor="middle" dominant-baseline="central" font-size="40">' + letter + '</text></svg>';
    },
    art: function (kind, seed, o) {
      o = o || {};
      if (S.art === 'v2' && V2) {
        var lay = (kind === 'cover' || kind === 'school') && ROLE_MAP[o.layout] ? ROLE_MAP[o.layout] : (V2.scenes[o.layout] || V2.layouts[o.layout] ? o.layout : undefined);
        return V2.make({ kind: kind, seed: seed, subject: o.subject, palette: o.palette, layout: lay, glyph: o.glyph, mode: S.theme });
      }
      return N.make({ kind: kind, seed: seed, subject: o.subject, palette: o.palette, layout: o.layout, glyph: o.glyph, mode: S.theme, motif: o.motif || 'none' });
    },
    glyph: function (icon, c) { return '<span class="glyph ' + c + '">' + U.ms(icon) + '</span>'; },
    head: function (title, count, tab) {
      return '<div class="mh"><h3>' + title + (count != null ? '<i>' + count + '</i>' : '') + '</h3>' + (tab ? '<button class="see" data-act="tab" data-tab="' + tab + '">See all' + U.ms('chevron_right', 's') + '</button>' : '') + '</div>';
    },
    verified: function (v) { return v ? '<span class="vf" title="Verified">' + U.ms('verified', 'f') + '</span>' : ''; },
    /* the website's resource-card, same anatomy: art, type pill, subject icon, subject chip, title, meta, author, views */
    resource: function (r) {
      var sub = N.subjects[r.subject] ? r.subject : 'Education';
      return '<button class="resource-card" data-act="open" data-what="' + r.title + '"><div class="rc-art">' + U.art('thumb', r.seed, { subject: sub, motif: 'none' }) + '<span class="rc-type">' + r.type + '</span><span class="rc-ic">' + U.ms(N.glyphFor(sub)) + '</span></div>' +
        '<div class="rc-info"><span class="rc-subj">' + r.subject + '</span><div class="rc-title">' + r.title + '</div><div class="rc-meta">' + r.meta + '</div>' +
        '<div class="rc-foot">' + U.av(r.by[0], r.shape || 'cookie', r.tone || 't1', 'sm') + '<div><b>' + r.by + '</b><small>' + r.when + ', ' + U.ms('visibility', 'xs') + ' ' + r.views + '</small></div></div></div></button>';
    },
    /* the website's post-card: author line, #category tag, title, body, thumb_up / comments / views / share */
    post: function (p, who) {
      var liked = p.liked ? ' liked' : '';
      return '<article class="post-card' + (p.pin ? ' pin' : '') + '">' + (p.pin ? '<div class="pinl">' + U.ms('push_pin', 's f') + 'Pinned</div>' : '') +
        '<div class="ph">' + U.av(who.letter, who.shape, who.tone, 'sm') + '<div class="meta2"><div class="pn">' + who.name + (who.verified ? U.ms('verified') : '') + '</div><div class="pm"><span class="tag">#' + p.cat + '</span><span>' + p.when + '</span></div></div><button class="iconbtn" aria-label="More">' + U.ms('more_horiz') + '</button></div>' +
        '<div class="pt">' + p.title + '</div><div class="pb">' + p.body + '</div>' +
        '<div class="pa"><button data-act="like" class="' + liked + '" data-n="' + p.likes + '">' + U.ms('thumb_up') + '<b>' + p.likes + '</b></button><span>' + U.ms('mode_comment') + p.comments + '<em style="font-style:normal"> comments</em></span>' + (S.self ? '<span>' + U.ms('visibility') + p.views + '</span>' : '') + '<i class="sp"></i><button data-act="share">' + U.ms('ios_share') + 'Share</button></div></article>';
    },
    chip: function (t, c, icon) { return '<span class="chip ' + (c || '') + '">' + (icon ? U.ms(icon, 'xs') : '') + t + '</span>'; },
    row: function (icon, c, t, s, end) { return '<div class="row">' + U.glyph(icon, c) + '<div class="grow"><b>' + t + '</b><small>' + s + '</small></div>' + (end ? '<div class="end">' + end + '</div>' : '') + '</div>'; },
    /* Open to: tonal tiles with an icon shape, the offer and the specific, replacing the old row of coloured pills */
    openTo: function (items) {
      return '<section class="open">' + U.head('Open to', items.length) + '<div class="ot">' + items.map(function (o, i) {
        return '<button data-act="invite" data-what="' + o.t + '"><div class="rowt">' + U.glyph(o.i, 'c' + (o.c || 1)) + U.ms(S.self ? 'edit' : 'arrow_outward', 's go') + '</div><div><b>' + o.t + '</b><small>' + o.d + '</small></div></button>';
      }).join('') + '</div></section>';
    },
    /* Studying now: subject art, chapter, segmented progress, week bars, resource link */
    studying: function (s) {
      var segs = '', i, wk = '';
      for (i = 0; i < s.total; i++) segs += '<i class="' + (i < s.ch - 1 ? 'd' : i === s.ch - 1 ? 'n' : '') + '"></i>';
      s.week.forEach(function (h, j) { wk += '<i class="' + (j === s.week.length - 1 ? 'today' : 'd') + '" style="height:' + Math.max(8, h * 7) + '%"></i>'; });
      return '<section>' + U.head('Studying now') + '<div class="card study"><div class="sa">' + U.art('thumb', s.seed, { subject: s.subject }) + '<span class="chip p">' + U.ms(N.glyphFor(s.subject), 'xs') + s.subject + '</span></div>' +
        '<div class="sb2"><div><h4>' + s.title + '</h4><div class="ch">Chapter ' + s.ch + ' of ' + s.total + ', ' + s.exam + '</div></div><div class="segs">' + segs + '</div>' +
        '<div class="srow"><div class="st"><span>' + U.ms('schedule', 's') + s.today + '</span><span>' + U.ms('local_fire_department', 's') + s.streak + ' days</span></div><div class="wk" style="width:96px">' + wk + '</div></div>' +
        '<button class="link" data-act="open" data-what="' + s.res + '">' + U.ms('menu_book') + '<div class="grow" style="flex:1"><b>' + s.res + '</b><small>Reading now</small></div>' + U.ms('chevron_right') + '</button></div></div></section>';
    },
    glance: function (a) { return '<section class="glance">' + a.map(function (g, i) { return '<div class="gt c' + g.c + '">' + U.ms(g.i) + '<div><b>' + g.n + '</b><span>' + g.l + '</span></div></div>'; }).join('') + '</section>'; },
    call: function (c, who) {
      return '<section>' + U.head('Contact') + '<div class="card call">' + U.glyph('call', 'c2') + '<div class="grow" style="flex:1"><b>' + c.phone + '</b><small>' + c.hours + '</small></div><button class="btn f" data-act="call" data-phone="' + c.phone + '">' + U.ms('call', 's') + 'Call</button></div></section>';
    }
  };
  return U;
})();
