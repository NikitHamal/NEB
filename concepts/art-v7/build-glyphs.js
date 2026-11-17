/* Builds v7-glyphs.js: the v1 glyph set plus Material Symbols Outlined paths used by v7.
   Usage: node build-glyphs.js /path/to/node_modules/@material-symbols/svg-400/outlined
   (npm i @material-symbols/svg-400, Apache 2.0). Mountains, trees, sun, moon and ships are never listed. */
var fs = require('fs'), path = require('path'), dir = process.argv[2];
global.window = global; require('../art/glyphs.js');
var out = {}, k, miss = [];
for (k in global.NebGlyphs) out[k] = global.NebGlyphs[k];
var EXTRA = ('search_off inbox notifications notifications_off bookmark bookmarks folder_open folder edit_note note_stack sticky_note_2 description article ' +
  'rate_review download cloud_off wifi_off favorite person_search lock trending_up event calendar_month checklist task_alt flag star military_tech ' +
  'local_fire_department timer hourglass_empty upload_file picture_as_pdf video_library play_circle headphones mic image photo_library link share settings tune ' +
  'filter_list sort grid_view dashboard layers category extension widgets rocket diamond key shield support_agent handshake volunteer_activism ' +
  'diversity_3 cast_for_education book library_books import_contacts collections_bookmark edit brush format_shapes interests sports_esports celebration redeem ' +
  'savings shopping_bag explore near_me add_circle search manage_search help info bug_report leaderboard query_stats pie_chart show_chart analytics data_usage ' +
  'schema account_tree database deployed_code self_improvement neurology vaccines stethoscope balance policy record_voice_over podcasts piano ' +
  'view_in_ar agriculture grass pest_control water bubble_chart scatter_plot hexagon pentagon change_history square_foot calculate functions pan_tool_alt ' +
  'flash_on bolt cloud lightbulb alarm mail send person group_add badge id_card contact_page assignment assignment_turned_in fact_check rule history_toggle_off ' +
  'schedule today update sync cloud_download offline_pin done_all verified_user workspace_premium').split(/\s+/).filter(Boolean);
EXTRA.forEach(function (n) {
  if (out[n]) return;
  var f = path.join(dir, n + '.svg');
  if (!fs.existsSync(f)) { miss.push(n); return; }
  var m = /<path d="([^"]+)"/.exec(fs.readFileSync(f, 'utf8'));
  if (m) out[n] = m[1]; else miss.push(n);
});
delete out.forest; delete out.compost;
fs.writeFileSync(path.join(__dirname, 'v7-glyphs.js'), '/* Material Symbols Outlined (400) glyph paths, viewBox 0 -960 960 960. Apache 2.0. Built by build-glyphs.js. */\nwindow.NebGlyphs=' + JSON.stringify(out) + ';\n');
console.log(Object.keys(out).length + ' glyphs, missing: ' + miss.join(' '));
