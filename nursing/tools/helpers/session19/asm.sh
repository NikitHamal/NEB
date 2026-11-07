#!/bin/bash
# asm.sh N : parts u{N}a/b/c -> unit file; checker section k{N}.py; fill python outputs, tokens, normalise, verify
set -e; N=$1; D=/tmp/NEB/nursing/course/year-3/family-and-reproductive-health-nursing; P=/tmp/v/bin/python
[ -f /tmp/parts/k$N.py ] && $P /tmp/NEB/nursing/tools/helpers/session19/addsec.py $N
cat /tmp/parts/u${N}a.md /tmp/parts/u${N}b.md $(ls /tmp/parts/u${N}c.md /tmp/parts/u${N}d.md 2>/dev/null) > /tmp/src/frh/unit-0$N.md; cp /tmp/src/frh/unit-0$N.md $D/unit-0$N.md
cd /tmp/NEB
$P nursing/tools/fill_text.py $D/unit-0$N.md; $P nursing/tools/check_frh.py --fill $D/unit-0$N.md; $P nursing/tools/normalize_md.py $D/unit-0$N.md; $P nursing/tools/check_frh.py --verify $D/unit-0*.md
wc -w /tmp/src/frh/unit-0$N.md
