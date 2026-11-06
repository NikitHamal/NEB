#!/bin/bash
set -e
cd /tmp/h/sbs; cat head.py $(ls u?.py 2>/dev/null) tail.py > /tmp/NEB/nursing/tools/check_sbs.py
