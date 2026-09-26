#!/usr/bin/env python3
"""Checks that the web's three subject consumers route a subject identically.

neb-art.js picks the art, subject_tokens.py picks the CSS class and the icon.
If they disagree, a card gets rose art under a steel chip. Both are generated
from Color.kt, so they should never diverge -- this is the assertion that says
so out loud.
"""
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
import sys, json, subprocess
sys.path.insert(0, os.path.join(_ROOT, "backend_python/web/templatetags"))
import subject_tokens as T

# Real strings out of the library: exact curriculum names, prefixed and suffixed
# variants, Devanagari, a few that match nothing, and the empty subject.
PROBES = [
    "Physics", "physics", "PHYSICS", "Chemistry", "Mathematics", "Biology",
    "English", "Nepali", "Computer Science", "Economics", "Accountancy",
    "Exam Tips", "Grade 12 Physics", "Compulsory English", "Optional Maths",
    "Health and Physical Education", "Phy. Edu.", "Social Studies",
    "Business Studies", "Book Keeping", "Environmental Science",
    "Computer Networking", "Model Set 2081", "Past Paper 2079",
    "Moral Education", "Hotel Management", "", "   ", "Untitled Subject",
    "सामाजिक अध्ययन",
    "नेपाली", "विज्ञान",
    "गणित", "स्वास्थ्य शिक्षा",
]

NODE = r"""
global.Path2D = function () {};
['moveTo','lineTo','bezierCurveTo','closePath','rect','arc','ellipse']
  .forEach(function (m) { Path2D.prototype[m] = function () {}; });
global.window = global;
global.document = { readyState: 'complete', querySelectorAll: function () { return []; },
  addEventListener: function () {}, documentElement: { getAttribute: function () { return null; } } };
global.ResizeObserver = null; global.matchMedia = null;
require(require('path').join(__dirname, '../../backend_python/web/static/web/js/neb-art.js'));
var probes = JSON.parse(process.argv[2]);
process.stdout.write(JSON.stringify(probes.map(function (s) {
  var hue = NebArt.subjectHue(s);
  return [NebArt.subjectFamily(s), hue.map(function (v) {
    return '#' + ('000000' + ((v >>> 0) & 0xFFFFFF).toString(16).toUpperCase()).slice(-6);
  })];
})));
"""

script = os.path.join(_HERE, ".cmpsubjects.node.js")
with open(script, "w") as f:
    f.write(NODE)
try:
    raw = subprocess.check_output(
        ["node", script, json.dumps(PROBES, ensure_ascii=False)],
        cwd=_HERE)
finally:
    os.unlink(script)
js = json.loads(raw)

bad = 0
for subject, (js_fam, js_hue) in zip(PROBES, js):
    py_fam = T.subject_family(subject)
    py_hue = list(T.subject_hue(subject))
    if py_fam != js_fam or py_hue != js_hue:
        bad += 1
        print("MISMATCH %r" % subject)
        print("  js: %-10s %s" % (js_fam, js_hue))
        print("  py: %-10s %s" % (py_fam, py_hue))

print("subject routing: %d / %d probes agree between neb-art.js and "
      "subject_tokens.py" % (len(PROBES) - bad, len(PROBES)))
if not bad:
    # Show the routing, so a reviewer can see what unknown subjects actually do.
    for s in PROBES:
        print("  %-34s %-10s .subject-%-17s %s"
              % (repr(s), T.subject_family(s), T.subject_slug(s), T.subject_hue(s)[0]))
sys.exit(1 if bad else 0)
