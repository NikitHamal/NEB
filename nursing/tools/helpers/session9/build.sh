#!/bin/bash
set -e
cd /tmp/h/psy; cat head.py $(ls u?.py 2>/dev/null) tail.py | sed 's/^# ==== END//' > /tmp/NEB/nursing/tools/check_psy.py
