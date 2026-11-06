#!/bin/bash
# assemble check_ger.py and unit file n from parts: build.sh N
set -e
cd /tmp/h/ger; cat head.py $(ls u?.py) tail.py | sed 's/^# ==== END//' > /tmp/NEB/nursing/tools/check_ger.py
