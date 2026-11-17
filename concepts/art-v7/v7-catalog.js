/* The named v7 set. Same entries in, same drawings out. Ids are stable: kind-001, kind-002 ...
   Order inside a kind never changes; new pieces are only ever appended. */
(function (g) {
  var N = g.NebArt, SUBS = N.subjectNames, PAL = N.palettes, GL = Object.keys(g.NebGlyphs || {}), LAY = N.layoutNames;
  var pad = function (n) { return ('00' + n).slice(-3); };
  var CALM = N.kinds.note.layouts;
  N.emptyStates = [
    ['No results', 'search_off', 'azure'], ['No resources', 'folder_open', 'sky'], ['No notes', 'edit_note', 'amber'], ['No bookmarks', 'bookmark', 'coral'],
    ['No notifications', 'notifications_off', 'teal'], ['No posts', 'article', 'periwinkle'], ['No comments', 'rate_review', 'rose'], ['No followers', 'group_add', 'mint'],
    ['Not following anyone', 'person_search', 'ocean'], ['No downloads', 'download', 'aqua'], ['You are offline', 'cloud_off', 'slate'], ['No connection', 'wifi_off', 'clay'],
    ['No history', 'history', 'sage'], ['No favourites', 'favorite', 'cherry'], ['No events', 'event', 'citrine'], ['No quizzes', 'quiz', 'orange'],
    ['No pathways', 'travel_explore', 'lagoon'], ['No badges yet', 'workspace_premium', 'amber'], ['No collections', 'collections_bookmark', 'moss'], ['No files', 'upload_file', 'sky'],
    ['No videos', 'video_library', 'coral'], ['No audio', 'headphones', 'teal'], ['No pictures', 'photo_library', 'rose'], ['No links', 'link', 'azure'],
    ['No tasks', 'checklist', 'mint'], ['No drafts', 'description', 'periwinkle'], ['No PDFs', 'picture_as_pdf', 'cherry'], ['No schools', 'school', 'ocean'],
    ['No teachers', 'cast_for_education', 'sage'], ['No books', 'library_books', 'amber'], ['No stories', 'auto_stories', 'clay'], ['No polls', 'leaderboard', 'teal'],
    ['No messages', 'mail', 'ocean'], ['No activity', 'query_stats', 'lagoon'], ['No reports', 'bug_report', 'orange'], ['Locked', 'lock', 'slate'],
    ['Something went wrong', 'help', 'coral'], ['Under maintenance', 'settings', 'citrine'], ['Archive is empty', 'inbox', 'sky'], ['Bin is empty', 'folder', 'moss'],
    ['No tags', 'category', 'mint'], ['No saved searches', 'manage_search', 'azure'], ['All done', 'task_alt', 'moss'], ['Welcome', 'celebration', 'rose']
  ];

  N.catalog = function () {
    var out = [], i, j, id = {};
    function add(kind, o) { id[kind] = (id[kind] || 0) + 1; o.kind = kind; o.id = kind + '-' + pad(id[kind]); o.group = o.group || N.kinds[kind].label; out.push(o); }
    for (i = 0; i < LAY.length; i++) for (j = 0; j < PAL.length; j++) add('cover', { seed: i * 31 + j, layout: LAY[i], palette: PAL[j], tag: LAY[i] });
    for (i = 0; i < 96; i++) add('school', { seed: 500 + i, palette: PAL[(i * 5) % PAL.length], tag: PAL[(i * 5) % PAL.length] });
    for (i = 0; i < SUBS.length; i++) for (j = 0; j < 8; j++) add('thumb', { seed: i * 8 + j, subject: SUBS[i], tag: SUBS[i] });
    for (i = 0; i < SUBS.length; i++) for (j = 0; j < 4; j++) add('book', { seed: 900 + i * 4 + j, subject: SUBS[i], tag: SUBS[i] });
    for (i = 0; i < PAL.length; i++) for (j = 0; j < 8; j++) add('note', { seed: 3000 + i * 8 + j, layout: CALM[(i * 5 + j * 3) % CALM.length], palette: PAL[i], tag: PAL[i], android: j < 4 });
    for (i = 0; i < N.emptyStates.length; i++) for (j = 0; j < 4; j++) add('empty', { seed: 4000 + i * 4 + j, variant: j, glyph: N.emptyStates[i][1], palette: N.emptyStates[i][2], tag: N.emptyStates[i][0], title: N.emptyStates[i][0] });
    for (i = 0; i < PAL.length; i++) for (j = 0; j < 16; j++) add('avatar', { seed: 5000 + i * 16 + j, variant: j % 8, glyph: GL[(i * 7 + j * 3) % GL.length], palette: PAL[i], tag: PAL[i] });
    for (i = 0; i < 72; i++) add('post', { seed: 1300 + i, palette: PAL[i % PAL.length], tag: PAL[i % PAL.length] });
    for (i = 0; i < 90; i++) add('bg', { seed: 1700 + i, palette: PAL[(i * 7) % PAL.length], tag: PAL[(i * 7) % PAL.length] });
    for (i = 0; i < 72; i++) add('wall', { seed: 6000 + i, palette: PAL[(i * 5) % PAL.length], tag: PAL[(i * 5) % PAL.length] });
    for (i = 0; i < 36; i++) add('story', { seed: 7000 + i, palette: PAL[(i * 7) % PAL.length], tag: PAL[(i * 7) % PAL.length] });
    for (i = 0; i < 54; i++) add('strip', { seed: 8000 + i, palette: PAL[(i * 5) % PAL.length], tag: PAL[(i * 5) % PAL.length] });
    for (i = 0; i < 72; i++) add('tile', { seed: 2100 + i, subject: SUBS[i % SUBS.length], palette: PAL[(i * 5 + 3) % PAL.length], tag: SUBS[i % SUBS.length] });
    for (i = 0; i < SUBS.length; i++) for (j = 0; j < 2; j++) add('icon', { seed: 9000 + i * 2 + j, subject: SUBS[i], palette: PAL[(i * 5 + j * 7) % PAL.length], tag: SUBS[i] });
    for (i = 0; i < GL.length; i++) add('sticker', { seed: 2500 + i, glyph: GL[i], palette: PAL[(i * 5) % PAL.length], tag: GL[i] });
    return out;
  };
  N.render = function (o, mode) { var c = {}; for (var k in o) c[k] = o[k]; c.mode = mode || 'light'; return N.make(c); };
  if (typeof module !== 'undefined') module.exports = N;
})(typeof window !== 'undefined' ? window : globalThis);
