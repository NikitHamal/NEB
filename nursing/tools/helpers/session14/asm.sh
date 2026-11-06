#!/bin/bash
# asm.sh N : parts u{N}a/b/c -> unit file; checker section k{N}.py; fill python outputs, tokens, normalise, verify
set -e; N=$1; D=/tmp/NEB/nursing/course/year-3/midwifery-2; P=/tmp/v/bin/python
[ -f /app/parts/k$N.py ] && $P /tmp/NEB/nursing/tools/helpers/session14/addsec.py $N
cat /app/parts/u${N}a.md /app/parts/u${N}b.md $(ls /app/parts/u${N}c.md /app/parts/u${N}d.md 2>/dev/null) > /tmp/src/mw2/unit-0$N.md; cp /tmp/src/mw2/unit-0$N.md $D/unit-0$N.md
cd /tmp/NEB
$P nursing/tools/fill_text.py $D/unit-0$N.md; $P nursing/tools/check_mw2.py --fill $D/unit-0$N.md; $P nursing/tools/normalize_md.py $D/unit-0$N.md; $P nursing/tools/check_mw2.py --verify $D/unit-0*.md
wc -w /tmp/src/mw2/unit-0$N.md
