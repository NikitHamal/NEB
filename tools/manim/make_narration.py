#!/usr/bin/env python3
"""Narration for the Physical Quantities episode, and the timing bookkeeping.

The voice-over is written here, one string per *beat* of the episode, so that
the words and the picture stay tied to the same list.  Two jobs live in this
file:

``script``
    Print the narration grouped the way it is recorded -- one group per
    ``generate_speech`` call -- together with the character count of each
    group, so the recording can be checked against the per-call limit before
    any audio is made.

``timings``
    Read the recorded group MP3s, measure how long each one runs, and write
    ``timings.json`` next to the scene.  ``NebEpisode.beat`` reads that file
    and holds each picture for exactly as long as its own narration runs.

A group's duration is shared out over the beats it contains in proportion to
how many characters each beat carries.  The voice is read at a steady rate, so
that is a good first cut; the numbers are only used to time the holds, never to
cut audio, so a small drift inside a group costs nothing.

Usage::

    tools/manim/make_narration.py script
    tools/manim/make_narration.py timings path/to/narration_dir
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# The narration.  Keys are the beat names used by ``self.beat`` in the scene.
# Beats that are absent here carry no words and keep their animation time only.
# ---------------------------------------------------------------------------

NARRATION: dict[str, str] = {
    # title card
    "s0": (
        "Class eleven physics, unit one: physical quantities. Significant "
        "figures, error, and dimensions - how a number learns to mean "
        "something."
    ),
    # units
    "s1a": (
        "Every measurement is a number times a unit. The number says how much; "
        "the unit says of what. Change the unit, and the number has to change "
        "with it."
    ),
    "s1b": (
        "So quantity equals number times unit, and n one u one equals n two u "
        "two: the value itself never moves."
    ),
    "s1c": (
        "Physics measures in S I units. Seven base quantities: length in "
        "metres, mass in kilograms, time in seconds, current in amperes, "
        "temperature in kelvin, amount in moles, and luminous intensity in "
        "candela. Every other quantity is built out of these."
    ),
    # accuracy and precision
    "s2a": (
        "Accuracy is how close a reading sits to the true value. Precision is "
        "how close repeated readings sit to each other. A clock that runs fast "
        "is precise, but it is not accurate."
    ),
    "s2b": "Precision is limited by the instrument. Accuracy is limited by you.",
    "s2c": (
        "The least count is the smallest reading an instrument can give. On a "
        "vernier calliper, ten vernier divisions span nine main-scale "
        "divisions of one millimetre each, so one vernier division is zero "
        "point nine millimetres, and the least count is zero point one "
        "millimetre."
    ),
    "s3a": (
        "The absolute error of any single reading is taken as half the least "
        "count. A least count of zero point one millimetre therefore carries an "
        "uncertainty of zero point zero five millimetres."
    ),
    "s3b": "This is the built-in uncertainty of the instrument itself.",
    # errors
    "s4a": (
        "Errors come in two families. Systematic errors always push the same "
        "way: a faulty instrument, zero error, or plain bias. Random errors "
        "scatter to both sides: judgement, draughts, and ripple."
    ),
    "s4b": (
        "Random errors shrink when you repeat the reading and take the mean. "
        "The deviation of one reading is that reading minus the mean, and the "
        "mean deviation is the average of all those deviations."
    ),
    "s5a": (
        "A systematic error cannot be averaged away. It has to be found, "
        "corrected, or worked around by changing the method."
    ),
    # significant figures
    "s6a": (
        "Significant figures are the digits known with certainty, plus the "
        "first uncertain digit. They record the precision of a measurement, "
        "not its size."
    ),
    "s6b": (
        "In zero point zero zero two five zero, the leading zeros are only "
        "placeholders. They are not significant."
    ),
    "s7b": (
        "Count from the first non-zero digit: two, five, and the trailing zero. "
        "Three significant figures."
    ),
    "s7c": (
        "Trailing zeros to the right of the decimal point are significant, "
        "because they were measured. Zeros between non-zero digits are "
        "significant too. Only the leading zeros never are."
    ),
    "s7d": "And a zero with a bar over it, or one written as ten to a power, is significant.",
    # rounding and arithmetic
    "s8a": (
        "Round by looking at the digit just after the last one you keep. Less "
        "than five, leave it. Greater than five, raise it. Exactly five with "
        "nothing after, round to the nearest even digit."
    ),
    "s8b": (
        "For answers, addition and subtraction keep the fewest decimal places. "
        "Multiplication and division keep the fewest significant figures."
    ),
    "s9a": (
        "Three point zero metres times two point five zero metres. The rule "
        "says keep the fewest significant figures, which is two, so the answer "
        "is seven point five square metres. The answer is seven point five."
    ),
    # combining uncertainties
    "s10a": (
        "When quantities combine, their uncertainties combine too. For a sum "
        "or a difference, the absolute errors add."
    ),
    "s10a2": (
        "For a product or a quotient, the relative errors add, and in a product "
        "of powers each one is weighted by its own power."
    ),
    "s10b": (
        "For a sum, take both quantities at their largest. Z max equals Z plus "
        "delta A plus delta B, so the absolute error of the sum is simply the "
        "sum of the absolute errors."
    ),
    "s11a": (
        "If the radius of a sphere is measured to one percent, the volume is "
        "good to three percent, because volume depends on the radius cubed."
    ),
    "s11b": "Two terms, three percent.",
    # dimensions
    "s12a": (
        "Dimensions tell you what kind of quantity something is. Force is mass "
        "times acceleration, so its dimensional formula is M L T to the minus "
        "two."
    ),
    "s12b": (
        "The principle of homogeneity says only quantities of the same "
        "dimensions may be added, subtracted or equated. So every term on both "
        "sides of a correct physical equation must carry the same dimensional "
        "formula."
    ),
    "s12c": "Here it is at work.",
    "s13a": "Take v squared equals u squared plus two a s.",
    "s13b": (
        "Every term has the same dimensions: length squared over time squared. "
        "The equation is dimensionally consistent."
    ),
    "s13c": "That is the check you run on any new formula.",
    # converting and deriving
    "s14a": (
        "Dimensions also convert units. One newton is one kilogram metre per "
        "second squared, straight from force equals mass times acceleration."
    ),
    "s14b": (
        "One joule is one newton metre, that is one kilogram metre squared per "
        "second squared, and it is ten to the seven ergs."
    ),
    "s15a": (
        "And they derive relations. Suppose the period of a simple pendulum "
        "depends on mass, length and gravity as T equals k m to the a, l to "
        "the b, g to the c."
    ),
    "s15b": (
        "Comparing dimensions gives a equals zero, b equals one half, and c "
        "equals minus one half. So the period does not depend on the mass at "
        "all, and T equals two pi root l over g."
    ),
    # limits and summary
    "s16a": (
        "Dimensional analysis has limits. It cannot supply a dimensionless "
        "constant like two pi, it cannot tell an addition from a subtraction, "
        "and it says nothing about trigonometric, exponential or logarithmic "
        "functions."
    ),
    "s16b": "So it checks a formula. It never replaces the physics.",
    "s16c": (
        "To sum up: a measurement needs its unit and its uncertainty. "
        "Significant figures carry the precision, systematic and random errors "
        "are handled differently, and dimensions check every equation you "
        "write."
    ),
    "s16d": (
        "Now open the notes, work through the practice questions, and make "
        "these ideas your own."
    ),
}

# ---------------------------------------------------------------------------
# How the narration is recorded: one group per call, in order.  A group must
# stay inside the ~1500 character limit of a single synthesis call.
# ---------------------------------------------------------------------------

GROUPS: list[tuple[str, list[str]]] = [
    ("00_intro_units", ["s0", "s1a", "s1b", "s1c"]),
    ("01_accuracy", ["s2a", "s2b", "s2c", "s3a", "s3b"]),
    ("02_errors", ["s4a", "s4b", "s5a"]),
    ("03_sigfigs", ["s6a", "s6b", "s7b", "s7c", "s7d"]),
    ("04_rounding", ["s8a", "s8b", "s9a"]),
    ("05_combining", ["s10a", "s10a2", "s10b", "s11a", "s11b"]),
    ("06_dimensions", ["s12a", "s12b", "s12c", "s13a", "s13b", "s13c"]),
    ("07_converting", ["s14a", "s14b", "s15a", "s15b"]),
    ("08_limits_summary", ["s16a", "s16b", "s16c", "s16d"]),
]

SCENE = os.path.join(HERE, "videos", "phy11_unit01.py")
TIMINGS = os.path.join(HERE, "videos", "timings.json")

#: how long each beat's own animation runs, and any lead-in pause, in seconds.
#: Recovered by replaying the scene, so the numbers cannot drift from the code.
_BEAT_ANIM = {
    "s0": (1.0, 0.0),
    "s1a": (0.9, 0.0),
    "s1b": (0.6, 0.0),
    "s1c": (0.9, 0.0),
    "s2a": (0.9, 0.0),
    "s2b": (0.6, 0.0),
    "s2c": (0.9, 0.0),
    "s3a": (0.6, 0.0),
    "s3b": (0.6, 0.0),
    "s4a": (0.9, 0.0),
    "s4b": (0.9, 0.0),
    "s5a": (0.6, 0.0),
    "s6a": (0.6, 0.0),
    "s6b": (0.6, 0.0),
    "s7b": (0.6, 0.0),
    "s7c": (0.6, 0.0),
    "s7d": (0.6, 0.0),
    "s8a": (0.9, 0.0),
    "s8b": (0.6, 0.0),
    "s9a": (0.9, 0.0),
    "s10a": (0.9, 0.0),
    "s10a2": (0.6, 0.0),
    "s10b": (0.6, 0.0),
    "s11a": (0.6, 0.0),
    "s11b": (0.6, 0.0),
    "s12a": (0.6, 0.0),
    "s12b": (0.9, 0.0),
    "s12c": (0.6, 0.0),
    "s13a": (0.6, 0.0),
    "s13b": (0.6, 0.0),
    "s13c": (0.6, 0.0),
    "s14a": (0.6, 0.0),
    "s14b": (0.6, 0.0),
    "s15a": (0.9, 0.0),
    "s15b": (0.6, 0.0),
    "s16a": (0.9, 0.0),
    "s16b": (0.6, 0.0),
    "s16c": (0.9, 0.0),
    "s16d": (0.6, 0.0),
}


def group_text(keys: list[str]) -> str:
    """The narration of a whole group, as one paragraph of spoken text."""

    return " ".join(NARRATION.get(key, "") for key in keys).strip()


def measure(path: str) -> float:
    """Duration of an audio file in seconds, via ffprobe."""

    ffmpeg = _ffmpeg()
    probe = os.path.join(os.path.dirname(ffmpeg), "ffprobe")
    if not os.path.exists(probe):
        # imageio-ffmpeg ships only the binary; fall back on ffmpeg itself.
        out = subprocess.run(
            [ffmpeg, "-hide_banner", "-i", path, "-f", "null", "-"],
            capture_output=True,
            text=True,
        ).stderr
        for line in out.splitlines():
            if "Duration:" in line:
                h, m, sec = line.split("Duration:")[1].split(",")[0].strip().split(":")
                return int(h) * 3600 + int(m) * 60 + float(sec)
        raise RuntimeError("no Duration line for %s" % path)
    out = subprocess.run(
        [probe, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return float(out)


def _ffmpeg() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # pragma: no cover - ffmpeg is expected on PATH
        return "ffmpeg"


def cmd_script() -> int:
    total = 0
    for name, keys in GROUPS:
        text = group_text(keys)
        total += len(text)
        print("=" * 78)
        print("%s   (%d characters)" % (name, len(text)))
        print("-" * 78)
        print(text)
    print("=" * 78)
    print("total: %d characters over %d groups" % (total, len(GROUPS)))
    missing = [k for k in NARRATION if not NARRATION[k].strip()]
    if missing:
        print("WARNING: empty narration for %s" % ", ".join(missing))
    return 0


def cmd_timings(directory: str) -> int:
    """Measure each group and write per-beat hold times to timings.json."""

    timings: dict[str, float] = {}
    report = []
    for name, keys in GROUPS:
        path = os.path.join(directory, "%s.mp3" % name)
        if not os.path.exists(path):
            print("missing %s" % path)
            return 1
        duration = measure(path)
        weights = {key: max(1, len(NARRATION.get(key, ""))) for key in keys}
        total_weight = sum(weights.values())
        for key in keys:
            share = duration * weights[key] / total_weight
            run_time, lead = _BEAT_ANIM.get(key, (0.6, 0.0))
            timings[key] = round(run_time + lead + share, 2)
        report.append((name, duration, total_weight))

    with open(TIMINGS, "w", encoding="utf-8") as handle:
        json.dump(timings, handle, indent=2, sort_keys=True)
        handle.write("\n")

    spoken = sum(d for _, d, _ in report)
    print("wrote %s" % TIMINGS)
    for name, duration, _ in report:
        print("  %-18s %6.2f s" % (name, duration))
    print("narration total: %.1f s (%.1f min)" % (spoken, spoken / 60))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in ("script", "timings"):
        print(__doc__.strip().splitlines()[-1])
        print(__doc__)
        return 2
    if argv[1] == "script":
        return cmd_script()
    if len(argv) < 3:
        print("usage: make_narration.py timings <dir with the group MP3s>")
        return 2
    return cmd_timings(argv[2])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
