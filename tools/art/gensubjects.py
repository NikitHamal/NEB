#!/usr/bin/env python3
"""Emits the web's subject colour tokens from the app's Color.kt.

The website had three separate subject-colour tables (--subject-color,
--art-c1..c4, --subject-badge-*), none of which agreed with each other or with
the app, plus a normalizer that only knew ten exact subject names -- so "Health
and Physical Education" or "सामाजिक अध्ययन" fell through to grey while the
banner art above it drew in rose or steel.

There is now one source of truth, Color.kt, and two generated consumers:

  backend_python/web/static/web/css/material3/06-subject-tokens.css
  backend_python/web/templatetags/subject_tokens.py

Both carry the app's family keyword routing, so a subject the table has never
seen lands on the same family -- and therefore the same hue -- as its art.
"""
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
import sys, re, json
sys.path.insert(0, _HERE)
import render as R

CSS_OUT = os.path.join(
    _ROOT, "backend_python/web/static/web/css/material3/06-subject-tokens.css")
PY_OUT = os.path.join(_ROOT, "backend_python/web/templatetags/subject_tokens.py")

BANNER = "GENERATED FILE. Do not hand-edit -- run tools/art/gensubjects.py."


def hexs(c):
    """Compose Color -> #RRGGBB. Subject hues are all fully opaque."""
    return "#%02X%02X%02X" % (round(c.r * 255), round(c.g * 255), round(c.b * 255))


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# The ten named subjects, in the order Color.kt lists them, plus the family
# fallbacks for everything else.
NAMED = [(name, [hexs(c) for c in cols]) for name, cols in R.HUES.items()]
FAMS = [(fam, [hexs(c) for c in cols]) for fam, cols in R.FAM_HUES.items()]

# Icons are a web-only concern (the app uses its own vector set), but they have
# to cover every family or an unknown subject gets no glyph at all.
FAMILY_ICONS = {
    "PHYSICS": "science", "CHEMISTRY": "biotech", "MATH": "calculate",
    "BIOLOGY": "eco", "LANGUAGE": "menu_book", "COMPUTING": "computer",
    "COMMERCE": "trending_up", "EXAM": "quiz", "SCIENCE": "travel_explore",
    "SOCIAL": "public", "HEALTH": "favorite", "GENERAL": "category",
}
NAMED_ICONS = {
    "Physics": "science", "Chemistry": "biotech", "Mathematics": "calculate",
    "Biology": "eco", "English": "menu_book", "Nepali": "translate",
    "Computer Science": "computer", "Economics": "trending_up",
    "Accountancy": "account_balance", "Exam Tips": "quiz",
}
missing = set(R.FAM_HUES) - set(FAMILY_ICONS)
assert not missing, "no icon for family %s" % sorted(missing)
missing = set(R.HUES) - set(NAMED_ICONS)
assert not missing, "no icon for subject %s" % sorted(missing)

# ------------------------------------------------------------------- CSS -----
rows = [("subject-" + slug(n), v, n) for n, v in NAMED]
rows += [("subject-fam-" + f.lower(), v, f + " family") for f, v in FAMS]

css = ["""/* %s
 *
 * One block per subject the curriculum names, then one per family, for every
 * subject it does not. A template asks for its class with the `subject_slug`
 * filter, which routes unknown subjects through the same keyword table the
 * generative art uses -- so the chip, the badge and the art always agree.
 *
 * Light values are the app's light/lightContainer/onLightContainer; the dark
 * block is the same hue lifted into the range that stays legible on navy.
 */
""" % BANNER]

for cls, v, label in rows:
    css.append(""".%s {
  /* %s */
  --subject-color: %s;
  --subject-container: %s;
  --subject-on-container: %s;
}
""" % (cls, label, v[0], v[1], v[2]))

css.append("""
/* ── Dark ── The light hues do not survive a navy surface; these are the same
   hues re-mixed for it, straight from the app's dark ramp. ── */
""")
for cls, v, label in rows:
    css.append("""[data-theme="dark"] .%s {
  --subject-color: %s;
  --subject-container: %s;
  --subject-on-container: %s;
}
""" % (cls, v[3], v[4], v[5]))

