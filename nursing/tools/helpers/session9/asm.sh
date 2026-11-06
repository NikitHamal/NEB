#!/bin/bash
# asm.sh N : parts -> /tmp/src/psy -> unit file; fill, verify (this unit only for tokens: others may be absent)
set -e; N=$1; D=/tmp/NEB/nursing/course/year-2/psychiatric-nursing; P=/tmp/v/bin/python
bash /tmp/h/build.sh
cat /home/user/sandbox/parts/u${N}a.md /home/user/sandbox/parts/u${N}b.md > /tmp/src/psy/unit-0$N.md; cp /tmp/src/psy/unit-0$N.md $D/unit-0$N.md
cd /tmp/NEB
$P nursing/tools/fill_text.py $D/unit-0$N.md; $P nursing/tools/check_psy.py --fill $D/unit-0$N.md; $P nursing/tools/normalize_md.py $D/unit-0$N.md; $P nursing/tools/check_psy.py --verify $D/unit-0*.md
wc -w /tmp/src/psy/unit-0$N.md
