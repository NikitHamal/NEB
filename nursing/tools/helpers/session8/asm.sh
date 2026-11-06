#!/bin/bash
# asm.sh N : parts -> /tmp/src -> unit file; fill, verify
set -e; N=$1; D=/tmp/NEB/nursing/course/year-2/geriatric-nursing; P=/tmp/v/bin/python
bash /tmp/h/build.sh
cat /app/parts/u${N}a.md /app/parts/u${N}b.md > /tmp/src/ger/unit-0$N.md; cp /tmp/src/ger/unit-0$N.md $D/unit-0$N.md
cd /tmp/NEB
$P nursing/tools/fill_text.py $D/unit-0$N.md; $P nursing/tools/check_ger.py --fill $D/unit-0$N.md; $P nursing/tools/normalize_md.py $D/unit-0$N.md; $P nursing/tools/check_ger.py --verify $D/unit-0*.md
wc -w /tmp/src/ger/unit-0$N.md
