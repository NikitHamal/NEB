#!/usr/bin/env python3
"""Checks that the web's liquid glass is wired up consistently.

There is no SVG renderer in this environment, so the filters cannot be executed
here. What can be checked is every join between the four pieces -- the CSS that
references a filter, the filter that references a map, the map that has to exist
on disk, and the scale that has to match the app's refraction and dispersion --
and those joins are where this sort of thing actually breaks: a renamed id, a
map that was never regenerated, a scale that drifted from the shader's.
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
WEB = os.path.join(_ROOT, "backend_python/web")
CSS = os.path.join(WEB, "static/web/css/material3/08-liquid-glass.css")
BASE = os.path.join(WEB, "templates/base.html")
KOTLIN = os.path.join(
    _ROOT, "app/src/main/java/com/neb/ians/ui/components/NebLiquidGlass.kt")

bad = []


def check(ok, msg):
    print("  %-4s %s" % ("ok" if ok else "FAIL", msg))
    if not ok:
        bad.append(msg)


css = open(CSS).read()
base = open(BASE).read()
kt = open(KOTLIN).read()

print("filter references")
refs = set(re.findall(r"backdrop-filter:\s*url\(#([\w-]+)\)", css))
defs = set(re.findall(r'<filter\s+id="([\w-]+)"', base))
check(bool(refs), "the CSS references at least one filter: %s" % sorted(refs))
for r in sorted(refs):
    check(r in defs, "#%s is defined in base.html" % r)
for d in sorted(defs):
    if d.startswith("neb-glass"):
        check(d in refs, "#%s is actually used by the CSS" % d)

print("displacement maps")
for href in re.findall(r"<feImage\s+href=\"\{% static '([^']+)' %\}\"", base):
    path = os.path.join(WEB, "static", href)
    check(os.path.exists(path),
          "%s exists (%s bytes)"
          % (href, os.path.getsize(path) if os.path.exists(path) else "missing"))
check(len(re.findall(r"<feImage", base)) == len(defs),
      "every filter loads exactly one map")

print("filter graph")
for fid in sorted(defs):
    block = base.split('<filter id="%s"' % fid, 1)[1].split("</filter>", 1)[0]
    check(block.count("<feDisplacementMap") == 3,
          "#%s makes three displacement taps (one per channel)" % fid)
    check('color-interpolation-filters="sRGB"' in
          base.split('<filter id="%s"' % fid, 1)[1].split(">", 1)[0],
          "#%s interpolates in sRGB, not linearRGB" % fid)
    check(block.count('operator="arithmetic"') == 2,
          "#%s recombines the three channels with two adds" % fid)
    # Every declared result has to be consumed, or a tap is silently dropped.
    results = re.findall(r'result="(\w+)"', block)
    used = set(re.findall(r'\bin2?="(\w+)"', block))
    orphans = [r for r in results[:-1] if r not in used]
    check(not orphans, "#%s has no orphaned primitive%s"
          % (fid, "" if not orphans else ": " + ", ".join(orphans)))

print("scale against the app")
# The shader samples at off, off * (1 + d) and off * (1 - d), with the map
# holding half amplitude, so scale = 2 * refraction * (1 +/- dispersion).
refraction = float(re.search(r"refraction = (\d+(?:\.\d+)?)\.dp", kt).group(1))
# rememberNebGlassStyle branches dark-first, so read each branch by name rather
# than taking whichever value the regex reaches first.
style = kt.split("fun rememberNebGlassStyle", 1)[1]
dark_src, light_src = style.split("} else {", 1)
disp_dark = float(re.search(r"dispersion = (\d+\.\d+)f", dark_src).group(1))
disp_light = float(re.search(r"dispersion = (\d+\.\d+)f", light_src).group(1))

# feDisplacementMap's scale is a filter attribute, not a CSS property, so it
# cannot vary with the theme without a second pair of filters. Both themes get
# the light style's dispersion; the check below is that the cost of that is
# small enough to be a decision rather than a bug.
dispersion = disp_light
want = [round(2 * refraction * (1 + dispersion), 2),
        round(2 * refraction, 2),
        round(2 * refraction * (1 - dispersion), 2)]
print("  app: refraction %.0fdp, dispersion %.2f light / %.2f dark -> scales %s"
      % (refraction, disp_light, disp_dark, want))
drift = 2 * refraction * abs(disp_dark - disp_light)
check(drift < 0.5,
      "dark theme reuses the light dispersion, costing %.2fpx on the "
      "outermost tap" % drift)
for fid in sorted(defs):
    block = base.split('<filter id="%s"' % fid, 1)[1].split("</filter>", 1)[0]
    got = [float(v) for v in re.findall(r'scale="([\d.]+)"', block)]
    check(got == want, "#%s scales %s match" % (fid, got))

print("tokens against the app")
for name, pat in [
    ("blur", r"blur = (\d+)\.dp"),
    ("rim", r"rim = (\d+)\.dp"),
]:
    kt_val = re.search(pat, kt).group(1)
    css_val = re.search(r"--neb-glass-%s:\s*(\d+)px" % name, css).group(1)
    check(kt_val == css_val,
          "%s: app %sdp, css %spx" % (name, kt_val, css_val))

# The light vector must be the components of the app's lightAngle.
import math
angle = float(re.search(r"lightAngle: Float = (-?\d+)f", kt).group(1))
lx = float(re.search(r"--neb-glass-lx:\s*([-\d.]+)", css).group(1))
ly = float(re.search(r"--neb-glass-ly:\s*([-\d.]+)", css).group(1))
check(abs(lx - math.cos(math.radians(angle))) < 0.002
      and abs(ly - math.sin(math.radians(angle))) < 0.002,
      "light vector: css (%.3f, %.3f) == cos/sin(%.0fdeg)" % (lx, ly, angle))

print("revert path")
check(css.count("html:not(.neb-no-glass)") >= 6
      and 'class="neb-no-glass"' not in base,
      "every glass rule is gated on html:not(.neb-no-glass), and it is off")
check("background: transparent" in css,
      "glass overrides the surface background rather than the surface "
      "deleting its own")

print("\n%d check%s failed" % (len(bad), "" if len(bad) == 1 else "s"))
sys.exit(1 if bad else 0)