css.append("""
/* The default, for an element with no subject class at all. Brand blue, which
   is the GENERAL family's hue, so "no subject" and "unrecognised subject" look
   the same rather than different kinds of broken. */
:root {
  --subject-color: %s;
  --subject-container: %s;
  --subject-on-container: %s;
}

[data-theme="dark"] {
  --subject-color: %s;
  --subject-container: %s;
  --subject-on-container: %s;
}
""" % tuple(dict(FAMS)["GENERAL"]))

with open(CSS_OUT, "w") as f:
    f.write("".join(css))
print("wrote %s (%d subject classes)" % (CSS_OUT, len(rows)))

# ---------------------------------------------------------------- Python -----
def pyrepr(v):
    return json.dumps(v, ensure_ascii=False)


py = ['"""%s\n\nThe subject hue tables and family routing, shared with the app and with\nneb-art.js. Imported by templatetags/web_extras.py.\n"""\n' % BANNER]
py.append("SUBJECT_HUES = {\n")
for n, v in NAMED:
    py.append("    %s: (%s),\n" % (pyrepr(n), ", ".join(pyrepr(c) for c in v)))
py.append("}\n\nFAMILY_HUES = {\n")
for f, v in FAMS:
    py.append("    %s: (%s),\n" % (pyrepr(f), ", ".join(pyrepr(c) for c in v)))
py.append("}\n\n")
py.append("# Ordered: the first family whose keyword appears in the subject wins, so a\n"
          "# string like \"Health and Physical Education\" cannot be claimed by LANGUAGE\n"
          "# on the word \"education\" before HEALTH has had a look at it.\n")
py.append("FAMILY_KEYWORDS = (\n")
for fam, kws in R.FAM_KEYWORDS:
    py.append("    (%s, (%s)),\n" % (pyrepr(fam), ", ".join(pyrepr(k) for k in kws) + ","))
py.append(")\n\n")
py.append("SUBJECT_ICONS = {\n")
for n, _ in NAMED:
    py.append("    %s: %s,\n" % (pyrepr(n), pyrepr(NAMED_ICONS[n])))
py.append("}\n\nFAMILY_ICONS = {\n")
for f, _ in FAMS:
    py.append("    %s: %s,\n" % (pyrepr(f), pyrepr(FAMILY_ICONS[f])))
py.append("}\n\n")
py.append('''_LOWER = {k.lower(): k for k in SUBJECT_HUES}


def subject_family(subject):
    """The family a subject belongs to. Mirrors neb-art.js `subjectFamily` and
    the app's `subjectFamily`, keyword table and order included."""
    s = (subject or "").lower().strip()
    if not s:
        return "GENERAL"
    for fam, kws in FAMILY_KEYWORDS:
        for kw in kws:
            if kw in s:
                return fam
    return "GENERAL"


def subject_key(subject):
    """The exact named subject, if this is one; otherwise None."""
    s = (subject or "").strip()
    return _LOWER.get(s.lower())


def subject_hue(subject):
    """The six-value hue tuple: light, lightContainer, onLightContainer, then
    the same three for dark."""
    key = subject_key(subject)
    if key:
        return SUBJECT_HUES[key]
    return FAMILY_HUES.get(subject_family(subject), FAMILY_HUES["GENERAL"])


def subject_slug(subject):
    """The CSS class suffix, matching a block in material3/06-subject-tokens.css.
    A named subject gets its own; anything else gets its family's."""
    key = subject_key(subject)
    if key:
        import re
        return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")
    return "fam-" + subject_family(subject).lower()


def subject_icon(subject):
    key = subject_key(subject)
    if key:
        return SUBJECT_ICONS[key]
    return FAMILY_ICONS.get(subject_family(subject), "category")
''')

with open(PY_OUT, "w") as f:
    f.write("".join(py))
print("wrote %s (%d subjects, %d families)" % (PY_OUT, len(NAMED), len(FAMS)))
